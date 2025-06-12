<template>
  <div class="pull-left border rounded p-4" style="max-width:400px;">
    <h5 class="mb-4">Unirse Grupo</h5>
    <form @submit.prevent="submit">
      <div class="mb-4">
        <label for="group-name" class="form-label text-uppercase" style="font-size:.85rem;">
          Codigo del grupo
        </label>
        <input
          id="group-name"
          v-model="name"
          type="text"
          class="form-control"
          placeholder="Ingresa el nombre del grupo"
          :disabled="loading"
        />
      </div>

      <div v-if="error" class="text-danger mb-3">{{ error }}</div>

      <div class="text-center">
        <button
          type="submit"
          class="btn btn-outline-primary"
          :disabled="!name.trim() || loading"
          style="min-width:100px;"
        >
          {{ loading ? 'Creando...' : 'Unirse' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/router/api'

export default {
  name: 'JoinGroupForm',
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
        await axios.post(api.community.join, {
          code: this.name.trim(),
          type: "group"
        })
        this.$emit('done')
      } catch (e) {
        this.error = e.response?.data?.message || 'Error al crear el grupo'
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
