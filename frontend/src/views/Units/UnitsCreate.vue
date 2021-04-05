<template>
  <portlet-base title="Unidades" subtitle="Crear">
    <units-form ref="form"></units-form>
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
import PortletBase from "../../components/portlets/PortletBase.vue";
import UnitsForm from "./UnitsForm.vue";
import { apiFactory } from "../../api/apiFactory";
const unitsApi = apiFactory.get("units");
export default {
  name:'UnitsCreate',
  components: {
    PortletBase,
    UnitsForm,
  },
  methods: {
    async onSubmit(){
      try {
        let formData = this.$refs.form.form;
        await unitsApi.create(formData);
        this.$buefy.toast.open({
          message: `Operación Realizada`,
          type: "is-success",
        });
        this.$router.push({ name: "units" });
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

