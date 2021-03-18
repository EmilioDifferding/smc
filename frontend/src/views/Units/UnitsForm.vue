<template>
  <div class="columns is-centered">
    <div class="mt-4 column">
      <b-field label-position="on-border" label="Nombre">
        <b-input
          v-model="form.name"
          id="name"
          placeholder="Ej. Corriente, Temperatura"
        >
        </b-input>
      </b-field>
    </div>
    
    <div class="mt-4 column">
      <b-field label-position="on-border" label="Simbolo">
        <b-input v-model="form.symbol" id="symbol" placeholder="Ej. A, mA, C">
        </b-input>
      </b-field>
    </div>
  </div>
</template>

<script>
export default {
  name: "UnitsForm",
  props: {
    unit: {
      type: Object,
      default() {
        return {
          id: "",
          name: "",
          symbol: "",
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
        name: this.unit.name,
        symbol: this.unit.symbol,
      };
    },
  },
  beforeMount() {
    this.form = this.mapToFormData();
  },
};
</script>

<style>
</style>