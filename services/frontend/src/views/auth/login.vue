<template>
  <div class="auth-page-wrapper pt-5">
    <div class="auth-one-bg" id="auth-particles">
      <div class="bg-overlay"></div>
      <div class="shape">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
          <path
            d="M 0,36 C 144,53.6 432,123.2 720,124 C 1008,124.8 1296,56.8 1440,40L1440 140L0 140z"
          />
        </svg>
      </div>
    </div>

    <BContainer>
      <BRow class="justify-content-center">
        <BCol md="8" lg="6" xl="5" class="w-100" style="max-width: 400px">
          <BCard no-body class="mt-4 scrollable-card">
            <BCardBody class="p-4">
              <div class="text-center mt-2">
                <h5 class="text-primary mb-4">Inicio de sesión</h5>
              </div>

              <div class="p-2 mt-4">
                <b-alert
                  v-model="showError"
                  variant="danger"
                  class="mt-3"
                  dismissible
                >
                  {{ authError }}
                </b-alert>

                <form @submit.prevent="signinapi">
                  <!-- Correo institucional -->
                  <div class="mb-3 position-relative">
                    <label for="email" class="form-label"
                      >Correo institucional</label
                    >
                    <input
                      v-model="email"
                      required
                      type="email"
                      class="form-control pr-5"
                      id="email"
                      placeholder="Correo institucional"
                      autocomplete="username"
                    />
                    <!-- Icono de sobre -->
                    <font-awesome-icon
                      :icon="['fas', 'envelope']"
                      class="position-absolute"
                      style="
                        top: 38px;
                        right: 16px;
                        pointer-events: none;
                        color: #aaa;
                      "
                    />
                  </div>

                  <!-- Contraseña -->
                  <div class="mb-2 position-relative">
                    <label for="password-input" class="form-label"
                      >Contraseña</label
                    >
                    <input
                      v-model="password"
                      required
                      type="password"
                      class="form-control pr-5"
                      id="password-input"
                      placeholder="Contraseña"
                      autocomplete="current-password"
                    />
                    <!-- Icono de candado -->
                    <font-awesome-icon
                      :icon="['fas', 'lock']"
                      class="position-absolute"
                      style="
                        top: 38px;
                        right: 16px;
                        pointer-events: none;
                        color: #aaa;
                      "
                    />
                  </div>

                  <!-- Olvidé mi contraseña -->
                  <div class="mb-3 text-end">
                    <router-link to="/reset-password" class="text-muted small">
                      Olvidé mi contraseña
                    </router-link>
                  </div>
                </form>
              </div>

              <div class="row pt-2">
                <div class="col-12">
                  <BButton
                    variant="success"
                    class="w-100"
                    type="button"
                    @click="signinapi"
                    :disabled="processing"
                  >
                    {{ processing ? "Cargando..." : "Iniciar sesión" }}
                  </BButton>
                </div>
                <div class="col-12 mt-2">
                  <BButton
                    variant="info"
                    class="w-100"
                    type="button"
                    @click="register"
                    :disabled="processing"
                  >
                    {{ processing ? "Cargando..." : "Registrarse" }}
                  </BButton>
                </div>
              </div>
            </BCardBody>
          </BCard>
        </BCol>
      </BRow>
    </BContainer>
  </div>
</template>

<script>
import axios from "axios";
import api from "@/router/api";

export default {
  data: () => ({
    email: "",
    password: "",
    authError: "",
    showError: false,
    processing: false,
  }),
  methods: {
    async signinapi() {
      if (!this.email) {
        this.authError = "El correo electrónico es requerido";
        this.showError = true;
        return;
      }
      if (!this.password) {
        this.authError = "La contraseña es requerida";
        this.showError = true;
        return;
      }

      this.processing = true;
      try {
        const { data } = await axios.post(api.users.login, {
          email: this.email,
          password: this.password,
        });

        if (data.status_code === 200) {
          const { access, refresh, user_name, user_id, email } = data.data;
          localStorage.setItem("access", access);
          localStorage.setItem("refresh", refresh);
          localStorage.setItem("user_name", user_name);
          localStorage.setItem("user_email", email);
          localStorage.setItem("user_id", user_id);
          this.$router.push({ name: "default" });
        } else {
          this.authError =
            data.non_field_errors || data.message || "Credenciales inválidas";
          this.showError = true;
        }
      } catch (err) {
        this.authError =
          err.response?.data?.non_field_errors ||
          err.response?.data?.message ||
          "Error de conexión";
        this.showError = true;
      } finally {
        this.processing = false;
      }
    },
    register() {
      this.$router.push({ name: "register" });
    },
  },
  async mounted() {
    const endpoints = [
      api.users.user,
      api.community.list,
      api.publication.publish,
      api.chat.ws_chat,
    ];

    const promesas = endpoints.map((url) =>
      axios
        .get(url)
        .then((res) => {
          console.log(`✅ ${url} → ${res.status}`);
        })
        .catch((err) => {
          console.warn(`❌ ${url} → ${err.message}`);
        })
    );

    await Promise.all(promesas);
    console.log("✔️ Wake‐up requests enviados desde Login.vue");
  },
};
</script>

<style scoped>
.scrollable-card {
  max-height: 80vh; /* Altura máxima relativa a la pantalla */
  overflow-y: auto;
}
</style>
