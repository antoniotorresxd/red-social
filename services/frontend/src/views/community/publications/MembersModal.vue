<template>
  <teleport to="body">
    <div v-if="show" class="publish-overlay" :style="overlayStyles" @click.self="$emit('close')">
      <div class="publish-card" style="max-width:380px;">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="mb-0">Integrantes</h5>
          <button class="btn btn-link text-dark p-0" @click="$emit('close')">
            <i class="ri-close-line fs-3"></i>
          </button>
        </div>
        <div style="min-height:150px; max-height:320px; overflow-y:auto;">
          <div v-if="isLoading" class="text-center text-muted">Cargando...</div>
          <ul v-else class="list-unstyled mb-0">
            <li v-for="u in members" :key="u.id" class="mb-2">
              <span
                class="avatar-xs rounded-circle bg-primary text-white me-2 d-inline-flex align-items-center justify-content-center"
                style="width:28px;height:28px;">
                {{ u.name ? u.name.charAt(0) : '-' }}
              </span>
              {{ u.name }}
              <br>
              <span class="text-muted small ms-5">{{ u.email }}</span>
            </li>
          </ul>
          <div v-if="!members.length && !isLoading" class="text-center text-muted">No hay integrantes.</div>
          <div v-if="error" class="text-center text-danger">{{ error }}</div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
export default {
  name: 'MembersModal',
  props: {
    show: Boolean,
    overlayStyles: {
      type: Object,
      default: () => ({
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        background: 'rgba(0,0,0,0.08)',
        zIndex: 1500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      })
    },
    members: Array,
    isLoading: Boolean,
    error: String
  }
}
</script>

<style scoped>
.publish-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: .5rem;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 .5rem 1rem rgba(0,0,0,0.15);
}
</style>
