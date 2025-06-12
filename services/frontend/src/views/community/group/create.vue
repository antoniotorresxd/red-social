<template>
  <div class="pull-left border rounded p-4" style="max-width: 400px">
    <h5 class="mb-4">Crear Grupo</h5>
    <form @submit.prevent="submit">
      <div class="mb-4">
        <label
          for="group-name"
          class="form-label text-uppercase"
          style="font-size: 0.85rem"
        >
          Nombre del grupo
        </label>
        <input
          id="group-name"
          v-model="name"
          type="text"
          class="form-control"
          placeholder="Ingresa el nombre del grupo"
          :disabled="loading"
        />
      </div>

      <div v-if="error" class="text-danger mb-3">{{ error }}</div>

      <div class="text-center">
        <button
          type="submit"
          class="btn btn-outline-primary"
          :disabled="!name.trim() || loading"
          style="min-width: 100px"
        >
          {{ loading ? "Creando..." : "Crear" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import api from "@/router/api";

export default {
  name: "CreateGroupForm",
  data() {
    return {
      name: "",
      loading: false,
      error: "",
    };
  },
  methods: {
    async submit() {
      if (!this.name.trim()) return;
      this.loading = true;
      this.error = "";
      try {
        const group = await axios.post(api.community.create, {
          name: this.name.trim(),
          type: "group",
          admin_id: localStorage.getItem("user_id"),
        });

        const noti = {
          id: Date.now(),
          user_id: localStorage.getItem("user_id"),
          title: "Grupo creado",
          message: `Se ha creado el grupo. Su código es: ${group.data.data.code}`,
          type: "all",
          created_at: new Date().toISOString(),
          read: false,
        };
        localStorage.setItem("new_notification", JSON.stringify(noti));
        window.dispatchEvent(
          new CustomEvent("show-notification", { detail: noti })
        );

        this.$emit("done");
      } catch (e) {
        let errorMsg = e.response?.data?.message;
        if (errorMsg) {
          const match = errorMsg.match(/string='([^']+)'/);
          this.error = match ? match[1] : "Error al crear el grupo";
        } else {
          this.error = "Error al crear el grupo";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.border {
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}
</style>
