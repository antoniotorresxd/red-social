<template>
  <header id="page-topbar">
    <div class="layout-width">
      <div class="navbar-header">
        <div class="d-flex align-items-center">
          <button type="button" class="btn btn-sm px-3 fs-16 header-item vertical-menu-btn topnav-hamburger"
            id="topnav-hamburger-icon">
            <span class="hamburger-icon">
              <span></span>
              <span></span>
              <span></span>
            </span>
          </button>
        </div>

        <div class="d-flex align-items-center">
          <!-- NOTIFICACIONES -->
          <BDropdown variant="ghost-dark" dropstart class="ms-1 dropdown"
            :offset="{ alignmentAxis: 57, crossAxis: 0, mainAxis: -42 }"
            toggle-class="btn-icon btn-topbar rounded-circle arrow-none" id="page-header-notifications-dropdown"
            menu-class="dropdown-menu-lg dropdown-menu-end p-0" auto-close="outside">
            <template #button-content>
              <i class='bx bx-bell fs-22'></i>
              <span class="position-absolute topbar-badge fs-10 translate-middle badge rounded-pill bg-danger">
                <span class="notification-badge">{{ totalNotis }}</span>
                <span class="visually-hidden">unread messages</span>
              </span>
            </template>
            <div class="dropdown-head bg-primary bg-pattern rounded-top dropdown-menu-lg">
              <div class="p-3">
                <BRow class="align-items-center">
                  <BCol>
                    <h6 class="m-0 fs-16 fw-semibold text-white">
                      Notifications
                    </h6>
                  </BCol>
                  <BCol cols="auto" class="dropdown-tabs">
                    <BBadge variant="light-subtle" class="bg-light-subtle text-body fs-13">
                      {{ totalNotis }} New
                    </BBadge>
                  </BCol>
                </BRow>
              </div>
            </div>
            <BTabs nav-class="dropdown-tabs nav-tab-custom bg-primary px-2 pt-2">
              <BTab title="ALL">
                <simplebar data-simplebar style="max-height: 300px" class="pe-2">
                  <template v-if="notifications.all.length">
                    <NotificationItem v-for="n in notifications.all" :key="n.id" :notification="n"
                      @read="markNotificationAsRead('all', n.id)" />
                  </template>
                  <p v-else class="text-white text-center mt-2 mb-2">No tienes notificaciones</p>
                </simplebar>
              </BTab>
            </BTabs>
          </BDropdown>

          <!-- PERFIL DE USUARIO -->
          <BDropdown variant="link" class="ms-sm-3 header-item topbar-user" toggle-class="rounded-circle arrow-none"
            menu-class="dropdown-menu-end" :offset="{ alignmentAxis: -14, crossAxis: 0, mainAxis: 0 }">
            <template #button-content>
              <span class="d-flex align-items-center">
                <img class="rounded-circle header-profile-user" src="@/assets/images/users/user-dummy-img.jpg"
                  alt="Header Avatar">
                <span class="text-start ms-xl-2">
                  <span class="d-none d-xl-inline-block ms-1 fw-medium user-name-text">{{ userName }}</span>
                </span>
              </span>
            </template>

            <router-link class="dropdown-item" to="" @click.prevent="logout"><i
                class="mdi mdi-logout text-muted fs-16 align-middle me-1"></i>
              <span class="align-middle" data-key="t-logout"> Logout</span>
            </router-link>
          </BDropdown>
        </div>
      </div>
    </div>
  </header>
</template>


<script>
import simplebar from "simplebar-vue";
import NotificationItem from "@/components/notification-item.vue"; // Ajusta si tu path es distinto
import axios from 'axios'
import api from '@/router/api'

export default {
  components: { simplebar, NotificationItem },
  data() {
    return {
      notifications: {
        all: [],
      }
    };
  },
  computed: {
    userName() {
      return localStorage.getItem('user_name') || '';
    },
    // SOLO suma las NO leídas
    totalNotis() {
      return Object.values(this.notifications)
        .reduce((sum, arr) => sum + arr.filter(n => !n.read).length, 0);
    }
  },
  methods: {
    // Agrega una notificación por tipo
    handleNotification(notification) {
      const { type } = notification;
      if (this.notifications[type]) {
        // Si no existe, inicializa el campo 'read' como false (por compatibilidad)
        if (notification.read === undefined) notification.read = false;
        this.notifications[type].unshift(notification);

        // Guarda el arreglo actualizado en localStorage
        const key = `notis_${type}`;
        localStorage.setItem(key, JSON.stringify(this.notifications[type]));
      }
    },
    // Marca como leída y actualiza en localStorage
    markNotificationAsRead(type, id) {
      const noti = this.notifications[type].find(n => n.id === id);
      if (noti && !noti.read) {
        noti.read = true;
        // Persiste el cambio
        const key = `notis_${type}`;
        localStorage.setItem(key, JSON.stringify(this.notifications[type]));
      }
    },
    // Carga las notificaciones guardadas en localStorage
    loadSavedNotifications() {
      const types = ["all"];
      types.forEach(type => {
        const stored = localStorage.getItem(`notis_${type}`);
        if (stored) this.notifications[type] = JSON.parse(stored);
      });
    },
    toggleHamburgerMenu() {
      // Copia exactamente la lógica original de tu plantilla
      const windowSize = document.documentElement.clientWidth;
      const layoutType = document.documentElement.getAttribute("data-layout");
      document.documentElement.setAttribute("data-sidebar-visibility", "show");
      // Icono hamburguesa
      if (windowSize > 767) {
        document.querySelector(".hamburger-icon")?.classList.toggle("open");
      }
      // Menú horizontal
      if (layoutType === "horizontal") {
        document.body.classList.toggle("menu");
      }
      // Menú vertical
      if (["vertical", "semibox"].includes(layoutType)) {
        if (windowSize < 1025 && windowSize > 767) {
          document.body.classList.remove("vertical-sidebar-enable");
          document.documentElement.setAttribute(
            "data-sidebar-size",
            document.documentElement.getAttribute("data-sidebar-size") === "sm" ? "" : "sm"
          );
        } else if (windowSize > 1025) {
          document.body.classList.remove("vertical-sidebar-enable");
          document.documentElement.setAttribute(
            "data-sidebar-size",
            document.documentElement.getAttribute("data-sidebar-size") === "lg" ? "sm" : "lg"
          );
        } else if (windowSize <= 767) {
          document.body.classList.add("vertical-sidebar-enable");
          document.documentElement.setAttribute("data-sidebar-size", "lg");
        }
      }
      // Menú dos columnas
      if (layoutType === "twocolumn") {
        document.body.classList.toggle("twocolumn-panel");
      }
    },
    async logout() {
      try {
        const payload = { refresh: localStorage.getItem('refresh') }
        const { data } = await axios.post(api.users.logout, payload)
        if (data.status_code === 200) {
          localStorage.clear()
          window.location.href = '/login'
        }
      } catch (err) {
        console.error(err?.response?.data?.message || err)
      }
    }
  },
  mounted() {
    // Carga notificaciones persistentes al iniciar
    this.loadSavedNotifications();

    // Escucha cambios en localStorage (otras pestañas)
    window.addEventListener("storage", (event) => {
      if (event.key === "new_notification") {
        const noti = JSON.parse(event.newValue);
        this.handleNotification(noti);
        localStorage.removeItem("new_notification");
      }
    });

    // Escucha evento personalizado para la misma pestaña
    window.addEventListener("show-notification", (e) => {
      this.handleNotification(e.detail);
    });

    // Menú hamburguesa (listener SOLO UNA VEZ)
    const hamb = document.getElementById("topnav-hamburger-icon");
    if (hamb) {
      hamb.addEventListener("click", this.toggleHamburgerMenu);
    }

    // Sombra de barra superior (de tu plantilla)
    document.addEventListener("scroll", function () {
      var pageTopbar = document.getElementById("page-topbar");
      if (pageTopbar) {
        (document.body.scrollTop >= 50 || document.documentElement.scrollTop >= 50)
          ? pageTopbar.classList.add("topbar-shadow")
          : pageTopbar.classList.remove("topbar-shadow");
      }
    });
  }
};
</script>

