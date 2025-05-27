<template>
  <teleport to="body">
    <div v-if="show" class="publish-overlay" :style="overlayStyles" @click.self="close">
      <div class="publish-card" style="max-width:400px;">
        <h5 class="mb-3">Subir tarea</h5>
        <div
          class="file-drop mb-3 d-flex flex-column align-items-center justify-content-center border rounded p-3"
          @dragover.prevent
          @drop.prevent="onDrop"
          style="min-height:100px; cursor:pointer;" @click="$refs.taskFileInput.click()">
          <input type="file" ref="taskFileInput" accept="application/pdf" class="d-none" @change="onFileChange" />
          <template v-if="taskFile">
            <div class="d-flex align-items-center mb-2">
              <i class="ri-file-pdf-2-line fs-2 text-danger me-2"></i>
              <div>
                <div class="fw-bold">{{ taskFile.name }}</div>
                <div class="small text-muted">PDF &middot; {{ (taskFile.size / 1024).toFixed(1) }} KB</div>
                <div class="small text-muted">Subido por ti · {{ now }}</div>
              </div>
              <button type="button" class="btn btn-link ms-2 p-0" @click.stop="removeTaskFile">
                <i class="ri-close-line fs-5"></i>
              </button>
            </div>
          </template>
          <template v-else>
            <div class="text-muted">Arrastra aquí el archivo o haz clic para seleccionar</div>
          </template>
        </div>
        <div v-if="error" class="text-danger small mb-2">{{ error }}</div>
        <div class="text-end">
          <BButton variant="secondary" @click="close">Cancelar</BButton>
          <BButton variant="primary" class="ms-2" :disabled="isSubmitting" @click="submitTaskFile">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1"></span>
            Enviar
          </BButton>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import { BButton } from 'bootstrap-vue-next'
import axios from 'axios'
import api from '@/router/api'
export default {
  name: 'TaskUploadModal',
  components: { BButton },
  props: {
    show: Boolean,
    task: Object,
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
    }
  },
  data() {
    return {
      taskFile: null,
      error: '',
      isSubmitting: false,
      now: new Date().toLocaleString()
    }
  },
  methods: {
    close() {
      this.$emit('close')
      this.taskFile = null
      this.error = ''
    },
    onFileChange(e) {
      const file = e.target.files[0]
      if (!file) return
      if (file.type !== "application/pdf") {
        this.error = "Solo se permiten archivos PDF."
        this.taskFile = null
        return
      }
      this.taskFile = file
      this.error = ''
    },
    onDrop(e) {
      e.preventDefault()
      this.onFileChange({ target: { files: e.dataTransfer.files } })
    },
    removeTaskFile() {
      this.taskFile = null
      this.error = ''
    },
    async submitTaskFile() {
      if (!this.taskFile) {
        this.error = 'Selecciona un archivo para subir.'
        return
      }
      this.isSubmitting = true
      this.error = ''
      try {
        const formData = new FormData()
        formData.append('task', this.task.id)
        formData.append('user_id', localStorage.getItem('user_id'))
        formData.append('file', this.taskFile)
        await axios.post(api.publication.submit_task, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        this.close()
        this.$emit('uploaded')
      } catch (e) {
        this.error = e.response?.data?.message || 'No se pudo subir la tarea.'
      } finally {
        this.isSubmitting = false
      }
    }
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
.file-drop { transition: border-color 0.2s; }
.file-drop:hover { border-color: #0d6efd; }
</style>
