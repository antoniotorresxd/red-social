<template>
  <Layout>
    <div class="chat-wrapper d-lg-flex gap-1 mx-n4 mt-n4 p-1">

      <!-- Sidebar de chats -->
      <div class="chat-leftsidebar border d-flex flex-column">
        <div class="px-4 pt-4 mb-4">
          <div class="d-flex align-items-start">
            <h5 class="flex-grow-1 mb-4">Chats</h5>
            <BButton variant="soft-primary" size="sm" @click="openCreateChat">
              <i class="ri-add-line align-bottom" />
            </BButton>
          </div>
          <div class="search-box mt-2">
            <input v-model="searchQuery" type="text" class="form-control bg-light border-light"
              placeholder="Buscar..." />
            <i class="ri-search-2-line search-icon"></i>
          </div>
        </div>

        <simplebar class="chat-room-list flex-fill" data-simplebar>
          <ul class="list-unstyled chat-list chat-user-list">
            <li v-for="chat in filteredChats" :key="chat._id" @click="selectChat(chat)"
              :class="{ active: activeChat && activeChat._id === chat._id }" class="py-2 px-3 hover-bg rounded mb-1">
              <div class="d-flex align-items-center">
                <div class="flex-shrink-0 chat-user-img online me-2">
                  <div class="avatar-xxs"></div>
                </div>
                <p class="mb-0 text-truncate flex-grow-1">
                  {{ getChatName(chat) }}
                </p>
              </div>
            </li>
          </ul>
        </simplebar>
      </div>

      <!-- Área de chat -->
      <div class="user-chat w-100 d-flex flex-column p-4">

        <!-- Header móvil -->
        <div class="d-flex align-items-center mb-4 d-lg-none">
          <BLink href="javascript:void(0)" class="user-chat-remove fs-18 p-1 me-3">
            <i class="ri-arrow-left-s-line align-bottom"></i>
          </BLink>
          <h5 class="mb-0">Chats</h5>
        </div>

        <!-- Formulario de crear chat -->
        <div v-if="showCreateChat" class="mt-4 d-flex">
          <div class="card shadow-sm" style="min-width: 330px; max-width: 350px;">
            <div class="card-body">
              <h5 class="card-title text-center mb-3">Agregar chat</h5>
              <div class="mb-3">
                <label class="form-label">Correo institucional</label>
                <input v-model="chatEmail" type="email" class="form-control" placeholder="usuario@alumno.ipn.mx" />
              </div>
              <div class="d-flex justify-content-end">
                <BButton variant="primary" size="sm" class="ms-2" @click="handleCreateChat">
                  Buscar
                </BButton>
              </div>
            </div>
          </div>
        </div>

        <!-- Área de mensajes -->
        <template v-else-if="activeChat">
          <simplebar ref="messagesArea" class="messages-area flex-grow-1" data-simplebar>

            <!-- <div class="messages-area flex-grow-1 overflow-auto"> -->
            <div v-for="msg in messages" :key="msg._id" class="mb-3"
              :class="msg.sender_id === userId ? 'text-end' : 'text-start'">
              <div :class="[
                'd-inline-block px-3 py-2 rounded',
                msg.sender_id === userId ? 'bg-primary text-white' : 'bg-light text-dark'
              ]">
                {{ msg.message }}
              </div>
              <small class="d-block text-muted">{{ formatTimestamp(msg.timestamp) }}</small>
            </div>
            <!-- </div> -->
            <div ref="bottomAnchor"></div>
          </simplebar>

          <div class="chat-input bg-white border-top pt-3 pb-3 mb-5">
            <div class="d-flex">
              <input v-model="newMessage" type="text" class="form-control me-2" placeholder="Escribe un mensaje..."
                @keyup.enter="handleSubmitMessage" />
              <BButton variant="primary" size="sm" @click="handleSubmitMessage">
                Enviar
              </BButton>
            </div>
          </div>
        </template>

        <!-- Espacio vacío si no hay chat activo -->
        <div v-else class="flex-grow-1"></div>
      </div>
    </div>
  </Layout>
</template>

<script>
import simplebar from 'simplebar-vue'
import Layout from '@/layouts/main.vue'
import api from '@/router/api'
import axios from 'axios'

export default {
  components: { Layout, simplebar },
  data() {
    return {
      ws: null,
      chatList: [],
      activeChat: null,
      messages: [],
      newMessage: '',
      chatEmail: '',
      showCreateChat: false,
      searchQuery: '',
      wsReady: false,
      userId: localStorage.getItem('user_id'),
      userEmail: localStorage.getItem('user_email'),
    }
  },
  computed: {
    filteredChats() {
      const query = this.searchQuery.toLowerCase()
      return query
        ? this.chatList.filter(c => this.getChatName(c).toLowerCase().includes(query))
        : this.chatList
    }
  },
  methods: {
    openCreateChat() {
      this.showCreateChat = true
      if (window.innerWidth < 992) {
        document.querySelector('.user-chat').classList.add('user-chat-show')
      }
    },
    selectChat(chat) {
      this.activeChat = chat
      this.messages = [] // limpiar mensajes actuales
      this.sendWebSocketMessage({
        event: 'join_chat',
        room_id: chat._id,
      })
      this.showCreateChat = false
      if (window.innerWidth < 992) {
        document.querySelector('.user-chat').classList.add('user-chat-show')
      }
    },
    formatTimestamp(ts) {
      return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    async getUserIdByEmail(email) {
      try {
        const { data } = await axios.get(api.users.find_by_email, { params: { email } })
        return data.data?.id || null
      } catch {
        return null
      }
    },
    sendWebSocketMessage(payload) {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify(payload))
      } else {
        alert('Conexión de chat no lista. Intenta de nuevo.')
      }
    },
    async handleCreateChat() {
      if (!this.chatEmail) {
        alert('Ingresa un correo válido')
        return
      }
      const targetUserId = await this.getUserIdByEmail(this.chatEmail)
      if (!targetUserId) return

      this.sendWebSocketMessage({
        event: 'create_chat',
        participants: [this.userId, targetUserId.toString()],
        token: localStorage.getItem('access'),
      })

      this.showCreateChat = false
      this.chatEmail = ''
    },
    handleSubmitMessage() {
      const text = this.newMessage.trim()
      if (!text || !this.activeChat) return

      if (this.ws?.readyState !== WebSocket.OPEN) {
        console.warn("WebSocket no está listo")
        return
      }

      const payload = {
        event: 'submit_message',
        room_id: this.activeChat._id,
        sender: this.userId,
        message: text,
      }
      this.ws.send(JSON.stringify(payload))
      this.newMessage = ''
    },

    initializeWebSocket() {
      this.ws = new WebSocket(api.chat.ws_chat)
      this.ws.onopen = () => {
        this.wsReady = true
        this.sendWebSocketMessage({
          event: 'list_chats',
          user: this.userId,
          token: localStorage.getItem('access'),
        })
      }

      this.ws.onmessage = ({ data }) => {
        const msg = JSON.parse(data)
        switch (msg.event) {
          case 'chats_list':
            this.chatList = msg.chats || []
            break
          case 'chat_created':
            this.chatList.unshift({ _id: msg.room_id, participants: msg.participants })
            this.activeChat = this.chatList[0]
            break
          case 'chat_exists':
            this.activeChat = this.chatList.find(c => c._id === msg.room_id) || null
            break
          case 'new_message':
            if (this.activeChat && msg.room_id === this.activeChat._id) {
              this.messages.push({
                _id: Date.now().toString(),
                sender_id: msg.sender,
                message: msg.message,
                timestamp: msg.timestamp,
              })
              this.$nextTick(() => this.scrollToBottom(true))
            }
            break
          case 'chat_history':
            if (this.activeChat && msg.room_id === this.activeChat._id && Array.isArray(msg.messages)) {
              console.log(msg.messages)
              this.messages = msg.messages.map(m => ({
                _id: m._id,
                sender_id: m.sender_id,
                message: m.message,
                timestamp: m.timestamp,
              }))
            } else {
              this.messages = []
            }
            this.$nextTick(() => this.scrollToBottom(true))
            break
        }
      }

      this.ws.onclose = this.ws.onerror = () => {
        this.wsReady = false
      }
    },
    getChatName(chat) {
      const other = (chat.participants || []).find(e => e !== this.userEmail)
      return other || 'Chat'
    },
scrollToBottom(force = false) {
  const wrapper = this.$refs.messagesArea?.$el || this.$refs.messagesArea
  const scrollEl = wrapper?.querySelector('.simplebar-content-wrapper')
  if (!scrollEl) return

  const atBottom =
    scrollEl.scrollHeight - scrollEl.scrollTop - scrollEl.clientHeight < 50

  if (force || atBottom) {
    scrollEl.scrollTop = scrollEl.scrollHeight
  }
}


  },
  mounted() {
    document.querySelectorAll('.user-chat-remove').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelector('.user-chat')?.classList.remove('user-chat-show')
      })
    })
    this.initializeWebSocket()
  },
  beforeUnmount() {
    this.ws?.close()
  },
}
</script>

<style scoped>
.chat-wrapper {
  position: relative;
  min-height: calc(100vh - 56px);
}

.user-chat {
  display: flex;
  flex-direction: column;
  background: #fff;
  height: 100%;
}

@media (max-width: 991.98px) {
  .user-chat {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #fff;
    transform: translateX(100%);
    transition: transform 0.3s ease-in-out;
    z-index: 5;
  }

  .user-chat.user-chat-show {
    transform: translateX(0);
  }
}

@media (min-width: 992px) {
  .user-chat {
    position: relative;
    transform: none !important;
  }
}

.messages-area {
  flex-grow: 1;
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.chat-input {
  flex: 0 0 auto;
}

.chat-leftsidebar .dropdown-menu {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
