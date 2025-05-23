<template>
  <div class="publications-wrapper">
    <!-- Área principal -->
    <div class="publications-area" ref="root">
      <!-- HEADER -->
      <div class="d-flex justify-content-between align-items-center mb-3 pub-header" ref="header">
        <!-- Kebab -->
        <button class="btn btn-ghost-secondary btn-icon" ref="kebabBtn" @click="toggleKebab">
          <i class="ri-more-2-fill fs-5"></i>
        </button>
        <!-- Filtrar -->
        <BButton variant="outline-secondary" size="sm" @click="$emit('filter')">
          <i class="ri-filter-3-line me-1"></i> Filtrar
        </BButton>
      </div>

      <!-- LISTADO DE PUBLICACIONES -->
      <simplebar class="publications-list" data-simplebar style="max-height: 60vh;">
        <div v-if="isLoadingPubs" class="text-center py-3">Cargando publicaciones…</div>
        <div v-else-if="errorPubs" class="text-danger text-center py-3">{{ errorPubs }}</div>
        <ul v-else class="list-unstyled">
          <li
            v-for="pub in filteredPublications"
            :key="pub.id"
            class="publication-card mb-3 p-3 position-relative border"
          >
            <!-- Cabecera con avatar, nombre y fecha -->
            <div class="d-flex align-items-center mb-2">
              <img
                :src="pub.authorAvatar || require('@/assets/images/users/user-dummy-img.jpg')"
                class="avatar-xs rounded-circle me-2"
                alt="Avatar"
              />
              <div>
                <strong>{{ pub.user_name }}</strong><br>
                <small class="text-muted">{{ formatDate(pub.timestamp) }}</small>
              </div>
            </div>

            <!-- Texto de la publicación -->
            <div class="publication-text mb-4">
              <h5 v-if="pub.title">
                <strong>Asignación: {{ pub.title }}</strong>
              </h5>
              {{ pub.description }}
            </div>

            <!-- Icono de comentarios en la esquina inferior derecha -->
            <div class="publication-icon position-absolute">
              <i class="ri-chat-3-line fs-5"></i>
            </div>
          </li>

          <li v-if="!filteredPublications.length" class="text-center text-muted py-3">
            <!-- No hay publicaciones que mostrar -->
          </li>
        </ul>
      </simplebar>
    </div>

    <!-- DROPDOWN (Publicar / Integrantes / Eliminar foro / Crear tarea si es grupo) -->
    <teleport to="body">
      <ul v-if="showKebab" class="dropdown-menu show" :style="menuStyles" @click.stop>
        <li v-for="item in kebabItems" :key="item">
          <a href="#" class="dropdown-item" @click.prevent="onSelect(item)">
            {{ item }}
          </a>
        </li>
      </ul>
    </teleport>

    <!-- MODAL “Publicar” -->
    <teleport to="body">
      <div
        v-if="modalType==='post'"
        class="publish-overlay"
        :style="overlayStyles"
        @click.self="closeModal"
      >
        <div class="publish-card">
          <h5 class="mb-3">Crear publicación</h5>
          <textarea
            v-model="newPost"
            class="form-control mb-3"
            rows="6"
            placeholder="Texto a publicar..."
          ></textarea>
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

    <!-- MODAL “Crear tarea” (solo para grupos) -->
    <teleport to="body">
      <div
        v-if="modalType==='task'"
        class="publish-overlay"
        :style="overlayStyles"
        @click.self="closeModal"
      >
        <div class="publish-card">
          <h5 class="mb-3">Crear tarea</h5>
          <input
            v-model="taskTitle"
            type="text"
            class="form-control mb-3"
            placeholder="Nombre de la tarea"
          />
          <textarea
            v-model="taskDesc"
            class="form-control mb-3"
            rows="4"
            placeholder="Descripción de la tarea"
          ></textarea>
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

export default {
  name: 'PublicationsArea',
  components: { simplebar, BButton },
  emits: ['action', 'filter'],
  props: {
    selected: { type: Object, required: true }
  },
  data() {
    return {
      // publicaciones
      publications: [],
      isLoadingPubs: false,
      errorPubs: '',
      searchQuery: '',

      // kebab + modales
      kebabItems: [],
      showKebab: false,
      menuStyles: {},
      modalType: null,       // 'post' | 'task'
      overlayStyles: {},

      // publicar
      newPost: '',
      isSubmitting: false,

      // tarea
      taskTitle: '',
      taskDesc: '',
      isSubmittingTask: false
    }
  },
  computed: {
    filteredPublications() {
      const q = this.searchQuery.trim().toLowerCase()
      return q
        ? this.publications.filter(p => p.description.toLowerCase().includes(q))
        : this.publications
    }
  },
  watch: {
    selected: {
      handler() {
        this.setupKebab()
        this.fetchPublications()
      },
      immediate: true
    }
  },
  methods: {
    // Inicializa las opciones del kebab
    setupKebab() {
      this.kebabItems = ['Publicar', 'Integrantes', 'Eliminar foro']
      if (this.selected.type === 'group') {
        this.kebabItems.splice(1, 0, 'Crear tarea')
      }
    },

    // — FETCH PUBLICACIONES —
    async fetchPublications() {
      this.isLoadingPubs = true
      this.errorPubs = ''
      try {
        const url = api.publication.publish
        const { data } = await axios.get(url, {
          params: { community_id: this.selected.id }
        })
        this.publications = data.data || data
      } catch (e) {
        this.errorPubs = 'No se pudieron cargar las publicaciones.'
      } finally {
        this.isLoadingPubs = false
      }
    },

    formatDate(iso) {
      return new Date(iso).toLocaleString()
    },

    // — KEBAB —
    toggleKebab() {
      this.showKebab = !this.showKebab
      if (this.showKebab) this.$nextTick(this.positionMenu)
    },
    positionMenu() {
      const btn = this.$refs.kebabBtn.getBoundingClientRect()
      this.menuStyles = {
        position: 'fixed',
        top:      `${btn.bottom}px`,
        left:     `${btn.left}px`,
        minWidth: '8rem',
        zIndex:   2000
      }
    },
    onSelect(item) {
      this.showKebab = false
      if (item === 'Publicar') {
        this.openModal('post')
      } else if (item === 'Crear tarea') {
        this.openModal('task')
      } else {
        this.$emit('action', item)
      }
    },

    // — MODALES —
    openModal(type) {
      this.modalType = type
      this.$nextTick(this.positionOverlay)
    },
    closeModal() {
      this.modalType = null
      this.newPost = ''
      this.taskTitle = ''
      this.taskDesc = ''
    },
    positionOverlay() {
      const root   = this.$refs.root.getBoundingClientRect()
      const header = this.$refs.header.getBoundingClientRect()
      this.overlayStyles = {
        position:      'fixed',
        top:           `${root.top + header.height}px`,
        left:          `${root.left}px`,
        width:         `${root.width}px`,
        height:        `${root.height - header.height}px`,
        background:    'rgba(0,0,0,0.05)',
        zIndex:        1500,
        display:       'flex',
        alignItems:    'center',
        justifyContent:'center'
      }
    },

    // — ACCIONES POST —
    async submitPublish() {
      if (!this.newPost.trim()) return
      this.isSubmitting = true
      try {
        await axios.post(api.publication.publish, {
          community_id: this.selected.id,
          user_id:      localStorage.getItem('user_id'),
          type:         'post',
          description:  this.newPost.trim()
        })
        await this.fetchPublications()
        this.closeModal()
      } catch (err) {
        console.error(err)
      } finally {
        this.isSubmitting = false
      }
    },

    // — ACCIONES TASK —
    async submitTask() {
      if (!this.taskTitle.trim()) return
      this.isSubmittingTask = true
      try {
        await axios.post(api.publication.publish, {
          community_id: this.selected.id,
          user_id:      localStorage.getItem('user_id'),
          type:         'task',
          title:        this.taskTitle.trim(),
          description:  this.taskDesc.trim()
        })
        await this.fetchPublications()
        this.closeModal()
      } catch (err) {
        console.error(err)
      } finally {
        this.isSubmittingTask = false
      }
    }
  }
}
</script>

<style scoped>
.publications-area {
  position: relative;
}
.pub-body {
  margin-bottom: 1rem;
}
/* kebab button */
.btn-icon {
  padding: 0.5rem;
}
/* lista scroll */
.publications-list {
  max-height: 60vh;
}
/* modal-card */
.publish-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: .5rem;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 .5rem 1rem rgba(0,0,0,0.15);
}
/* publicación */
.avatar-xs {
  width: 32px; height: 32px;
}
.publication-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: .5rem;
}
/* icono comentarios */
.publication-icon {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
</style>
