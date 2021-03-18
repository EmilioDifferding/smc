<template>
  <portlet-base title="Dispositivos" subtitle="crear">
    <device-form ref="form"> </device-form>
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
import DeviceForm from "./DeviceForm";
import { apiFactory } from "../../api/apiFactory";
const devicesApi = apiFactory.get("devices");

export default {
  name: "DeviceCreate",
  components: {
    PortletBase,
    DeviceForm,
  },
  methods: {
    async onSubmit() {
      try {
        let formData = this.$refs.form.form;
        await devicesApi.create(formData);
        this.$buefy.toast.open({
          message: `Operación Realizada`,
          type: "is-success",
        });
        this.$router.push({ name: "devices" });
      } catch (error) {
        this.$buefy.toast.open({
          message: `Algo salio mal ${error}`,
          type: "is-danger",
        });
      }
    },
  },
};
</script>

<style>
</style>