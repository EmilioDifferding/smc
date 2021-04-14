<template>
  <portlet-base title="Usuarios" subtitle="Crear">
    <users-form ref="form"></users-form>
    <template v-slot:action-footer>
      <b-button
        type="is-success"
        expanded
        label="Guardar"
        icon-left="check-bold"
        @click="onSubmit()"
      >
      </b-button>
    </template>
  </portlet-base>
</template>

<script>
import PortletBase from "../../components/portlets/PortletBase";
import UsersForm from "./UsersForm";
import { apiFactory } from "../../api/apiFactory";
const usersApi = apiFactory.get("users");
export default {
  name: "UsersCreate",
  components: {
    PortletBase,
    UsersForm
  },
  methods:{
    async onSubmit() {
      try {
        let formData = this.$refs.form.form;
        let response = await usersApi.create(formData);
        if (response.error){
          this.$buefy.toast.open({
          message:`${response.msg}`,
          type:'is-warning',
        });  
        }else{
            this.$buefy.toast.open({
              message:'Operación realizada.',
              type:'is-success',
            });
            this.$router.push({name:'users'})
          }
      } catch (error) {
        this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger",
        });
      }
    }
  }
};
</script>

<style>
</style>