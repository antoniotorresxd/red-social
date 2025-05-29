<!-- src/views/user/UserProfile.vue -->
<template>
  <div class="col-xl-5 col-12 mx-auto mt-4">
    <h5 class="text-center mb-4">{{ showPasswordForm ? 'Cambiar Contraseña' : 'Mi Perfil' }}</h5>

    <!-- FORMULARIO DE PERFIL -->
    <form v-if="!showPasswordForm" @submit.prevent="updateProfile">
      <div class="mb-3">
        <label>Nombre Completo</label>
        <input type="text" class="form-control" v-model="user.name" :disabled="!editing">
      </div>
      <div class="mb-3">
        <label>Fecha de Nacimiento</label>
        <input type="date" class="form-control" v-model="user.birthdate" :disabled="!editing">
      </div>
      <div class="mb-3">
        <label>No. Boleta</label>
        <input type="text" class="form-control" v-model="user.id_student" :disabled="!editing" placeholder="Opcional">
      </div>
      <div class="mb-3">
        <label>Correo Institucional</label>
        <input type="email" class="form-control" v-model="user.email" disabled>
      </div>

      <div class="d-flex gap-2 mt-4">
        <button hidden class="btn btn-outline-secondary w-100" type="button" @click="showPasswordForm = true">Cambiar contraseña</button>
        <button v-if="editing" class="btn btn-outline-secondary w-100" type="button" @click="cancelEdit">Cancelar</button>
        <button v-if="editing" class="btn btn-primary w-100" type="submit">Guardar</button>
        <button v-else class="btn btn-outline-primary w-100" type="button" @click="editing = true">Modificar</button>
      </div>
    </form>

    <!-- FORMULARIO DE CAMBIO DE CONTRASEÑA -->
    <form v-else @submit.prevent="changePassword">
      <div class="mb-3">
        <label>Nueva Contraseña</label>
        <input type="password" class="form-control" v-model="passwordData.new_password" required>
      </div>
      <div class="mb-3">
        <label>Correo Institucional</label>
        <input type="email" class="form-control" v-model="passwordData.email" required>
      </div>
      <div class="mb-3">
        <label>Fecha de Nacimiento</label>
        <input type="date" class="form-control" v-model="passwordData.birthdate" required>
      </div>

      <p class="text-muted">Debe estar seguro de cambiar su contraseña</p>

      <div class="d-flex justify-content-between mt-3">
        <button type="button" class="btn btn-outline-secondary" @click="showPasswordForm = false">Cancelar</button>
        <button type="submit" class="btn btn-primary">Cambiar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import api from '../../router/api'

export default {
  name: 'UserProfile',
  data() {
    return {
      user: {},
      editing: false,
      showPasswordForm: false,
      passwordData: {
        new_password: '',
        email: '',
        birthdate: ''
      }
    }
  },
  methods: {
    async fetchUser() {
      try {
        const user_id = localStorage.getItem("user_id")
        const { data } = await axios.get(api.users.user + user_id + "/")
        this.user = data.data || data
      } catch (error) {
        console.error('Error al cargar el perfil del usuario:', error)
      }
    },

    async updateProfile() {
      try {
        const user_id = localStorage.getItem("user_id")
        const payload = {
          name: this.user.name,
          birthdate: this.user.birthdate,
          id_student: this.user.id_student,
          email: this.user.email
        }
        await axios.put(api.users.user + user_id + "/", payload)
        localStorage.setItem("user_name", this.user.name)
        this.editing = false
        window.location.reload()
      } catch (error) {
        console.error('Error al actualizar perfil:', error)
      }
    },

    cancelEdit() {
      this.editing = false
      this.fetchUser()
    },

    async changePassword() {
      try {
        const user_id = localStorage.getItem("user_id")
        const payload = {
          email: this.passwordData.email,
          id: user_id,
          birthdate: this.passwordData.birthdate,
          new_password: this.passwordData.new_password
        }
        await axios.post(api.users.reset_password, payload)
        this.showPasswordForm = false
      } catch (error) {
        console.error('Error al cambiar la contraseña:', error)
      }
    }
  },
  mounted() {
    this.fetchUser()
  }
}
</script>
