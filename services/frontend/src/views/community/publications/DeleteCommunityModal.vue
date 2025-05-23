<template>
  <teleport to="body">
    <div
      v-if="show"
      class="publish-overlay"
      :style="overlayStyles"
      @click.self="$emit('close')"
    >
      <div class="publish-card" style="max-width:380px;">
        <h5 class="mb-3 text-center">
          ¿Está seguro de eliminar el {{ communityType === 'group' ? 'grupo' : 'foro' }}?
        </h5>
        <div class="d-flex justify-content-between mt-4">
          <BButton variant="secondary" @click="$emit('close')" :disabled="isDeleting">
            Cancelar
          </BButton>
          <BButton variant="danger" @click="$emit('delete')" :disabled="isDeleting">
            <span v-if="isDeleting" class="spinner-border spinner-border-sm me-1"></span>
            Aceptar
          </BButton>
        </div>
        <div v-if="error" class="text-danger text-center mt-2">{{ error }}</div>
      </div>
    </div>
  </teleport>
</template>

<script>
import { BButton } from 'bootstrap-vue-next'
export default {
  name: 'DeleteCommunityModal',
  components: { BButton },
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
    isDeleting: Boolean,
    error: String,
    communityType: String
  }
}
</script>

<style scoped>
.publish-overlay {
  /* puedes dejarlo vacío o solo para fallback */
}
.publish-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: .5rem;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 .5rem 1rem rgba(0,0,0,0.15);
}
</style>
