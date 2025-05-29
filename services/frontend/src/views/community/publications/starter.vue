<template>
  <div class="publications-wrapper">

    <div class="publications-area" ref="root">

      <div class="d-flex justify-content-between align-items-center mb-3 pub-header" ref="header">

        <button v-if="showTaskSubmissions" class="btn btn-ghost-secondary btn-icon" @click="closeGrading">
          <i class="ri-arrow-left-line fs-5"></i>
        </button>

        <button v-else class="btn btn-ghost-secondary btn-icon" ref="kebabBtn" @click="toggleKebab">
          <i class="ri-more-2-fill fs-5"></i>
        </button>

        <BButton variant="outline-secondary" size="sm" @click="onFilter">
          <i class="ri-filter-3-line me-1"></i> Ordenar
        </BButton>

      </div>

      <!-- ÁREA DINÁMICA: Cambia entre publicaciones y workspace entregas -->
      <div>
        <TaskSubmissions v-if="showTaskSubmissions" :task-id="gradingTask?.id" @close="closeGrading" />
        <template v-else>
          <simplebar class="publications-list" data-simplebar style="max-height: 75vh;">
            <div v-if="isLoadingPubs" class="text-center py-3">Cargando publicaciones…</div>
            <div v-else-if="errorPubs" class="text-danger text-center py-3">{{ errorPubs }}</div>
            <ul v-else class="list-unstyled">
              <PublicationCard class="m-2" v-for="pub in filteredPublications" :key="pub.id" :pub="pub"
                :selectedType="selected.type" :isAdmin="isAdmin" @upload-task="openUploadModal"
                @grade-task="openGrading" />
              <li v-if="!filteredPublications.length" class="text-center text-muted py-3">
                <!-- No hay publicaciones que mostrar -->
              </li>
            </ul>
          </simplebar>
        </template>
      </div>
    </div>


    <!-- MODALES -->
    <TaskUploadModal :show="showUploadModal" :task="selectedTask" :overlayStyles="uploadOverlayStyles"
      @close="closeUploadModal" @uploaded="fetchPublications" />

    <MembersModal :show="showMembers" :overlayStyles="membersOverlayStyles" :members="members"
      :isLoading="isLoadingMembers" :error="errorMembers" @close="closeMembersModal" />

    <DeleteCommunityModal :show="showDeleteModal" :overlayStyles="deleteOverlayStyles" :isDeleting="isDeleting"
      :error="deleteError" :communityType="selected.type" @close="closeDeleteModal" @delete="confirmDeleteCommunity" />

    <ExitCommunityModal :show="showExitModal" :overlayStyles="exitOverlayStyles" :isExiting="isExiting"
      :error="exitError" :communityType="selected.type" @close="closeExitModal" @exit="confirmExitCommunity" />

    <!-- MENU KEBAB -->
    <teleport to="body">
      <ul v-if="showKebab" class="dropdown-menu show" :style="menuStyles" @click.stop>
        <li v-for="item in kebabItems" :key="item">
          <a href="#" class="dropdown-item" @click.prevent="onSelect(item)">
            {{ item }}
          </a>
        </li>
      </ul>
    </teleport>

    <!-- MODAL “Crear publicación” -->
    <teleport to="body">
      <div v-if="modalType === 'post'" class="publish-overlay" :style="modalOverlayStyles" @click.self="closeModal">
        <div class="publish-card">
          <h5 class="mb-3">Crear publicación</h5>
          <textarea v-model="newPost" class="form-control mb-3" rows="6" placeholder="Texto a publicar..."></textarea>
          <div class="text-end">
            <BButton variant="secondary" @click="closeModal">Cancelar</BButton>
            <BButton variant="primary" class="ms-2" :disabled="isSubmitting" @click="submitPublish">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1"></span>
              Publicar
            </BButton>
          </div>
        </div>
      </div>
    </teleport>

    <!-- MODAL “Crear tarea” (solo admin y grupos) -->
    <teleport to="body">
      <div v-if="modalType === 'task'" class="publish-overlay mt-5 pt-5" :style="modalOverlayStyles"
        @click.self="closeModal">
        <div class="publish-card">
          <h5 class="mb-3">Crear tarea</h5>
          <label for="">Nombre de la tarea</label>
          <input v-model="taskTitle" type="text" class="form-control mb-3" placeholder="" />
          <label for="">Descripción de la tarea</label>
          <textarea v-model="taskDesc" class="form-control mb-3" rows="4" placeholder=""></textarea>
          <label for="">Fecha de vencimiento</label>
          <input v-model="taskDue" class="form-control mb-3" type="datetime-local" name="" id="">
          <div class="text-end">
            <BButton variant="secondary" @click="closeModal">Cancelar</BButton>
            <BButton variant="primary" class="ms-2" :disabled="isSubmittingTask" @click="submitTask">
              <span v-if="isSubmittingTask" class="spinner-border spinner-border-sm me-1"></span>
              Crear
            </BButton>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/router/api'
import simplebar from 'simplebar-vue'
import { BButton } from 'bootstrap-vue-next'
import PublicationCard from './PublicationCard.vue'
import TaskUploadModal from './TaskUploadModal.vue'
import MembersModal from './MembersModal.vue'
import DeleteCommunityModal from './DeleteCommunityModal.vue'
import ExitCommunityModal from './ExitCommunityModal.vue'
import TaskSubmissions from './TaskSubmissions.vue'


export default {
  name: 'PublicationsStarter',
  components: {
    simplebar, BButton,
    PublicationCard, TaskUploadModal, MembersModal, DeleteCommunityModal, ExitCommunityModal, TaskSubmissions,
  },
  props: {
    selected: { type: Object, required: true }
  },
  data() {
    return {
      publications: [],
      isLoadingPubs: false,
      errorPubs: '',
      searchQuery: '',
      sortOrder: 'desc',
      // kebab + modales
      kebabItems: [],
      showKebab: false,
      menuStyles: {},
      modalType: null,      // 'post' | 'task'
      modalOverlayStyles: {},
      // publicar
      newPost: '',
      isSubmitting: false,
      // tarea
      taskTitle: '',
      taskDesc: '',
      taskDue: '',
      isSubmittingTask: false,
      // Integrantes
      showMembers: false,
      members: [],
      isLoadingMembers: false,
      errorMembers: '',
      membersOverlayStyles: {},
      // Eliminar comunidad
      showDeleteModal: false,
      isDeleting: false,
      deleteError: '',
      deleteOverlayStyles: {},
      // Salir comunidad
      showExitModal: false,
      isExiting: false,
      exitError: '',
      exitOverlayStyles: {},
      // Subir tarea
      showUploadModal: false,
      selectedTask: null,
      uploadOverlayStyles: {},
      // submmision task
      showTaskSubmissions: false,
      gradingTask: null,
    }
  },
  computed: {
    filteredPublications() {
      const q = this.searchQuery.trim().toLowerCase()
      return q
        ? this.publications.filter(p => p.description.toLowerCase().includes(q))
        : this.publications
    },
    isAdmin() {
      const userId = parseInt(localStorage.getItem('user_id'))
      return this.selected && userId === this.selected.admin_id
    }
  },
  watch: {
    selected: {
      handler() {
        this.showTaskSubmissions = false;
        this.gradingTask = null;
        this.setupKebab()
        this.fetchPublications()
      },
      immediate: true
    }
  },
  methods: {
    openGrading(pub) {
      this.gradingTask = pub
      this.showTaskSubmissions = true
    },
    closeGrading() {
      this.showTaskSubmissions = false
      this.gradingTask = null
    },
    // ===== MODALES HIJOS =====
    openUploadModal(pub) {
      this.selectedTask = pub
      this.showUploadModal = true
      this.$nextTick(this.positionUploadOverlay)
    },
    closeUploadModal() {
      this.showUploadModal = false
      this.selectedTask = null
    },
    positionUploadOverlay() {
      const root = this.$refs.root.getBoundingClientRect()
      const header = this.$refs.header.getBoundingClientRect()
      this.uploadOverlayStyles = {
        position: 'fixed',
        top: `${root.top + header.height}px`,
        left: `${root.left}px`,
        width: `${root.width}px`,
        height: `${root.height - header.height}px`,
        background: 'rgba(0,0,0,0.05)',
        zIndex: 1500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }
    },

    // MODAL INTEGRANTES
    openMembersModal() {
      this.showMembers = true
      this.fetchMembers()
      this.$nextTick(this.positionMembersOverlay)
    },
    closeMembersModal() {
      this.showMembers = false
    },
    positionMembersOverlay() {
      const root = this.$refs.root.getBoundingClientRect()
      const header = this.$refs.header.getBoundingClientRect()
      this.membersOverlayStyles = {
        position: 'fixed',
        top: `${root.top + header.height}px`,
        left: `${root.left}px`,
        width: `${root.width}px`,
        height: `${root.height - header.height}px`,
        background: 'rgba(0,0,0,0.05)',
        zIndex: 1500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }
    },

    // MODAL ELIMINAR
    openDeleteModal() {
      this.showDeleteModal = true
      this.$nextTick(this.positionDeleteOverlay)
    },
    closeDeleteModal() {
      this.showDeleteModal = false
      this.deleteError = ''
    },
    positionDeleteOverlay() {
      const root = this.$refs.root.getBoundingClientRect()
      const header = this.$refs.header.getBoundingClientRect()
      this.deleteOverlayStyles = {
        position: 'fixed',
        top: `${root.top + header.height}px`,
        left: `${root.left}px`,
        width: `${root.width}px`,
        height: `${root.height - header.height}px`,
        background: 'rgba(0,0,0,0.05)',
        zIndex: 1500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }
    },

    // MODAL SALIR
    openExitModal() {
      this.showExitModal = true
      this.$nextTick(this.positionExitOverlay)
    },
    closeExitModal() {
      this.showExitModal = false
      this.exitError = ''
    },
    positionExitOverlay() {
      const root = this.$refs.root.getBoundingClientRect()
      const header = this.$refs.header.getBoundingClientRect()
      this.exitOverlayStyles = {
        position: 'fixed',
        top: `${root.top + header.height}px`,
        left: `${root.left}px`,
        width: `${root.width}px`,
        height: `${root.height - header.height}px`,
        background: 'rgba(0,0,0,0.05)',
        zIndex: 1500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }
    },

    // MODAL PUBLICAR/TAREA
    openModal(type) {
      this.modalType = type
      this.$nextTick(this.positionModalOverlay)
    },
    closeModal() {
      this.modalType = null
      this.newPost = ''
      this.taskTitle = ''
      this.taskDesc = ''
      this.taskDue = ''
    },
    positionModalOverlay() {
      const root = this.$refs.root.getBoundingClientRect()
      const header = this.$refs.header.getBoundingClientRect()
      this.modalOverlayStyles = {
        position: 'fixed',
        top: `${root.top + header.height}px`,
        left: `${root.left}px`,
        width: `${root.width}px`,
        height: `${root.height - header.height}px`,
        background: 'rgba(0,0,0,0.05)',
        zIndex: 1500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }
    },

    // ========== FETCH =============
    async fetchPublications(order) {
      this.isLoadingPubs = true
      this.errorPubs = ''
      try {
        const url = api.publication.publish
        let params = { community_id: this.selected.id }
        if (order) {
          params.ordering = order === 'desc' ? 'timestamp' : '-timestamp'
        }
        const { data } = await axios.get(url, { params })
        this.publications = data.data || data
        this.sortOrder = order || this.sortOrder
      } catch (e) {
        this.errorPubs = 'No se pudieron cargar las publicaciones.'
      } finally {
        this.isLoadingPubs = false
      }
    },

    async fetchMembers() {
      this.isLoadingMembers = true
      this.errorMembers = ''
      try {
        const url = `${api.community.list}${this.selected.id}/`
        const res = await axios.get(url)
        const userIds = res.data.data.list_users || []
        if (!userIds.length) {
          this.members = []
          this.isLoadingMembers = false
          return
        }
        const url_participants = api.users.user
        const usersRes = await axios.get(url_participants, {
          params: { ids: userIds.join(',') }
        })
        this.members = usersRes.data?.data || []
      } catch (e) {
        this.errorMembers = 'No se pudieron cargar los integrantes.'
      } finally {
        this.isLoadingMembers = false
      }
    },

    // ========== KEBAB Y ACCIONES ============
    setupKebab() {
      this.kebabItems = []
      if (this.isAdmin) {
        this.kebabItems.push('Publicar')
        if (this.selected.type === 'group') {
          this.kebabItems.push('Crear tarea')
        }
        this.kebabItems.push('Integrantes')
        this.kebabItems.push(
          this.selected.type === 'group' ? 'Eliminar grupo' : 'Eliminar foro'
        )
      } else {
        this.kebabItems.push('Publicar')
        this.kebabItems.push('Integrantes')
        this.kebabItems.push(
          this.selected.type === 'group' ? 'Salir del grupo' : 'Salir del foro'
        )
      }
    },
    handleOutsideClick(event) {
      const kebab = this.$refs.kebabBtn
      const menu = document.querySelector('.dropdown-menu.show')

      // Si se hace clic fuera del botón y del menú, lo cerramos
      if (
        this.showKebab &&
        !kebab?.contains(event.target) &&
        !menu?.contains(event.target)
      ) {
        this.showKebab = false
      }
    },
    toggleKebab() {
      this.showKebab = !this.showKebab
      if (this.showKebab) this.$nextTick(this.positionMenu)
    },
    positionMenu() {
      const btn = this.$refs.kebabBtn.getBoundingClientRect()
      this.menuStyles = {
        position: 'fixed',
        top: `${btn.bottom}px`,
        left: `${btn.left}px`,
        minWidth: '8rem',
        zIndex: 2000
      }
    },
    onSelect(item) {
      this.showKebab = false
      if (item === 'Publicar') {
        this.openModal('post')
      } else if (item === 'Crear tarea') {
        this.openModal('task')
      } else if (item === 'Integrantes') {
        this.openMembersModal()
      } else if (item === 'Eliminar foro' || item === 'Eliminar grupo') {
        this.openDeleteModal()
      } else if (item === 'Salir del foro' || item === 'Salir del grupo') {
        this.openExitModal()
      } else {
        // custom actions
      }
    },

    // ========== PUBLICAR/TAREA ============
    async submitPublish() {
      if (!this.newPost.trim()) return
      this.isSubmitting = true
      try {
        await axios.post(api.publication.publish, {
          community_id: this.selected.id,
          user_id: localStorage.getItem('user_id'),
          type: 'post',
          description: this.newPost.trim()
        })
        await this.fetchPublications()
        this.closeModal()
      } catch (err) {
        console.error(err)
      } finally {
        this.isSubmitting = false
      }
    },
    async submitTask() {
      if (!this.taskTitle.trim()) return
      this.isSubmittingTask = true
      try {
        await axios.post(api.publication.publish, {
          community_id: this.selected.id,
          user_id: localStorage.getItem('user_id'),
          type: 'task',
          title: this.taskTitle.trim(),
          description: this.taskDesc.trim(),
          due_date: this.taskDue

        })
        await this.fetchPublications()
        this.closeModal()
      } catch (err) {
        console.error(err)
      } finally {
        this.isSubmittingTask = false
      }
    },

    // ========== ELIMINAR/SALIR ============
    async confirmDeleteCommunity() {
      this.isDeleting = true
      this.deleteError = ''
      try {
        await axios.delete(`${api.community.list}${this.selected.id}/`)
        this.$emit('done') // actualiza comunidades arriba
        this.closeDeleteModal()
      } catch (err) {
        this.deleteError = 'No se pudo eliminar la comunidad.'
      } finally {
        this.isDeleting = false
      }
    },
    async confirmExitCommunity() {
      this.isExiting = true
      this.exitError = ''
      try {
        await axios.post(
          `${api.community.list}${this.selected.id}/exit/`,
          {},
          { headers: { 'X-User-Id': localStorage.getItem('user_id') } }
        )
        this.$emit('done')
        this.closeExitModal()
      } catch (err) {
        this.exitError = err.response?.data?.message || 'No se pudo salir de la comunidad.'
      } finally {
        this.isExiting = false
      }
    },
    onFilter() {
      const newOrder = this.sortOrder === 'desc' ? 'asc' : 'desc'
      this.fetchPublications(newOrder)
    }
  },
  mounted() {
    document.addEventListener('click', this.handleOutsideClick)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleOutsideClick)
  },
}
</script>

<style scoped>
.publications-area {
  position: relative;
}

.pub-body {
  margin-bottom: 1rem;
}

.btn-icon {
  padding: 0.5rem;
}

.publications-list {
  max-height: 60vh;
}

.publish-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: .5rem;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 .5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
