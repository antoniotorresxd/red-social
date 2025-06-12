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
                <h5 class="text-primary">Cambiar Contraseña</h5>
              </div>

              <div class="p-2 mt-4">
                <b-alert v-model="showError" variant="danger" class="mt-3" dismissible>
                  {{ authError }}
                </b-alert>

                <form @submit.prevent="resetPassword">
                  <div class="mb-3">
                    <label for="email" class="form-label">Correo Institucional</label>
                    <input v-model="email" type="email" required class="form-control" id="email"
                      placeholder="correo@alumno.ipn.mx" />
                  </div>

                  <div class="mb-3">
                    <label for="birthdate" class="form-label">Fecha de nacimiento</label>
                    <input v-model="birthdate" type="date" required class="form-control" id="birthdate" />
                  </div>

                  <div class="mb-3">
                    <label for="new_password" class="form-label">Nueva Contraseña</label>
                    <input v-model="new_password" type="password" required class="form-control"
                      id="new_password" placeholder="Nueva contraseña" />
                  </div>

                  <p class="text-muted">Debe estar seguro de cambiar su contraseña</p>

                  <div class="d-grid mt-4">
                    <BButton variant="info" type="submit" :disabled="processing">
                      {{ processing ? "Cambiando..." : "Cambiar" }}
                    </BButton>
                  </div>

                  <div class="d-grid mt-2">
                    <BButton variant="secondary" class="w-100" type="button" @click="redirectLogin" :disabled="processing">
                    {{ processing ? "Cargando..." : "Cancelar" }}
                  </BButton>
                  </div>

                </form>
              </div>
            </BCardBody>
          </BCard>
        </BCol>
      </BRow>
    </BContainer>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/router/api'

export default {
  name: 'ResetPassword',
  data() {
    return {
      email: '',
      birthdate: '',
      new_password: '',
      authError: '',
      showError: false,
      processing: false,
    }
  },
  methods: {
    redirectLogin(){
      this.$router.push({ name: "login" });
    },
    async resetPassword() {
      // Validación mínima
      if (!this.email || !this.birthdate || !this.new_password) {
        this.authError = "Todos los campos son obligatorios";
        this.showError = true;
        return;
      }

      this.processing = true;

      const payload = {
        email: this.email,
        birthdate: this.birthdate,
        new_password: this.new_password
      }

      try {
        const { data } = await axios.post(api.users.reset_password, payload);
        if (data.status_code === 200) {
          this.$router.push({ name: 'login' });
        } else {
          this.authError = data.message || "No se pudo cambiar la contraseña";
          this.showError = true;
        }
      } catch (err) {
        this.authError =
          err.response?.data?.message ||
          "Error de conexión con el servidor";
        this.showError = true;
      } finally {
        this.processing = false;
      }
    }
  }
}
</script>

<style scoped>

.scrollable-card {
  max-height: 80vh; /* Altura máxima relativa a la pantalla */
  overflow-y: auto;
}

</style>