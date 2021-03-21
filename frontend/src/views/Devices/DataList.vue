<template>
  <div class="container">
    <portlet-base title="Datos de dispositivo" :subtitle="device.name ? device.name : null">
      <b-table v-if="aliasesColumns" :data="device.data" :columns="columns"> </b-table>
      <p v-if="!device.data.length">No data yet</p>
    </portlet-base>
  </div>
</template>

<script>
/**
 * @todo: Obtener todos los datos leidos por el dispositivo, conformar las columnas con todos los alias (medidas) que releva el dispositivo y ubicar esos datos de en orden cronologico inverso, agergar paginacion y boton de descarga de los datos en formato excel [ver libreria vue-json-excel o algo similar]
 */
import PortletBase from "../../components/portlets/PortletBase.vue";
import { apiFactory } from "../../api/apiFactory";
const devicesApi = apiFactory.get("devices");
export default {
  components: { PortletBase },
  name: "DataList",
  computed:{
    aliasesColumns(){
      // header columns rendering dinamically based on the aliases given
      if (this.device.data.length > 0){
        this.device.data[0].values.forEach((key, value) => {
          let new_column = {
            field: key.alias,
            label: key.alias,
          }
          this.columns.push(new_column)
        });
      }
      return true
    },
  },
  data() {
    return {
      columns: [
        {
          field: "id",
          label: "ID",
          numeric: true,
        },
        {
          field: "timestamp",
          label: "Fecha/Hora"
        },
      ],
      device: {
        data: [],
      },
    };
  },
  methods: {
    async getData() {
      try {
        const data = await devicesApi.getData(this.$route.params.id);
        // map every element to conform the [alias:value] pair to the same level as [values] to be correctly rendered on the table
        data.measurements.map((obj)=>{
          obj.values.forEach(v =>{obj[`${v.alias}`] = v.value})
        });
        this.device.data = data.measurements;
        this.device.name = data.name
        
        
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getData();
  },
};
</script>

<style>
</style>