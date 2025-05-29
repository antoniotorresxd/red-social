<template>
  <div class="mx-auto border rounded p-4" style="max-width:400px;">
    <h5 class="mb-4">Crear Foro</h5>
    <form @submit.prevent="submit">
      <div class="mb-4">
        <label for="forum-name" class="form-label text-uppercase" style="font-size:.85rem;">
          Nombre del foro
        </label>
        <input id="forum-name" v-model="name" type="text" class="form-control" placeholder="Ingresa el nombre del foro"
          :disabled="loading" />
      </div>

      <div v-if="error" class="text-danger mb-3">{{ error }}</div>

      <div class="text-center">
        <button type="submit" class="btn btn-outline-primary" :disabled="!name.trim() || loading"
          style="min-width:100px;">
          {{ loading ? 'Creando...' : 'Crear' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/router/api'

export default {
  name: 'CreateForumForm',
  data() {
    return {
      name: '',
      loading: false,
      error: ''
    }
  },
  methods: {
    async submit() {
      if (!this.name.trim()) return
      this.loading = true
      this.error = ''
      try {

        await axios.post(api.community.create, {
          name: this.name.trim(),
          type: 'forum',
          admin_id: localStorage.getItem("user_id"),
        })

        const noti = {
          id: Date.now(),
          user_id: localStorage.getItem("user_id"), 
          title: "Foro creado",
          message: `El foro ${this.name.trim()} se ha creado correctamente.`,
          type: "all",
          created_at: new Date().toISOString(),
          read: false 
        };
        localStorage.setItem("new_notification", JSON.stringify(noti));
        window.dispatchEvent(new CustomEvent("show-notification", { detail: noti }));

        this.$emit('done')
      } catch (e) {
        this.error = e.response?.data?.message || 'Error al crear el foro'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.border {
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}
</style>
