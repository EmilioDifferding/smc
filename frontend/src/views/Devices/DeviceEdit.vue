<template>
  <portlet-base title="Dispositivo" subtitle="Editar" v-if="device">
    <device-form :device="device" ref="form"></device-form>
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
import DeviceForm from "./DeviceForm.vue";

import { apiFactory } from "../../api/apiFactory";
const devicesApi = apiFactory.get("devices");

export default {
  components: {
    PortletBase,
    DeviceForm
  },
  data() {
    return {
      device: null
    };
  },
  methods: {
    async getResource() {
      try {
        const data = await devicesApi.find(this.$route.params.id);
        this.device = data;
      } catch (error) {
        console.log("error");
      }
    },
    async onSubmit() {
      try {
        let formData = this.$refs.form.form;
        await devicesApi.update(this.$route.params.id, formData);
        this.$buefy.toast.open({
          message: `Operación Realizada`,
          type: "is-success"
        });
        this.$router.push({ name: "devices" });
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