<template>
  <Layout>
    <div class="chat-wrapper d-lg-flex gap-1 mx-n4 mt-n4 p-1">
      <div class="chat-leftsidebar border">
        <div class="px-4 pt-4 mb-4">
          <div class="d-flex align-items-start">
            <div class="flex-grow-1">
              <h5 class="mb-4">Chats</h5>
            </div>
            <div class="flex-shrink-0">
              <div v-b-tooltip.hover title="Add Contact">
                <BButton type="button" variant="soft-primary" size="sm">
                  <i class="ri-add-line align-bottom"></i>
                </BButton>
              </div>
            </div>
          </div>
          <div class="search-box">
            <input type="text" v-model="searchQuery" class="form-control bg-light border-light" placeholder="Search here..." />
            <i class="ri-search-2-line search-icon"></i>
          </div>
        </div>

        <simplebar class="chat-room-list" data-simplebar>

          <div class="chat-message-list">
            <SimpleBar class="list-unstyled chat-list chat-user-list">
              <li v-for="chat in filteredChats"
                  :key="chat._id"
                  @click="selectChat(chat)"
                  :class="{ active: activeChat && activeChat._id === chat._id }">
                <BLink href="javascript: void(0);">
                  <div class="d-flex align-items-center">
                    <div class="flex-shrink-0 chat-user-img online align-self-center me-2 ms-0">
                      <div class="avatar-xxs">
                        <div class="avatar-title rounded-circle bg-danger userprofile">
                          {{ getChatName(chat).charAt(0) }}
                        </div>
                      </div>
                    </div>
                    <div class="flex-grow-1 overflow-hidden">
                      <p class="text-truncate mb-1">
                        {{ getChatName(chat) }}
                      </p>
                    </div>
                  </div>
                </BLink>
              </li>
            </SimpleBar>
          </div>
        </simplebar>
      </div>
      <!-- Chat view y mensaje: esto lo adaptamos en el siguiente paso -->
      <div class="user-chat w-100 overflow-hidden border">
        <div class="chat-content d-lg-flex">
          <div class="w-100 overflow-hidden position-relative">
            <div class="position-relative">
              <div class="p-3 user-chat-topbar">
                <BRow class="align-items-center">
                  <BCol sm="4" cols="8">
                    <div class="d-flex align-items-center">
                      <div class="flex-shrink-0 chat-user-img online user-own-img align-self-center me-3 ms-0">
                        <img :src="profile ? profile : require('@/assets/images/users/user-dummy-img.jpg')"
                          class="rounded-circle avatar-xs" alt="" />
                        <span class="user-status"></span>
                      </div>
                      <div class="flex-grow-1 overflow-hidden">
                        <h5 class="text-truncate mb-0 fs-16">
                          <BLink class="text-reset username" @click="showOffcanvas = !showOffcanvas">{{ username }}</BLink>
                        </h5>
                      </div>
                    </div>
                  </BCol>
                </BRow>
              </div>
              <!-- Aquí irá la lista de mensajes cuando selecciones un chat -->
              <div class="position-relative" id="users-chat">
                <div class="d-flex justify-content-center align-items-center" style="height: 200px;" v-if="!activeChat">
                  <!-- <span class="text-muted">Selecciona un chat para comenzar</span> -->
                </div>
                <!-- Aquí agregaremos la conversación en el siguiente paso -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script>
import simplebar from 'simplebar-vue';
import Layout from "@/layouts/main.vue";
// import { required, helpers } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import api from "../../router/api"

export default {
  setup() {
    return {
      v$: useVuelidate()
    };
  },
  data() {
    return {
      ws: null,
      chatList: [],
      activeChat: null,
      searchQuery: '',
      showOffcanvas: false,
  
      userId: localStorage.getItem("user_id"),
      username: localStorage.getItem("user_name"),
      profile: require("@/assets/images/users/user-dummy-img.jpg"),
    };
  },
  components: {
    Layout,
    simplebar
  },
  validations: {},
  computed: {
    filteredChats() {
      if (this.searchQuery) {
        const search = this.searchQuery.toLowerCase();
        return this.chatList.filter((chat) =>
          this.getChatName(chat).toLowerCase().includes(search)
        );
      }
      return this.chatList;
    },
  },
  methods: {
    connectWebSocket() {
      if (this.ws) this.ws.close();

      this.ws = new WebSocket(api.chat.ws_chat);
      this.ws.onopen = () => {
        this.ws.send(JSON.stringify({
          event: "list_chats",
          user: this.userId
        }));
      };
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.event === "chats_list") {
          this.chatList = data.chats || [];
        }
        // Aquí después puedes escuchar mensajes nuevos/globales
      };
      this.ws.onerror = () => { /* manejo opcional */ };
      this.ws.onclose = () => { /* reconexión opcional */ };
    },
    selectChat(chat) {
      this.activeChat = chat;
      // Aquí después cargarás los mensajes y abrirás el ws de mensajes
      this.username = this.getChatName(chat);
    },
    getChatName(chat) {
      // Si tienes los nombres de los usuarios, cámbialo. Aquí muestra el ID "opuesto"
      // Por ahora, asume que 'participants' son ObjectIDs, regresa el otro usuario
      if (chat && chat.participants && Array.isArray(chat.participants)) {
        return chat.participants.find((p) => p !== this.userId) || "Chat";
      }
      return "Chat";
    }
  },
  mounted() {
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.ws) this.ws.close();
  },
};
</script>
