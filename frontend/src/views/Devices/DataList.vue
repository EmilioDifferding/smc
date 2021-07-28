<template>
  <div class="container">
    <portlet-base title="Datos de dispositivo" :subtitle="device.name ? device.name : null">
     
      <client-table
        :data="table"
      ></client-table>
    </portlet-base>
  </div>
</template>

<script>
import ClientTable from '../../components/tables/ClientTable.vue'
import PortletBase from "../../components/portlets/PortletBase.vue";
import { apiFactory } from "../../api/apiFactory";
const devicesApi = apiFactory.get("devices");
export default {
  components: { 
    PortletBase,
    ClientTable,
    },
  name: "DataList",
  computed:{
    aliasesColumns(){
      let columns = [
        {
          field: "id",
          label: "ID",
          numeric: true,
          sortable: true,
          firstSortType: 'desc'
        },
        {
          field: "timestamp",
          label: "Fecha/Hora",
          sortable: true,
        },
      ];
      // header columns rendering dinamically based on the aliases given
      if (this.device.data.length > 0){
        this.device.data[0].values.forEach((key, value) => {
          let new_column = {
            field: key.alias,
            label: key.alias,
          }
          columns.push(new_column)
          console.log(columns)
        });
      }
      // this.table.columns = this.columns//.push(new_column)
      // return true
      return columns
    },
  },
  data() {
    return {
      isPaginated:true,
      isPaginationSimple:true,
      perPage:10,
      
      device: {
        data: [],
      },
      table:{
        rows:[],
        columns:[]
      }
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
        this.table.rows = data.measurements
        this.table.columns = this.aliasesColumns;
        this.device.name = data.name
        
      } catch (error) {
        this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger",
        });
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