<template>
  <li class="publication-card p-4 position-relative border">
    <!-- INFO PRINCIPAL -->
    <div class="d-flex align-items-center mb-2">
      <img :src="pub.authorAvatar || require('@/assets/images/users/user-dummy-img.jpg')"
        class="avatar-xs rounded-circle me-2" alt="Avatar" />
      <div>
        <strong>{{ pub.user_name }}</strong><br>
        <small class="text-muted">{{ formatDate(pub.timestamp) }}</small>
      </div>
    </div>

    <!-- TEXTO PUBLICADO -->
    <div class="publication-text mb-3">
      <h5 v-if="pub.title">
        <strong>Nueva tarea: {{ pub.title }}</strong>
      </h5>
      {{ pub.description }}
      <div v-if="pub.type === 'task' && selectedType === 'group'" class="mt-2">
        <BButton v-if="!isAdmin" size="sm" variant="outline-primary" @click="$emit('upload-task', pub)">
          Subir tarea
        </BButton>

        <BButton class="mt-2" v-else size="sm" variant="outline-success" @click="$emit('grade-task', pub)">
          Calificar tarea
        </BButton>
      </div>
    </div>

    <!-- COMENTARIOS -->
    <div v-if="pub.type === 'post' && showComments">
      <CommentCard :comments="comments" />
      <div class="comment-input-container mt-2 position-relative">
        <input v-model="newComment" class="form-control comment-input pe-5" type="text"
          placeholder="Escribe un comentario..." @keyup.enter="submitComment" />
        <button class="send-button" :disabled="!newComment.trim()" @click="submitComment">
          ↑
        </button>
      </div>
    </div>

    <!-- ICONO DE COMENTAR -->
    <div v-if="pub.type === 'post'" class="comment-action d-flex align-items-center mt-3" @click="toggleComments"
      style="cursor: pointer;">
      <i class="ri-chat-3-line fs-5 me-1"></i>
      <span>Comentarios</span>
    </div>
  </li>
</template>

<script>
import { BButton } from 'bootstrap-vue-next'
import CommentCard from './CommentCard.vue'
import axios from 'axios'
import api from '@/router/api'

export default {
  name: 'PublicationCard',
  components: { BButton, CommentCard },
  props: {
    pub: { type: Object, required: true },
    selectedType: { type: String, required: true },
    isAdmin: { type: Boolean, required: true }
  },
  data() {
    return {
      showComments: false,
      comments: [],
      newComment: ''
    }
  },
  computed: {
    showUploadButton() {
      return this.selectedType === 'group' && this.pub.type === 'task' && !this.isAdmin
    }
  },
  methods: {
    formatDate(iso) {
      return new Date(iso).toLocaleString()
    },
    toggleComments() {
      this.showComments = !this.showComments
      if (this.showComments && this.comments.length === 0) {
        this.fetchComments()
      }
    },
    async fetchComments() {
      try {
        const res = await axios.get(`${api.publication.publish}${this.pub.id}/comments/`)
        this.comments = res.data.data
      } catch (err) {
        console.error('Error al cargar comentarios:', err)
      }
    },
    async submitComment() {
      if (!this.newComment.trim()) return
      try {
        await axios.post(`${api.publication.publish}${this.pub.id}/add-comment/`, {
          content: this.newComment
        })
        this.newComment = ''
        this.fetchComments()
      } catch (err) {
        console.error('Error al comentar:', err)
      }
    }
  }
}
</script>

<style>
.comment-input-container {
  position: relative;
  width: 100%;
}

.comment-input {
  border-radius: 999px;
  background: #f0f2f5;
  padding-right: 2.5rem;
  padding-left: 1rem;
  height: 40px;
}

.send-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: white;
  border: none;
  color: #0d6efd;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.send-button:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>