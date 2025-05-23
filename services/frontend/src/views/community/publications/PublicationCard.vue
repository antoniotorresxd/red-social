<template>
  <li class="publication-card mb-3 p-3 position-relative border">
    <div class="d-flex align-items-center mb-2">
      <img :src="pub.authorAvatar || require('@/assets/images/users/user-dummy-img.jpg')"
           class="avatar-xs rounded-circle me-2" alt="Avatar" />
      <div>
        <strong>{{ pub.user_name }}</strong><br>
        <small class="text-muted">{{ formatDate(pub.timestamp) }}</small>
      </div>
    </div>
    <div class="publication-text mb-4">
      <h5 v-if="pub.title">
        <strong>Nueva tarea: {{ pub.title }}</strong>
      </h5>
      {{ pub.description }}
      <div v-if="showUploadButton" class="mt-2">
        <BButton size="sm" variant="outline-primary" @click="$emit('upload-task', pub)">
          Subir tarea
        </BButton>
      </div>
    </div>
    <div class="publication-icon position-absolute">
      <i class="ri-chat-3-line fs-5"></i>
    </div>
  </li>
</template>

<script>
import { BButton } from 'bootstrap-vue-next'
export default {
  name: 'PublicationCard',
  components: { BButton },
  props: {
    pub: { type: Object, required: true },
    selectedType: { type: String, required: true },
    isAdmin: { type: Boolean, required: true }
  },
  computed: {
    showUploadButton() {
      // Botón solo para tareas, grupos y no admin
      return this.selectedType === 'group' && this.pub.type === 'task' && !this.isAdmin
    }
  },
  methods: {
    formatDate(iso) {
      return new Date(iso).toLocaleString()
    }
  }
}
</script>

<style scoped>
.publication-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: .5rem;
  position: relative;
}
.publication-icon {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
.avatar-xs {
  width: 32px;
  height: 32px;
}
</style>
