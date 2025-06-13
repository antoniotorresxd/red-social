<template>
  <Layout>
    <div class="chat-wrapper d-lg-flex gap-1 mx-n4 mt-n4 p-1">
      <!-- Sidebar de chats -->
      <div class="chat-leftsidebar border">
        <div class="px-4 pt-4 mb-4">
          <div class="d-flex align-items-start">
            <div class="flex-grow-1">
              <h5 class="mb-4">Chats</h5>
            </div>
            <div class="flex-shrink-0">
              <div v-b-tooltip.hover title="Agregar chat">
                <BButton
                  type="button"
                  variant="soft-primary"
                  size="sm"
                  @click="openCreateChat"
                >
                  <i class="ri-add-line align-bottom"></i>
                </BButton>
              </div>
            </div>
          </div>
          <div class="search-box">
            <input
              type="text"
              v-model="searchQuery"
              class="form-control bg-light border-light"
              placeholder="Search here..."
            />
            <i class="ri-search-2-line search-icon"></i>
          </div>
        </div>

        <simplebar class="chat-room-list" data-simplebar>
          <div class="chat-message-list">
            <SimpleBar class="list-unstyled chat-list chat-user-list">
              <li
                v-for="chat in filteredChats"
                :key="chat._id"
                @click="selectChat(chat)"
                :class="{ active: activeChat && activeChat._id === chat._id }"
              >
                <BLink href="javascript: void(0);">
                  <div class="d-flex align-items-center">
                    <div
                      class="flex-shrink-0 chat-user-img online align-self-center me-2 ms-0"
                    >
                      <div class="avatar-xxs">
                        <div
                          class="avatar-title rounded-circle bg-primary userprofile"
                        >
                          {{ getChatName(chat).charAt(0).toUpperCase() }}
                        </div>
                      </div>
                    </div>
                    <div class="flex-grow-1 overflow-hidden">
                      <p class="text-truncate mb-1">{{ getChatName(chat) }}</p>
                    </div>
                  </div>
                </BLink>
              </li>
            </SimpleBar>
          </div>
        </simplebar>
      </div>

      <!-- Área de chat principal -->
      <div
        style="background: #fff"
        class="user-chat w-100 overflow-hidden border"
        :class="{ 'user-chat-show': activeChat || showCreateChat }"
      >
        <div class="chat-content d-lg-flex">
          <div class="w-100 overflow-hidden position-relative">
            <!-- Formulario crear chat -->

            <div v-if="showCreateChat">
              <!-- Header idéntico al de conversación -->
              <div class="p-3 user-chat-topbar d-flex align-items-center">
                <BLink
                  href="javascript:void(0);"
                  class="user-chat-remove fs-18 p-1 d-block d-lg-none"
                  @click="showCreateChat = false"
                >
                  <i class="ri-arrow-left-s-line align-bottom"></i>
                </BLink>

                <h5 class="text-left flex-grow-1 mb-0">Agregar chat</h5>
              </div>

              <!-- Card de formulario, sin padding-top extra -->
              <div class="d-flex justify-content-start align-items-start p-3">
                <div
                  class="card shadow-sm"
                  style="max-width: 400px; width: 100%"
                >
                  <div class="card-body">
                    <div class="mb-3">
                      <label class="form-label">Correo institucional</label>
                      <input
                        v-model="chatEmail"
                        type="email"
                        class="form-control"
                        placeholder="usuario@alumno.ipn.mx"
                      />
                    </div>
                    <div class="d-flex justify-content-center">
                      <BButton variant="primary" @click="handleCreateChat">
                        Buscar
                      </BButton>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Chat activo -->
            <div v-else-if="activeChat" class="position-relative">
              <div class="p-3 user-chat-topbar">
                <BRow class="align-items-center">
                  <BCol sm="4" cols="8">
                    <div class="d-flex align-items-center">
                      <div class="flex-shrink-0 d-block d-lg-none me-3">
                        <BLink
                          href="javascript: void(0);"
                          class="user-chat-remove fs-18 p-1"
                          @click="deselectChat"
                        >
                          <i class="ri-arrow-left-s-line align-bottom"></i>
                        </BLink>
                      </div>
                      <div class="flex-grow-1 overflow-hidden">
                        <div class="d-flex align-items-center">
                          <div
                            class="flex-shrink-0 chat-user-img online user-own-img align-self-center me-3 ms-0"
                          >
                            <div
                              class="avatar-xs rounded-circle bg-primary d-flex align-items-center justify-content-center"
                            >
                              <span class="text-white">{{
                                username.charAt(0).toUpperCase()
                              }}</span>
                            </div>
                            <span class="user-status"></span>
                          </div>
                          <div class="flex-grow-1 overflow-hidden">
                            <h5 class="text-truncate mb-0 fs-16">
                              <BLink
                                class="text-reset username"
                                
                              >
                                {{ username }}
                              </BLink>
                            </h5>
                            <p
                              class="text-truncate text-muted fs-14 mb-0 userStatus"
                            >
                              <small></small>
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </BCol>
                  <BCol sm="8" cols="4"> </BCol>
                </BRow>
              </div>

              <div class="position-relative" id="users-chat">
                <simplebar
                  class="chat-conversation p-3 p-lg-4"
                  id="chat-conversation"
                  data-simplebar
                  ref="chatContainer"
                >
                  <ul class="list-unstyled chat-conversation-list">
                    <li
                      v-for="data of resultQuery"
                      :key="data._id"
                      :class="{
                        right: `${data.align}` === 'right',
                        left: `${data.align}` !== 'right',
                      }"
                      class="chat-list"
                    >
                      <div class="conversation-list">
                        <div class="chat-avatar" v-if="data.align !== 'right'">
                          <div
                            class="avatar-xs rounded-circle bg-secondary d-flex align-items-center justify-content-center"
                          >
                            <span class="text-white">{{
                              data.name
                                ? data.name.charAt(0).toUpperCase()
                                : "U"
                            }}</span>
                          </div>
                        </div>
                        <div class="user-chat-content pt-1">
                          <div class="ctext-wrap">
                            <div class="ctext-wrap-content">
                              <p class="mb-0 ctext-content">
                                {{ data.message }}
                              </p>
                            </div>
                          </div>
                          <div class="conversation-name">
                            <small class="text-muted time">{{
                              data.time
                            }}</small>
                          </div>
                        </div>
                      </div>
                    </li>
                  </ul>
                </simplebar>

                <div
                  class="alert alert-warning alert-dismissible copyclipboard-alert px-4 fade show"
                  id="copyClipBoard"
                  role="alert"
                  style="display: none"
                >
                  Message copied
                </div>
              </div>

              <div class="chat-input-section p-3 p-lg-4">
                <form @submit.prevent="formSubmit">
                  <BRow class="g-0 align-items-center">
                    <BCol cols="auto">
                      <div class="chat-input-links me-2">
                        <div class="links-list-item"></div>
                      </div>
                    </BCol>
                    <BCol>
                      <div class="chat-input-feedback">
                        Please Enter a Message
                      </div>

                      <input
                        type="text"
                        v-model="form.message"
                        class="form-control chat-input bg-light border-light fs-13"
                        placeholder="Enviar mensaje..."
                        :class="{
                          'is-invalid': submitted && v$.form.message.$error,
                        }"
                      />
                      <div
                        v-if="submitted && v$.form.message.$error"
                        class="invalid-feedback"
                      >
                        <span v-if="v$.form.message.required.$message">
                          {{ v$.form.message.required.$message }}
                        </span>
                      </div>
                    </BCol>
                    <BCol cols="auto">
                      <div class="chat-input-links ms-2">
                        <div class="links-list-item">
                          <BButton
                            variant="success"
                            type="submit"
                            class="chat-send fs-13"
                          >
                            <i class="ri-send-plane-2-fill align-bottom"></i>
                          </BButton>
                        </div>
                      </div>
                    </BCol>
                  </BRow>
                </form>
              </div>

              <div class="replyCard">
                <BCard no-body class="mb-0">
                  <BCardBody class="py-3">
                    <div
                      class="replymessage-block mb-0 d-flex align-items-start"
                    >
                      <div class="flex-grow-1">
                        <h5 class="conversation-name"></h5>
                        <p class="mb-0"></p>
                      </div>
                      <div class="flex-shrink-0">
                        <BButton
                          type="button"
                          variant="link"
                          size="sm"
                          id="close_toggle"
                          class="mt-n2 me-n3 fs-18"
                        >
                          <i class="bx bx-x align-middle"></i>
                        </BButton>
                      </div>
                    </div>
                  </BCardBody>
                </BCard>
              </div>
            </div>

            <!-- Estado por defecto -->
            <div
              v-else
              class="d-flex justify-content-center align-items-center h-100"
            >
              <div class="text-center">
                <!-- <h5 class="text-muted">Selecciona un chat para comenzar</h5> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Offcanvas de información del usuario -->
    <BOffcanvas
      placement="end"
      v-model="showOffcanvas"
      body-class="border-0 p-0 overflow-hidden"
      header-class="border-bottom"
    >
      <div class="offcanvas-body profile-offcanvas p-0">
        <div class="team-cover">
          <img src="@/assets/images/small/img-9.jpg" alt="" class="img-fluid" />
        </div>
        <div class="p-1 pb-4 pt-0">
          <div class="team-settings">
            <div class="row g-0">
              <div class="col"></div>
              <div class="col-auto">
                <div class="user-chat-nav d-flex">
                  <button
                    type="button"
                    class="btn nav-btn favourite-btn active"
                  >
                    <i class="ri-star-fill"></i>
                  </button>

                  <div class="dropdown">
                    <BLink
                      class="btn nav-btn"
                      href="javascript:void(0);"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      <i class="ri-more-2-fill"></i>
                    </BLink>
                    <ul class="dropdown-menu dropdown-menu-end">
                      <li>
                        <BLink class="dropdown-item" href="javascript:void(0);"
                          ><i
                            class="ri-inbox-archive-line align-bottom text-muted me-2"
                          ></i
                          >Archive</BLink
                        >
                      </li>
                      <li>
                        <BLink class="dropdown-item" href="javascript:void(0);"
                          ><i
                            class="ri-mic-off-line align-bottom text-muted me-2"
                          ></i
                          >Muted</BLink
                        >
                      </li>
                      <li>
                        <BLink class="dropdown-item" href="javascript:void(0);"
                          ><i
                            class="ri-delete-bin-5-line align-bottom text-muted me-2"
                          ></i
                          >Delete</BLink
                        >
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="p-3 text-center">
          <div
            class="avatar-lg img-thumbnail rounded-circle mx-auto profile-img bg-primary d-flex align-items-center justify-content-center"
          >
            <span class="text-white fs-4">{{
              username.charAt(0).toUpperCase()
            }}</span>
          </div>
          <div class="mt-3">
            <h5 class="fs-16 mb-1">
              <BLink href="javascript:void(0);" class="link-primary username">
                {{ username }}</BLink
              >
            </h5>
            <p class="text-muted">
              <i
                class="ri-checkbox-blank-circle-fill me-1 align-bottom text-success"
              ></i
              >Online
            </p>
          </div>

          <div class="d-flex gap-2 justify-content-center">
            <button
              type="button"
              class="btn avatar-xs p-0"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Message"
            >
              <span class="avatar-title rounded bg-light text-body">
                <i class="ri-question-answer-line"></i>
              </span>
            </button>

            <button
              type="button"
              class="btn avatar-xs p-0"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Favourite"
            >
              <span class="avatar-title rounded bg-light text-body">
                <i class="ri-star-line"></i>
              </span>
            </button>

            <button
              type="button"
              class="btn avatar-xs p-0"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Phone"
            >
              <span class="avatar-title rounded bg-light text-body">
                <i class="ri-phone-line"></i>
              </span>
            </button>

            <div class="dropdown">
              <button
                class="btn avatar-xs p-0"
                type="button"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                <span class="avatar-title bg-light text-body rounded">
                  <i class="ri-more-fill"></i>
                </span>
              </button>

              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <BLink class="dropdown-item" href="javascript:void(0);"
                    ><i
                      class="ri-inbox-archive-line align-bottom text-muted me-2"
                    ></i
                    >Archive</BLink
                  >
                </li>
                <li>
                  <BLink class="dropdown-item" href="javascript:void(0);"
                    ><i class="ri-mic-off-line align-bottom text-muted me-2"></i
                    >Muted</BLink
                  >
                </li>
                <li>
                  <BLink class="dropdown-item" href="javascript:void(0);"
                    ><i
                      class="ri-delete-bin-5-line align-bottom text-muted me-2"
                    ></i
                    >Delete</BLink
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="border-top border-top-dashed p-3">
          <h5 class="fs-15 mb-3">Personal Details</h5>
          <div class="mb-3">
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">Number</p>
            <h6>+(256) 2451 8974</h6>
          </div>
          <div class="mb-3">
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">Email</p>
            <h6>{{ userEmail }}</h6>
          </div>
          <div>
            <p class="text-muted text-uppercase fw-medium fs-12 mb-1">
              Location
            </p>
            <h6 class="mb-0">California, USA</h6>
          </div>
        </div>
      </div>
    </BOffcanvas>
  </Layout>
</template>

<script>
import simplebar from "simplebar-vue";

import { required, helpers } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";

import Layout from "@/layouts/main.vue";
import api from "@/router/api";
import axios from "axios";

export default {
  setup() {
    return {
      v$: useVuelidate(),
    };
  },

  data() {
    return {
      // WebSocket y datos de chat
      ws: null,
      chatList: [],
      activeChat: null,
      messages: [],
      wsReady: false,
      userId: localStorage.getItem("user_id"),
      userEmail: localStorage.getItem("user_email"),

      // UI estado
      searchQuery: "",
      showOffcanvas: false,
      showCreateChat: false,
      chatEmail: "",
      submitted: false,
      form: {
        message: "",
      },
      username: "Steven Franklin",
      profile: require("@/assets/images/users/avatar-2.jpg"),
    };
  },

  components: {
    Layout,
    simplebar,
  },

  validations: {
    form: {
      message: {
        required: helpers.withMessage("Message is required", required),
      },
    },
  },

  computed: {
    filteredChats() {
      const query = this.searchQuery.toLowerCase();
      return query
        ? this.chatList.filter((c) =>
            this.getChatName(c).toLowerCase().includes(query)
          )
        : this.chatList;
    },

    resultQuery() {
      return this.messages;
    },
  },

  methods: {
    // Métodos de WebSocket
    initializeWebSocket() {
      try {
        this.ws = new WebSocket(api.chat.ws_chat);

        this.ws.onopen = () => {
          this.wsReady = true;
          this.sendWebSocketMessage({
            event: "list_chats",
            user: this.userId,
            token: localStorage.getItem("access"),
          });
        };

        this.ws.onmessage = ({ data }) => {
          const msg = JSON.parse(data);
          this.handleWebSocketMessage(msg);
        };

        this.ws.onclose = () => {
          this.wsReady = false;
          // Intentar reconexión después de 5 segundos
          setTimeout(this.initializeWebSocket, 5000);
        };

        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
          this.wsReady = false;
        };
      } catch (error) {
        console.error("Error al inicializar WebSocket:", error);
        setTimeout(this.initializeWebSocket, 5000);
      }
    },

    handleWebSocketMessage(msg) {
      switch (msg.event) {
        case "chats_list": {
          this.chatList = msg.chats || [];
          break;
        }
        case "chat_created": {
          let newChat = this.chatList.find((c) => c._id === msg.room_id);

          if (!newChat) {
            newChat = {
              _id: msg.room_id,
              participants: msg.participants,
            };
            this.chatList.unshift(newChat);
          }

          this.$nextTick(() => {
            this.selectChat(newChat);
            this.showCreateChat = false;
          });
          break;
        }

        case "chat_exists": {
          this.activeChat =
            this.chatList.find((c) => c._id === msg.room_id) || null;
          if (this.activeChat) {
            this.username = this.getChatName(this.activeChat);
            this.messages = [];
          }
          this.showCreateChat = false;
          break;
        }
        case "new_message": {
          if (this.activeChat && msg.room_id === this.activeChat._id) {
            this.messages.push({
              _id: Date.now().toString(),
              sender_id: msg.sender,
              message: msg.message,
              timestamp: msg.timestamp,
              align: msg.sender === this.userId ? "right" : "left",
              name:
                msg.sender === this.userId
                  ? "Tú"
                  : this.getChatName(this.activeChat),
              time: this.formatTimestamp(msg.timestamp),
            });
            this.$nextTick(() => this.scrollToBottom());
          }
          break;
        }
        case "chat_history": {
          if (
            this.activeChat &&
            msg.room_id === this.activeChat._id &&
            Array.isArray(msg.messages)
          ) {
            this.messages = msg.messages.map((m) => ({
              _id: m._id,
              sender_id: m.sender_id,
              message: m.message,
              timestamp: m.timestamp,
              align: m.sender_id === this.userId ? "right" : "left",
              name:
                m.sender_id === this.userId
                  ? "Tú"
                  : this.getChatName(this.activeChat),
              time: this.formatTimestamp(m.timestamp),
            }));
          } else {
            this.messages = [];
          }
          this.$nextTick(() => this.scrollToBottom());
          break;
        }
      }
    },

    sendWebSocketMessage(payload) {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify(payload));
      } else {
        console.warn("Conexión de chat no lista. Intenta de nuevo.");
        this.initializeWebSocket();
      }
    },

    async getUserIdByEmail(email) {
      try {
        const { data } = await axios.get(api.users.find_by_email, {
          params: { email },
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        });
        return data.data?.id || null;
      } catch (error) {
        console.error("Error al buscar usuario:", error);
        return null;
      }
    },

    async handleCreateChat() {
      if (!this.chatEmail) {
        alert("Ingresa un correo válido");
        return;
      }

      const targetUserId = await this.getUserIdByEmail(this.chatEmail);
      if (!targetUserId) {
        alert("Usuario no encontrado");
        return;
      }

      this.sendWebSocketMessage({
        event: "create_chat",
        participants: [this.userId, targetUserId.toString()],
        token: localStorage.getItem("access"),
      });

      this.chatEmail = "";
    },

    // Métodos de UI
    openCreateChat() {
      this.showCreateChat = true;
      this.activeChat = null;
      this.messages = [];
    },

    selectChat(chat) {
      this.activeChat = chat;
      this.messages = [];
      this.username = this.getChatName(chat);
      this.sendWebSocketMessage({
        event: "join_chat",
        room_id: chat._id,
      });
      this.showCreateChat = false;
    },

    deselectChat() {
      this.activeChat = null;
      this.messages = [];
    },

    getChatName(chat) {
      const other = (chat.participants || []).find((e) => e !== this.userEmail);
      return other || "Chat";
    },

    formatTimestamp(ts) {
      return new Date(ts).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    scrollToBottom() {
      this.$nextTick(() => {
        if (!this.$refs.chatContainer) return;

        try {
          if (
            this.$refs.chatContainer.simpleBar &&
            this.$refs.chatContainer.simpleBar.getScrollElement
          ) {
            const scrollElement =
              this.$refs.chatContainer.simpleBar.getScrollElement();
            scrollElement.scrollTop = scrollElement.scrollHeight;
            return;
          }

          const contentWrapper = this.$refs.chatContainer.$el?.querySelector(
            ".simplebar-content-wrapper"
          );
          if (contentWrapper) {
            contentWrapper.scrollTop = contentWrapper.scrollHeight;
            return;
          }

          const scrollContent = this.$refs.chatContainer.$el?.querySelector(
            ".simplebar-scroll-content"
          );
          if (scrollContent) {
            scrollContent.scrollTop = scrollContent.scrollHeight;
            return;
          }

          const rootElement =
            this.$refs.chatContainer.$el || this.$refs.chatContainer;
          if (rootElement) {
            rootElement.scrollTop = rootElement.scrollHeight;
          }
        } catch (error) {
          console.warn("Error al hacer scroll:", error);

          const chatList = document.querySelector(".chat-conversation-list");
          if (chatList) {
            chatList.scrollTop = chatList.scrollHeight;
          }
        }
      });
    },

    formSubmit() {
      this.submitted = true;
      this.v$.$touch();

      if (this.v$.$invalid) {
        return;
      }

      const message = this.form.message.trim();
      if (!message || !this.activeChat) return;

      if (this.ws?.readyState !== WebSocket.OPEN) {
        this.$bvToast.toast("Conexión de chat no disponible", {
          title: "Error",
          variant: "danger",
          solid: true,
        });
        return;
      }

      const payload = {
        event: "submit_message",
        room_id: this.activeChat._id,
        sender: this.userId,
        message: message,
      };

      this.ws.send(JSON.stringify(payload));
      this.form.message = "";
      this.submitted = false;
      this.scrollToBottom();
    },
  },

  mounted() {
    this.initializeWebSocket();
  },

  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  },
};
</script>

<style scoped>
.user-chat-show {
  display: block !important;
}

.chat-user-list li.active {
  background-color: rgba(85, 110, 230, 0.1);
}

.chat-conversation-list .right .conversation-list {
  margin-right: 16px;
}

.chat-conversation-list .left .conversation-list {
  margin-left: 16px;
}

.copyclipboard-alert {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 999;
  display: none;
}
</style>