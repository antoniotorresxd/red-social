<template>
  <div class="pull-left border rounded p-4" style="max-width:400px;">
    <h5 class="mb-4 d-flex justify-content-center">Unirse a Foro</h5>
    <div class="mb-3">
      <label for="forum-search" class="form-label text-uppercase" style="font-size:.85rem;">
        Nombre del foro
      </label>
      <input
        id="forum-search"
        v-model="searchTerm"
        type="text"
        class="form-control"
        placeholder="Escribe para buscar..."
        :disabled="joining"
      />
    </div>

    <div v-if="loadingMatches" class="text-center mb-3">
      Buscando…
    </div>

    <ul v-else class="list-group mb-3" style="max-height:200px; overflow:auto;">
      <li
        v-for="f in options"
        :key="f.id"
        class="list-group-item list-group-item-action d-flex align-items-center"
        :class="{ active: selected && selected.id === f.id }"
        @click="selectForum(f)"
        style="cursor:pointer;"
      >
        <span class="me-2">
          <i class="ri-forum-line"></i>
        </span>
        <span class="flex-grow-1 text-truncate">{{ f.name }}</span>
      </li>
      <li v-if="!loadingMatches && options.length === 0" class="list-group-item text-muted">
        No se encontraron foros
      </li>
    </ul>

    <div v-if="error" class="text-danger mb-3">{{ error }}</div>

    <div class="text-center">
      <button
        class="btn btn-outline-primary"
        @click="submit"
        :disabled="!selected || joining"
        style="min-width:100px;"
      >
        {{ joining ? 'Uniendo...' : 'Unirse' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/router/api'

export default {
  name: 'JoinForumForm',
  data() {
    return {
      searchTerm: '',
      options: [],
      selected: null,
      loadingMatches: false,
      joining: false,
      error: '',
      searchTimeoutId: null
    }
  },
  watch: {
    searchTerm(newVal) {
      clearTimeout(this.searchTimeoutId)
      this.selected = null
      if (!newVal.trim()) {
        this.options = []
        return
      }
      this.searchTimeoutId = setTimeout(this.fetchMatches, 300)
    }
  },
  methods: {
    async fetchMatches() {
      this.loadingMatches = true
      try {
        const { data } = await axios.get(api.community.list, {
          params: { name: this.searchTerm.trim(), type : "forum", join: true, }
        })
        this.options = data.data
      } catch (e) {
        this.options = []
      } finally {
        this.loadingMatches = false
      }
    },
    selectForum(forum) {
      this.selected = forum
      this.error = ''
    },
    async submit() {
      if (!this.selected) return
      this.joining = true
      this.error = ''
      try {
        await axios.post(api.community.join, {
          id: this.selected.id,
          type: 'forum',
          user: localStorage.getItem("user_id")
        })
        this.$emit('done')
      } catch (e) {
        this.error = e.response?.data?.message || 'Error al unirse al foro'
      } finally {
        this.joining = false
      }
    }
  }
}
</script>

<style scoped>
.border {
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}
.list-group-item.active {
  background-color: #e7f1ff;
  border-color: #cfe2ff;
}
</style>
