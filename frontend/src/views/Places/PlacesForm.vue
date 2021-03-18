<template>
  <div class="columns is-centered">
    <b-field class="mt-4" label-position="on-border" label="Nombre">
      <b-input
        v-model="form.name"
        
        placeholder="Ej. Laboratirio Química"
      ></b-input>
    </b-field>
  </div>
</template>

<script>
export default {
  name: "PlacesForm",
  props: {
    place: {
      type: Object,
      default() {
        return {
          id: "",
          name: "",
        };
      },
    },
  },
  data() {
    return {
      form: {},
    };
  },
  methods: {
    mapToFormData() {
      return {
        name: this.place.name,
      };
    },
  },
  mounted() {
    this.form = this.mapToFormData();
  },
};
</script>

<style>
</style>