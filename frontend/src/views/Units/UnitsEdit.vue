<template>
  <portlet-base title="Unidades" subtitle="Editar" v-if="unit">
    <units-form :unit="unit" ref="form"></units-form>

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
import UnitsForm from "./UnitsForm.vue";

import { apiFactory } from "../../api/apiFactory";
const unitsApi = apiFactory.get("units");

export default {
  components: {
    PortletBase,
    UnitsForm,
  },
  data() {
    return {
      unit: null,
    };
  },
  methods: {
    async getResource() {
      try {
        const data = await unitsApi.find(this.$route.params.id);
        this.unit = data;
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
        console.log(this.unit.id)
        await unitsApi.update(this.unit.id, formData);
        this.$buefy.toast.open({
          message: `Operación Realizada`,
          type: "is-success"
        });
        this.$router.push({ name: "units" });
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