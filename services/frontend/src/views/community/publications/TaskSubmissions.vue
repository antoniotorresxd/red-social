<template>
  <div class="task-submissions-card mx-auto my-4 p-4 border rounded shadow" style="max-width: 720px;">
    <!-- Cabecera de la tarea -->
    <div class="d-flex justify-content-between align-items-start mb-3">
      <div>
        <h5 class="mb-1">{{ task?.title || 'Tarea' }}</h5>
        <div class="text-muted">{{ task?.description }}</div>
        <div v-if="task?.due_date" class="small text-muted">
          <i class="ri-calendar-event-line me-1"></i>
          Fecha límite: {{ formatDate(task.due_date) }}
        </div>
      </div>
      <div class="task-title text-end">
        <span class="fw-bold">{{ task?.title || '' }}</span>
      </div>
    </div>

    <hr class="mb-3">

    <h6 class="mb-3">Entregas de los participantes</h6>

    <div v-if="isLoading" class="text-center">Cargando entregas...</div>
    <div v-else>
      <div v-if="submissions.length">
        <div
          v-for="submission in submissions"
          :key="submission.id"
          class="submission-card d-flex justify-content-between align-items-center mb-3 p-3 border rounded"
        >
          <div>
            <div class="fw-bold">{{ submission.user_name }}</div>
            <div class="text-muted small">{{ formatDate(submission.submitted_at) }}</div>
            <div>
              <a :href="submission.file" target="_blank" rel="noopener">
                <i class="ri-file-pdf-line"></i> {{ extractFileName(submission.file) }}
              </a>
            </div>
          </div>
          <div>
            <BButton size="sm" variant="outline-primary" @click="openGradeModal(submission)">
              Calificar
            </BButton>
          </div>
        </div>
      </div>
      <div v-else class="text-center text-muted">
        No hay entregas para esta tarea.
      </div>
    </div>

    <!-- MODAL CALIFICAR -->
    <teleport to="body">
      <div v-if="showModal" class="grade-modal-overlay" @click.self="closeModal">
        <div class="grade-modal-card p-4 rounded shadow">
          <h5 class="mb-3">Calificar tarea</h5>
          <div class="mb-2">
            <a :href="selectedSubmission.file" target="_blank" rel="noopener">
              <i class="ri-file-pdf-line fs-4"></i>
              {{ extractFileName(selectedSubmission.file) }}
            </a>
          </div>
          <div class="mb-3 text-muted small">
            Subido el: {{ formatDate(selectedSubmission.submitted_at) }}
          </div>
          <div class="mb-3">
            <label class="form-label">Calificación</label>
            <input v-model="grade" type="number" min="0" max="100" class="form-control" />
          </div>
          <div class="text-end">
            <BButton variant="secondary" class="me-2" @click="closeModal">Cancelar</BButton>
            <BButton variant="primary" :disabled="!grade || isSubmitting" @click="submitGrade">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1"></span>
              Calificar
            </BButton>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script>
import { BButton } from 'bootstrap-vue-next'
import axios from 'axios'
import api from '@/router/api'

export default {
  name: 'TaskSubmissions',
  components: { BButton },
  props: {
    taskId: { type: [String, Number], required: true }
  },
  data() {
    return {
      isLoading: false,
      task: null,
      submissions: [],
      showModal: false,
      selectedSubmission: {},
      grade: '',
      isSubmitting: false,
    }
  },
  mounted() {
    this.fetchTaskAndSubmissions()
  },
  methods: {
    async fetchTaskAndSubmissions() {
      this.isLoading = true
      try {
        // 1. Trae los datos de la tarea
        const taskRes = await axios.get(`${api.publication.publish}${this.taskId}/`)
        this.task = taskRes.data.data

        // 2. Trae las entregas
        const { data } = await axios.get(`${api.publication.publish}${this.taskId}/submissions/`)
        this.submissions = data.data || []
      } catch (e) {
        this.submissions = []
        this.task = {}
      } finally {
        this.isLoading = false
      }
    },
    formatDate(dt) {
      if (!dt) return ''
      return new Date(dt).toLocaleString()
    },
    extractFileName(path) {
      if (!path) return ''
      return path.split('/').pop()
    },
    openGradeModal(submission) {
      this.selectedSubmission = submission
      this.grade = submission.grade || ''
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.selectedSubmission = {}
      this.grade = ''
    },
    async submitGrade() {
      if (!this.grade) return
      this.isSubmitting = true
      try {
        await axios.post(`${api.publication.publish}grader/${this.selectedSubmission.id}/`, {
          grade: this.grade
        })
        this.closeModal()
        this.fetchTaskAndSubmissions()
      } catch (e) {
        // Manejo de error opcional
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
.task-submissions-card {
  background: #fff;
}
.submission-card {
  background: #f8f9fa;
}
.grade-modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.09);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000;
}
.grade-modal-card {
  background: #fff;
  min-width: 320px;
  max-width: 95vw;
  max-height: 95vh;
  overflow-y: auto;
}
</style>
