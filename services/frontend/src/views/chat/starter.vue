<template>
  <Layout>
    <div class="chat-wrapper d-lg-flex gap-1 mx-n4 mt-n4 p-1">
      <!-- Sidebar (idéntico al tuyo) -->
      <div class="chat-leftsidebar border d-flex flex-column">
        <!-- Header + buscador + botón -->
        <div class="px-4 pt-4 mb-4">
          <div class="d-flex align-items-start">
            <div class="flex-grow-1">
              <h5 class="mb-4">Chats</h5>
            </div>
            <div class="flex-shrink-0 position-relative" ref="menuWrapper">
              <BButton variant="soft-primary" size="sm" @click="openCreateChat">
                <i class="ri-add-line align-bottom" />
              </BButton>
            </div>
          </div>
          <div class="search-box mt-2">
            <input v-model="searchQuery" type="text" class="form-control bg-light border-light"
              placeholder="Buscar..." />
            <i class="ri-search-2-line search-icon"></i>
          </div>
        </div>

        <!-- Lista de chats -->
        <simplebar class="chat-room-list flex-fill" data-simplebar>
          <ul class="list-unstyled chat-list chat-user-list">
            <li v-for="chat in filteredChats" :key="chat._id" @click="selectChat(chat)"
              :class="{ active: activeChat && activeChat._id === chat._id }" class="py-2 px-3 hover-bg rounded mb-1">
              <div class="d-flex align-items-center">
                <div class="flex-shrink-0 chat-user-img online align-self-center me-2">
                  <div class="avatar-xxs"></div>
                </div>
                <div class="flex-grow-1 overflow-hidden">
                  <p class="text-truncate mb-0">{{ getChatName(chat) }}</p>
                </div>
              </div>
            </li>
          </ul>
        </simplebar>
      </div>

      <!-- Área de trabajo (idéntico al de Community, sin forzar height) -->
      <div class="user-chat w-100 d-flex flex-column p-4">
        <!-- Header móvil -->
        <div class="d-flex align-items-center mb-4 d-lg-none">
          <BLink href="javascript:void(0)" class="user-chat-remove fs-18 p-1 me-3">
            <i class="ri-arrow-left-s-line align-bottom"></i>
          </BLink>
          <h5 class="mb-0">Chats</h5>
        </div>

        <!-- Formulario de crear chat -->

        <div v-if="showCreateChat" class="mt-4 d-flex ">
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


        <template v-else-if="activeChat">
          <!-- Mensajes (única parte scrollable) -->
          <div class="messages-area flex-grow-1 overflow-auto">
            <div v-for="msg in messages" :key="msg._id" class="mb-3">
              <div :class="msg.sender_id === userId ? 'text-end' : 'text-start'">
                <div :class="[
                  'd-inline-block px-3 py-2 rounded',
                  msg.sender_id === userId
                    ? 'bg-primary text-white'
                    : 'bg-light text-dark'
                ]">
                  {{ msg.message }}
                </div>
                <small class="d-block text-muted">{{ formatTimestamp(msg.timestamp) }}</small>
              </div>
            </div>
          </div>

          <!-- Input de chat siempre abajo, igual que en Community -->
          <div class="chat-input bg-white border-top pt-3 pb-3 mb-5">
            <div class="d-flex">
              <input type="text" v-model="newMessage" class="form-control me-2" placeholder="Escribe un mensaje..."
                @keyup.enter="handleSubmitMessage" />
              <BButton variant="primary" size="sm" @click="handleSubmitMessage">
                Enviar
              </BButton>
            </div>
          </div>
        </template>

        <!-- Si no hay chat seleccionado, ocupa espacio en blanco -->
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
      userId: localStorage.getItem('user_id'),
      wsReady: false,
      userEmail: localStorage.getItem('user_email'),
    }
  },
  computed: {
    filteredChats() {
      const lower = this.searchQuery.toLowerCase()
      return lower
        ? this.chatList.filter(c => this.getChatName(c).toLowerCase().includes(lower))
        : this.chatList
    },
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
        const response = await axios.get(api.users.find_by_email, {
          params: { email }
        })
        return (response.data.data && response.data.data.id) || null
      } catch {
        return null
      }
    },
    sendWebSocketMessage(payload) {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
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
      const payload = {
        event: 'create_chat',
        participants: [this.userId, targetUserId.toString()],
        token: localStorage.getItem('access'),
      }
      this.sendWebSocketMessage(payload)
      this.showCreateChat = false
      this.chatEmail = ''
    },
    handleSubmitMessage() {
      this.newMessage = ''
    },
    initializeWebSocket() {
      this.ws = new WebSocket(api.chat.ws_chat)
      this.ws.onopen = () => {
        this.wsReady = true
        const payload = {
          event: 'list_chats',
          user: this.userId.toString(),
          token: localStorage.getItem('access'),
        }
        this.sendWebSocketMessage(payload)
      }
      this.ws.onmessage = event => {
        const data = JSON.parse(event.data)
        if (data.event === 'chats_list') {
          this.chatList = data.chats || []
        } else if (data.event === 'chat_created') {
          this.chatList.unshift({ _id: data.room_id, participants: data.participants })
          this.activeChat = this.chatList[0]
        } else if (data.event === 'chat_exists') {
          this.activeChat = this.chatList.find(c => c._id === data.room_id) || null
        }
      }
      this.ws.onclose = () => {
        this.wsReady = false
      }
      this.ws.onerror = () => {
        this.wsReady = false
      }
    },
    getChatName(chat) {
      if (!Array.isArray(chat.participants)) return 'Chat'
      const filtered = chat.participants.filter(e => !!e)
      const other = filtered.find(e => e !== this.userEmail)
      return other || 'Chat'
    },
  },
  mounted() {
    document.querySelectorAll('.user-chat-remove').forEach(item => {
      item.addEventListener('click', () => {
        document.querySelector('.user-chat').classList.remove('user-chat-show')
      })
    })
    this.initializeWebSocket()
  },
  beforeUnmount() {
    if (this.ws) this.ws.close()
  },
}
</script>

<style scoped>
.chat-leftsidebar .dropdown-menu {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.chat-wrapper {
  position: relative;
  min-height: calc(100vh - 56px);
}

/* .user-chat en escritorio NO forzamos height; solo en móvil lo hacemos deslizante */
.user-chat {
  display: flex;
  flex-direction: column;
   background: #fff;
}

@media (max-width: 991.98px) {

  /* En móvil, abrimos/deslizamos la capa completa */
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

.messages-area {
  flex: 1 1 0;
  min-height: 0;
  overflow-y: auto;
}

.chat-input {
  flex: 0 0 auto;
}

@media (min-width: 992px) {
  .user-chat {
    position: relative;
    transform: none !important;
  }
}
</style>
