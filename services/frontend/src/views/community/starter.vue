<template>
  <Layout>
    <div class="chat-wrapper d-lg-flex gap-1 mx-n4 mt-n4 p-1">
      <!-- Sidebar -->
      <div class="chat-leftsidebar border d-flex flex-column">
        <!-- Header + botón -->
        <div class="px-4 pt-4 mb-4">
          <div class="d-flex align-items-start">
            <div class="flex-grow-1">
              <h5 class="mb-4">{{ title }}</h5>
            </div>
            <div class="flex-shrink-0 position-relative" ref="menuWrapper">
              <BButton variant="soft-primary" size="sm" @click="toggleMenu">
                <i class="ri-add-line align-bottom" />
              </BButton>
              <ul
                v-if="showMenu"
                class="dropdown-menu show position-absolute end-0 mt-2"
                style="min-width: 8rem; z-index:1000"
              >
                <li v-for="item in menuItems" :key="item.action">
                  <a
                    href="#"
                    class="dropdown-item"
                    @click.prevent="doMenuAction(item.action)"
                  >
                    {{ item.label }}
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <!-- Buscador -->
          <div class="search-box mt-2">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control bg-light border-light"
              placeholder="Search here..."
            />
            <i class="ri-search-2-line search-icon"></i>
          </div>
        </div>

        <!-- Lista de foros o grupos -->
        <simplebar class="chat-room-list flex-fill" data-simplebar>
          <div v-if="isLoading" class="text-center my-3">Cargando…</div>
          <div v-else-if="error" class="text-danger px-4">{{ error }}</div>
          <ul v-else class="list-unstyled chat-list chat-user-list">
            <li
              v-for="f in filteredForums"
              :key="f.id"
              @click="selectForum(f)"
              :class="{ active: selectedForum && selectedForum.id === f.id }"
            >
              <BLink href="javascript:void(0);">
                <div class="d-flex align-items-center">
                  <div class="flex-shrink-0 chat-user-img online align-self-center me-2">
                    <div class="avatar-xxs" v-if="f.image">
                      <img :src="f.image" class="rounded-circle img-fluid userprofile" />
                    </div>
                    <div class="avatar-xxs" v-else>
                      <div class="avatar-title rounded-circle bg-danger userprofile">
                        {{ f.name.charAt(0) }}
                      </div>
                    </div>
                  </div>
                  <div class="flex-grow-1 overflow-hidden">
                    <p class="text-truncate mb-1">{{ f.name }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <BBadge variant="dark-subtle" class="bg-dark-subtle text-body rounded p-1">
                      {{ f.count }}
                    </BBadge>
                  </div>
                </div>
              </BLink>
            </li>
          </ul>
        </simplebar>
      </div>

      <!-- Área de trabajo -->
      <div class="user-chat w-100 overflow-auto p-4">
        <!-- header móvil con flecha atrás -->
        <div class="d-flex align-items-center mb-4 d-lg-none">
          <BLink href="javascript:void(0)" class="user-chat-remove fs-18 p-1 me-3">
            <i class="ri-arrow-left-s-line align-bottom"></i>
          </BLink>
          <h5 class="mb-0">{{ title }}</h5>
        </div>

        <!-- Formularios de create/join -->
        <component
          v-if="currentActionComponent"
          :is="currentActionComponent"
          @done="handleDone"
          :key="currentActionComponent"
        />

        <!-- PublicationsArea cuando hay un foro/grupo seleccionado -->
        <PublicationsArea
          v-else-if="selectedForum"
          :selected="selectedForum"
          @action="onPubAction"
          @filter="onFilter"
        />

        <!-- Placeholder si no hay nada -->
        <div v-else class="text-center text-muted">
          
        </div>
      </div>
    </div>
  </Layout>
</template>

<script>
import simplebar            from 'simplebar-vue'
import Layout               from '@/layouts/main.vue'
import axios                from 'axios'
import api                  from '@/router/api'

import CreateCommunityForm  from './forum/create.vue'
import JoinCommunityForm    from './forum/join.vue'
import CreateCommunityGroup from './group/create.vue'
import JoinCommunityGroup   from './group/join.vue'

import PublicationsArea     from './publications/starter.vue'

export default {
  name: 'ForumMenuOnly',
  components: {
    Layout,
    simplebar,
    CreateCommunityForm,
    JoinCommunityForm,
    CreateCommunityGroup,
    JoinCommunityGroup,
    PublicationsArea
  },

  data() {
    return {
      showMenu:      false,
      currentAction: null,
      searchQuery:   '',
      forums:        [],
      selectedForum: null,
      isLoading:     false,
      error:         null
    }
  },

  computed: {
    title() {
      const t = this.$route.query.type || 'forum'
      return t === 'group' ? 'Grupos' : 'Foros'
    },
    menuItems() {
      const t = this.$route.query.type || 'forum'
      const label = t === 'group' ? 'grupo' : 'foro'
      return [
        { action: `create-${t}`, label: `Crear ${label}` },
        { action: `join-${t}`,   label: `Unirse a ${label}` }
      ]
    },
    currentActionComponent() {
      switch (this.currentAction) {
        case 'create-forum': return CreateCommunityForm
        case 'join-forum':   return JoinCommunityForm
        case 'create-group': return CreateCommunityGroup
        case 'join-group':   return JoinCommunityGroup
        default:             return null
      }
    },
    filteredForums() {
      const q = this.searchQuery.trim().toLowerCase()
      return q
        ? this.forums.filter(f => f.name.toLowerCase().includes(q))
        : this.forums
    }
  },

  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu
    },

    doMenuAction(action) {
        this.showMenu      = false
        this.currentAction = action
        this.selectedForum = null

        // en móvil, abre el panel de detalle (create/join)
        if (window.innerWidth < 992) {
          document
            .querySelector('.user-chat')
            .classList
            .add('user-chat-show')
        }
      },

    selectForum(item) {
      this.selectedForum = item
      this.currentAction = null

      // en móvil, abre el panel de detalle
      if (window.innerWidth < 992) {
        document
          .querySelector('.user-chat')
          .classList
          .add('user-chat-show')
      }
    },

    resetAll() {
      this.showMenu      = false
      this.currentAction = null
      this.searchQuery   = ''
      this.selectedForum = null

      const panel = document.querySelector('.user-chat')
      panel && panel.classList.remove('user-chat-show')
    },

    async handleDone() {
      this.currentAction = null
      await this.fetchForums()
    },

    async fetchForums() {
      this.isLoading = true
      this.error     = null
      try {
        const { data } = await axios.get(api.community.list, {
          params: { type: this.$route.query.type || '' }
        })
        this.forums = data.data || data
      } catch (e) {
        this.error = 'No se pudieron cargar los datos'
      } finally {
        this.isLoading = false
      }
    },

    onPubAction(action) {
      console.log('Kebab action:', action)
    },

    onFilter() {
      console.log('Filtro pulsado')
    },

    handleClickOutside(e) {
      const w = this.$refs.menuWrapper
      if (w && !w.contains(e.target)) {
        this.showMenu = false
      }
    }
  },

  watch: {
    '$route.query.type'() {
      this.resetAll()
      this.fetchForums()
    }
  },

  mounted() {
    document.addEventListener('click', this.handleClickOutside)

    document.querySelectorAll('.user-chat-remove').forEach(item => {
      item.addEventListener('click', () => {
        document
          .querySelector('.user-chat')
          .classList
          .remove('user-chat-show')
      })
    })

    // carga inicial
    this.fetchForums()
  },

  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  }
}
</script>


<style scoped>
.chat-leftsidebar .dropdown-menu {
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15);
}

/* anima el área de trabajo en móvil */
.chat-wrapper { position: relative; }
.user-chat {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: #fff;
  transform: translateX(100%);
  transition: transform .3s ease-in-out;
  z-index: 5;
}
.user-chat.user-chat-show {
  transform: translateX(0);
}
/* en desktop siempre visible y sin animación */
@media(min-width: 992px) {
  .user-chat {
    position: relative;
    transform: none !important;
  }
}
</style>
