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
            <input type="text" class="form-control bg-light border-light" placeholder="Search here..." />
            <i class="ri-search-2-line search-icon"></i>
          </div>
        </div>

        <simplebar class="chat-room-list" data-simplebar>
          <div class="d-flex align-items-center px-4 mb-2">
            <div class="flex-grow-1">
              <h4 class="mb-0 fs-11 text-muted text-uppercase">
                Direct Messages
              </h4>
            </div>
            <div class="flex-shrink-0">
              <div v-b-tooltip.hover title="New Message">
                <BButton type="button" variant="soft-primary" size="sm">
                  <i class="ri-add-line align-bottom"></i>
                </BButton>
              </div>
            </div>
          </div>

          <div class="chat-message-list">
            <SimpleBar class="list-unstyled chat-list chat-user-list">
              <li class v-for="data of chatData" :key="data.id" @click="chatUsername(data.name, data.image)"
                :class="{ active: username == data.name }">
                <BLink href="javascript: void(0);">
                  <div class="d-flex align-items-center">
                    <div class="flex-shrink-0 chat-user-img online align-self-center me-2 ms-0">
                      <div class="avatar-xxs" v-if="data.image">
                        <img :src="`${data.image}`" class="rounded-circle img-fluid userprofile" alt />
                      </div>
                      <div class="avatar-xxs" v-if="!data.image">
                        <div class="avatar-title rounded-circle bg-danger userprofile">
                          {{ data.name.charAt(0) }}
                        </div>
                      </div>
                    </div>
                    <div class="flex-grow-1 overflow-hidden">
                      <p class="text-truncate mb-1">
                        {{ data.name }}
                      </p>
                    </div>

                    <div class="flex-shrink-0">
                      <BBadge variant="dark-subtle" class="bg-dark-subtle text-body rounded p-1">{{ data.time
                      }}</BBadge>
                    </div>
                  </div>
                </BLink>
              </li>
            </SimpleBar>
          </div>

        </simplebar>
      </div>
      <div class="user-chat w-100 overflow-hidden border">
        <div class="chat-content d-lg-flex">
          <div class="w-100 overflow-hidden position-relative">
            <div class="position-relative">
              <div class="p-3 user-chat-topbar">
                <BRow class="align-items-center">
                  <BCol sm="4" cols="8">
                    <div class="d-flex align-items-center">
                      <div class="flex-shrink-0 d-block d-lg-none me-3">
                        <BLink href="javascript: void(0);" class="user-chat-remove fs-18 p-1"><i
                            class="ri-arrow-left-s-line align-bottom"></i></BLink>
                      </div>
                      <div class="flex-grow-1 overflow-hidden">
                        <div class="d-flex align-items-center">
                          <div class="flex-shrink-0 chat-user-img online user-own-img align-self-center me-3 ms-0">
                            <img :src="profile ? profile : require('@/assets/images/users/user-dummy-img.jpg')"
                              class="rounded-circle avatar-xs" alt="" />
                            <span class="user-status"></span>
                          </div>
                          <div class="flex-grow-1 overflow-hidden">
                            <h5 class="text-truncate mb-0 fs-16">
                              <BLink class="text-reset username" @click="showOffcanvas = !showOffcanvas">{{ username }}
                              </BLink>
                            </h5>
                          </div>
                        </div>
                      </div>
                    </div>
                  </BCol>
                </BRow>
              </div>

              <div class="position-relative" id="users-chat">
                <simplebar class="chat-conversation p-3 p-lg-4" id="chat-conversation" data-simplebar ref="current">
                  <ul class="list-unstyled chat-conversation-list">
                    <li v-for="data of resultQuery" :key="data.message" :class="{
                      right: `${data.align}` === 'right',
                      left: `${data.align}` !== 'right',
                    }" class="chat-list">
                      <div class="conversation-list">
                        <div class="chat-avatar" v-if="data.align !== 'right'">
                          <img :src="profile ? profile : require('@/assets/images/users/user-dummy-img.jpg')" alt="" />
                        </div>
                        <div class="user-chat-content">
                          <div class="ctext-wrap">
                            <div class="ctext-wrap-content">
                              <p class="mb-0 ctext-content">
                                {{ data.message }}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </li>
                  </ul>

                </simplebar>
                <div class="alert alert-warning alert-dismissible copyclipboard-alert px-4 fade show" id="copyClipBoard"
                  role="alert">
                  Message copied
                </div>
              </div>


              <div class="chat-input-section p-3 p-lg-4">
                <form @submit.prevent="formSubmit">
                  <BRow class="g-0 align-items-center">
                    <BCol>
                      <div class="chat-input-feedback">
                        Please Enter a Message
                      </div>

                      <input type="text" v-model="form.message"
                        class="form-control chat-input bg-light border-light fs-13" placeholder="Enter Message..."
                        :class="{
                          'is-invalid': submitted && v$.form.message.$error,
                        }" />
                      <div v-if="submitted && v$.form.message.$error" class="invalid-feedback">
                        <span v-if="v$.form.message.required.$message">{{
                          v$.form.message.required.$message
                        }}</span>
                      </div>
                    </BCol>
                    <BCol cols="auto">
                      <div class="chat-input-links ms-2">
                        <div class="links-list-item">
                          <BButton variant="success" type="submit" class="chat-send fs-13">
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
                    <div class="replymessage-block mb-0 d-flex align-items-start">
                      <div class="flex-grow-1">
                        <h5 class="conversation-name"></h5>
                        <p class="mb-0"></p>
                      </div>
                      <div class="flex-shrink-0">
                        <BButton type="button" variant="link" size="sm" id="close_toggle" class="mt-n2 me-n3 fs-18">
                          <i class="bx bx-x align-middle"></i>
                        </BButton>
                      </div>
                    </div>
                  </BCardBody>
                </BCard>
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

import {
  required,
  helpers
} from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";

import Layout from "@/layouts/main.vue";

import {
  chatData,
  chatMessagesData
} from "@/common/data";

export default {
  setup() {
    return {
      v$: useVuelidate()
    };
  },

  data() {
    return {
      searchQuery: '',
      showOffcanvas: false,
      chatData: chatData,
      chatMessagesData: chatMessagesData,
      submitted: false,
      form: {
        message: "",
      },
      username: "Steven Franklin",
      profile: require("@/assets/images/users/avatar-2.jpg")
    };
  },
  components: {
    Layout,
    simplebar
  },
  validations: {
    form: {
      message: {
        required: helpers.withMessage("Message is required", required),
      },
    },
  },
  methods: {
    /**
     * Get the name of user
     */
    scrollToBottom(id) {
      setTimeout(function () {
        var simpleBar = document.getElementById(id).querySelector(
          "#chat-conversation .simplebar-content-wrapper") ?
          document.getElementById(id).querySelector(
            "#chat-conversation .simplebar-content-wrapper") : '';
        var offsetHeight = document.getElementsByClassName("chat-conversation-list")[0] ?
          document.getElementById(id).getElementsByClassName("chat-conversation-list")[0]
            .scrollHeight - window.innerHeight + 600 : 0;
        if (simpleBar && offsetHeight)
          simpleBar.scrollTo({
            top: offsetHeight,
            behavior: "smooth"
          });
      }, 300);
    },
    chatUsername(name, image) {
      this.username = name;
      this.profile = image;
      this.usermessage = "Hello";
      this.chatMessagesData = [];
      const currentDate = new Date();
      const hours = (currentDate.getHours() < 10 ? "0" : "") + currentDate.getHours();
      const minutes = (currentDate.getMinutes() < 10 ? "0" : "") + currentDate.getMinutes();

      this.chatMessagesData.push({
        name: this.username,
        message: this.usermessage,
        time: hours + ":" + minutes,
      });
    },

    /**
     * Char form Submit
     */
    formSubmit() {
      this.submitted = true;

      // stop here if form is invalid
      this.v$.$touch();

      if (this.v$.$invalid) {
        return;
      } else {
        const message = this.form.message;
        const currentDate = new Date();
        const hours = (currentDate.getHours() < 10 ? "0" : "") + currentDate.getHours();
        const minutes = (currentDate.getMinutes() < 10 ? "0" : "") + currentDate.getMinutes();
        this.chatMessagesData.push({
          align: "right",
          name: "Henry Wells",
          message,
          time: hours + ":" + minutes,
        });
        var currentChatId = "users-chat";
        this.scrollToBottom(currentChatId);
      }
      this.submitted = false;
      this.form = {};
    },
  },
  mounted() {
    var currentChatId = "users-chat";
    this.scrollToBottom(currentChatId);
    document.getElementById('copyClipBoard').style.display = 'none';
    var userChatElement = document.querySelectorAll(".user-chat");
    document.querySelectorAll(".chat-user-list li a").forEach(function (item) {
      item.addEventListener("click", function () {
        userChatElement.forEach(function (elm) {
          elm.classList.add("user-chat-show");
        });

        // chat user list link active
        var chatUserList = document.querySelector(".chat-user-list li.active");
        if (chatUserList) chatUserList.classList.remove("active");
        this.parentNode.classList.add("active");
      });
    });

    // user-chat-remove
    document.querySelectorAll(".user-chat-remove").forEach(function (item) {
      item.addEventListener("click", function () {
        userChatElement.forEach(function (elm) {
          elm.classList.remove("user-chat-show");
        });
      });
    });
  },
  computed: {
    resultQuery() {
      if (this.searchQuery) {
        const search = this.searchQuery.toLowerCase();
        return this.chatMessagesData.filter((data) => {
          return (
            data.message.toLowerCase().includes(search)
          );
        });
      } else {
        return this.chatMessagesData;
      }
    },
  }
};
</script>