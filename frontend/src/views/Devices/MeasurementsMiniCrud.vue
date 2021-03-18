<template>
  <!-- Aliases and alerts configuration -->
  <div class="column is-full has-lineup has-linedown pt-5">
    <div class="columns">
      <div class="column is-3">
        <b-field :label-position="labelPosition" label="Unidad">
          <b-select 
            expanded 
            placeholder="Seleccione"
            :loading="loadingUnits" 
            v-model="measurement.unit"
            >
            <option v-for="unit in units" :value="unit" :key="unit.id">
              {{ unit.name }}({{unit.symbol}})
            </option>
          </b-select>
        </b-field>
      </div>

      <div class="column is-3">
        <b-field :label-position="labelPosition" label="Alias">
          <b-input placeholder="Sensor 1" v-model="measurement.alias">
          </b-input>
        </b-field>
      </div>

      <div class="column">
        <b-field>
          <b-switch :type="switchType" :left-label="true" v-model="alerts">
            Alertas
          </b-switch>
        </b-field>
      </div>
      <div class="column" v-if="alerts">
        <b-field
          label="Min."
          :label-position="labelPosition"
          title="Alerta por valor bajo"
        >
          <b-input v-model="measurement.min_limit"></b-input>
        </b-field>
      </div>
      <div class="column" v-if="alerts">
        <b-field
          label="Máx."
          :label-position="labelPosition"
          title="Alerta por valor alto"
        >
          <b-input v-model="measurement.max_limit"></b-input>
        </b-field>
      </div>
      <div class="column">
        <b-button outlined type="is-primary" @click.prevent="addNewItem"
          >Agregar medida</b-button
        >
      </div>
    </div>
  </div>
  <!-- End Aliases and alerts Configurations -->
</template>

<script>
import { apiFactory } from "../../api/apiFactory";
const unitsApi = apiFactory.get("units");
export default {
  name: "MeasurementsMiniCrud",
  data() {
    return {
      labelPosition: "on-border",
      switchType: "is-success",

      loadingUnits: false,
      units: [],

      alerts: false,
      measurement: {
        unit: {},
        alias: null,
        max_limit: null,
        min_limit: null,
        alert: this.alerts,
      },
    };
  },
  methods: {
    async loadUnits(){
      this.loadingUnits = true;
      try {
        const data = await unitsApi.get();
        this.units = data['units'];
        this.loadingUnits = false;
      } catch (error) {
        this.loadingUnits = false;
        console.log(error)
      }
    },
    addNewItem() {
      this.$emit("on-new-item", this.measurement);
      this.measurement = {
        unit: null,
        alias: null,
        min_limit: null,
        max_limit: null,
        alert: false,
      };
      this.loadUnits()
      this.alerts = false;
    },
  },
  created(){
    this.loadUnits()
  }
};
</script>

<style>
</style>