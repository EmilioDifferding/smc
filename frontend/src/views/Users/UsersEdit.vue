<template>
  <div class="container">
    <portlet-base title="Usuarios" subtitle="Editar" v-if="user">
      <users-form :user="user" ref="form"></users-form>
      <template v-slot:action-footer>
        <b-button
          type="is-success"
          expanded
          label="Guardar"
          icon-left="check-bold"
          @click.prevent="onSubmit()"
        ></b-button>
      </template>
    </portlet-base>
  </div>
</template>

<script>
import UsersForm from "./UsersForm";
import PortletBase from "../../components/portlets/PortletBase";
import { apiFactory } from "../../api/apiFactory";
const usersApi = apiFactory.get("users");
export default {
  name: "UserEdit",
  components: {
    PortletBase,
    UsersForm
  },
  data() {
    return {
      user: null
    };
  },
  methods: {
    async getResource() {
      try {
        const data = await usersApi.find(this.$route.params.id);
        this.user = data;
      } catch (error) {
        this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger"
        });
      }
    },
    async onSubmit() {
      try {
        let formData = this.$refs.form.form;
        await usersApi.update(this.$route.params.id, formData);
        this.$buefy.toast.open({
          message: `Operación Realizada`,
          type: "is-success"
        });
        this.$router.push({ name: "users" });
      } catch (error) {
        console.log(error);
        this.$buefy.toast.open({
          message: `Algo salio mal ${error}`,
          type: "is-danger"
        });
      }
    }
  },
  created() {
    this.getResource();
  }
};
</script>

<style>
</style>