<template>
  <div class="auth-page-wrapper pt-5">
    <div class="auth-one-bg" id="auth-particles">
      <div class="bg-overlay"></div>
      <div class="shape">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
          <path d="M 0,36 C 144,53.6 432,123.2 720,124 C 1008,124.8 1296,56.8 1440,40L1440 140L0 140z" />
        </svg>
      </div>
    </div>

    <BContainer>
      <BRow class="justify-content-center">
        <BCol md="8" lg="6" xl="5" class="w-100" style="max-width: 400px;">
          <BCard no-body class="mt-4 scrollable-card">
            <BCardBody class="p-4">
              <div class="text-center mt-2">
                <h5 class="text-primary">Registrarse</h5>
              </div>

              <div class="p-2 mt-4">
                <b-alert v-model="showError" variant="danger" class="mt-3" dismissible>
                  {{ authError }}
                </b-alert>

                <form>

                  <div class="mb-3">
                    <label for="name" class="form-label">Nombre Completo</label>
                    <input v-model="name" required type="text" class="form-control" id="name"
                      placeholder="Nombre Completo" />
                  </div>

                  <div class="mb-3">
                    <label for="email" class="form-label">Correo institucional</label>
                    <input v-model="email" required type="email" class="form-control" id="email"
                      placeholder="Dirección de correo electrónico" />
                  </div>

                  <div class="mb-3">
                    <label for="birthdate" class="form-label">Fecha de nacimiento</label>
                    <input v-model="birthdate" required type="date" class="form-control" id="birthdate"
                      placeholder="Fecha de nacimiento" />
                  </div>

                  <div class="mb-3">
                    <label for="password-input" class="form-label">Contraseña</label>
                    <div class="position-relative auth-pass-inputgroup mb-1">
                      <input v-model="password" required type="password" class="form-control pe-5" id="password-input"
                        placeholder="Contraseña" />
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="password2" class="form-label">Validación de contraseña</label>
                    <div class="position-relative auth-pass-inputgroup mb-1">
                      <input v-model="password2" required type="password" class="form-control pe-5" id="password2"
                        placeholder="Confirmar contraseña" />
                    </div>
                  </div>
                </form>
              </div>

              <div class="row ">
                <div class="col-12">
                  <BButton variant="info" class="w-100" type="button" @click="registerapi" :disabled="processing">
                    {{ processing ? "Cargando..." : "Registrarse" }}
                  </BButton>
                </div>
                <div class="col-12 pt-2">
                  <BButton variant="success" class="w-100" type="button" @click="redirectLogin" :disabled="processing">
                    {{ processing ? "Cargando..." : "Iniciar Sesion" }}
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
    name: "",
    email: "",
    birthdate: "",
    password: "",
    password2 : "",
    authError: "",
    showError: false,
    processing: false,
  }),
  methods: {
    redirectLogin(){
      this.$router.push({ name: "login" });
    },
    async registerapi() {
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
      const payload = {
        "name": this.name,
        "email":  this.email,
        "birthdate": this.birthdate,
        "password": this.password,
        "password2": this.password2,
      }
      try {
        const { data } = await axios.post(api.users.register, payload,
        );

        if (data.status_code === 201) {
          this.redirectLogin()
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
  },
};
</script>

<style scoped>

.scrollable-card {
  max-height: 80vh; /* Altura máxima relativa a la pantalla */
  overflow-y: auto;
}

</style>