<template>
  <div class="comment-card mt-2" v-for="comment in comments" :key="comment.id">
    <div class="d-flex align-items-center mb-1">
      <img :src="comment.avatar || require('@/assets/images/users/user-dummy-img.jpg')"
           class="avatar-xs rounded-circle me-2" />
      <div>
        <strong>{{ comment.user_name }}</strong><br>
        <small class="text-muted">{{ formatDate(comment.timestamp) }}</small>
      </div>
    </div>
    <p class="mb-1">{{ comment.content }}</p>
  </div>
</template>

<script>
export default {
  name: 'CommentCard',
  props: {
    comments: { type: Array, required: true }
  },
  methods: {
    formatDate(iso) {
      return new Date(iso).toLocaleString()
    }
  }
}
</script>

<style scoped>
.comment-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: .4rem;
  padding: .75rem;
}
</style>
