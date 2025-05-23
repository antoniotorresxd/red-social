<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="mb-0">Integrantes</h5>
        <button class="btn btn-link text-dark" @click="close"><i class="ri-close-line fs-3"></i></button>
      </div>
      <div class="border p-3" style="min-height:180px; max-height:400px; overflow-y:auto;">
        <div v-if="isLoading" class="text-center text-muted">Cargando...</div>
        <ul v-else class="list-unstyled mb-0">
          <li v-for="u in users" :key="u.id" class="mb-2">
            <!-- Avatar opcional, puedes usar la primera letra -->
            <span class="avatar avatar-xs rounded-circle bg-primary text-white me-2">{{ u.first_name.charAt(0) }}</span>
            {{ u.first_name }} {{ u.last_name }}
            <span class="text-muted small ms-2">{{ u.email }}</span>
          </li>
        </ul>
        <div v-if="!users.length && !isLoading" class="text-center text-muted">No hay integrantes.</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import api from "@/router/api"

export default {
  props: {
    communityId: { type: Number, required: true },
    show:        { type: Boolean, default: false }
  },
  data() {
    return {
      users: [],
      isLoading: false
    }
  },
  watch: {
    show(newVal) {
      if (newVal) this.loadUsers()
    }
  },
  methods: {
    async loadUsers() {
      this.isLoading = true
      try {
        const { data } = await axios.get(api.community.listUsers, {
          params: { community_id: this.communityId }
        })
        this.users = data.data || []
      } catch (e) {
        this.users = []
      } finally {
        this.isLoading = false
      }
    },
    close() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; left:0; top:0; width:100vw; height:100vh;
  background:rgba(0,0,0,.15); z-index:2000;
  display: flex; align-items: center; justify-content: center;
}
.modal-content {
  background:#fff; border-radius:1rem; padding:1.5rem; min-width:320px; max-width:400px; box-shadow:0 2px 20px #0003;
}
.avatar-xs {
  display:inline-flex; align-items:center; justify-content:center; width:24px; height:24px;
  font-size:14px; font-weight:bold;
}
</style>
