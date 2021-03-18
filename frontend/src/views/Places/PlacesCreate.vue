<template>
  <portlet-base title="Lugares" subtitle="Crear">
    <places-form ref="form"> </places-form>
    <template v-slot:action-footer>
      <b-button
        type="is-success"
        expanded
        label="Guardar"
        icon-left="check-bold"
        @click.prevent="onSubmit()"
      >
      </b-button>
    </template>
  </portlet-base>
</template>

<script>
import PortletBase from "../../components/portlets/PortletBase";
import PlacesForm from "./PlacesForm";
import { apiFactory } from "../../api/apiFactory";
const placesApi = apiFactory.get("places");
export default {
  name: "PlacesCreate",
  components: {
    PortletBase,
    PlacesForm,
  },
  methods: {
    async onSubmit() {
      try {
        let formData = this.$refs.form.form;
        await placesApi.create(formData);
        this.$buefy.toast.open({
          message: `Operación Realizada`,
          type: "is-success",
        });
        this.$router.push({ name: "places" });
      } catch (error) {
        this.$buefy.toast.open({
          message: `Algo salio mal: ERROR: ${error}`,
          type: "is-danger",
        });
      }
    },
  },
};
</script>

<style>
</style>