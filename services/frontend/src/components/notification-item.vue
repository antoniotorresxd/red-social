<template>
  <div class="text-reset notification-item d-block dropdown-item position-relative">
    <div class="d-flex">
      <div class="avatar-xs me-3 flex-shrink-0">
        <span class="avatar-title bg-info-subtle text-info rounded-circle fs-16">
          <i class="bx bx-badge-check"></i>
        </span>
      </div>
      <div class="flex-grow-1">
        <BLink href="#!" class="stretched-link" @click="markAsRead">
          <h6 class="mt-0 mb-2 lh-base d-flex align-items-center">
            {{ notification.title }}
            <span v-if="!notification.read" class="dot-unread ms-2"></span>
          </h6>
        </BLink>
        <p class="mb-0 fs-11 fw-medium text-uppercase text-muted">
          <span><i class="mdi mdi-clock-outline"></i> {{ formattedDate }}</span>
        </p>
        <p class="mb-0 fs-12">{{ notification.message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    notification: { type: Object, required: true }
  },
  computed: {
    formattedDate() {
      const date = new Date(this.notification.created_at);
      return date.toLocaleString('es-MX', {
        hour: '2-digit',
        minute: '2-digit',
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      });
    }
  },
  methods: {
    markNotificationAsRead(type, id) {
      const noti = this.notifications[type].find(n => n.id === id);
      if (noti && !noti.read) {
        noti.read = true;
        // GUARDAR EN LOCALSTORAGE:
        const key = `notis_${type}`;
        localStorage.setItem(key, JSON.stringify(this.notifications[type]));
      }
    },
  }
};
</script>

<style scoped>
.dot-unread {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #e00;
  margin-left: 0.3rem;
  border: 2px solid #fff;
}
</style>
