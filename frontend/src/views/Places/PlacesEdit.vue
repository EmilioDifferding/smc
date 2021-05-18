<template>
  <portlet-base title="Lugares" subtitle="Editar" v-if="place">
    <places-form :place="place" ref="form"></places-form>

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
</template>

<script>
import PortletBase from "../../components/portlets/PortletBase.vue";
import PlacesForm from "./PlacesForm.vue";

import { apiFactory } from "../../api/apiFactory";
const placesApi = apiFactory.get("places");

export default {
  components: {
    PortletBase,
    PlacesForm,
  },
  data() {
    return {
      place: null,
    };
  },
  methods: {
    async getResource() {
      try {
        const data = await placesApi.find(this.$route.params.id);
        this.place = data;
      } catch (error) {
       this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger",
        });
      }
    },
    async onSubmit() {
      try {
        let formData = this.$refs.form.form;
        console.log(this.place.id)
        await placesApi.update(this.place.id, formData);
        this.$buefy.toast.open({
          message: `Operación Realizada`,
          type: "is-success"
        });
        this.$router.push({ name: "places" });
      } catch (error) {
        this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger",
        });
      }
    },
  },
  created() {
    this.getResource();
  },
};
</script>

<style>
</style>