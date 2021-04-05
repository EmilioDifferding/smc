<template>
  <div class="container">
    <portlet-base title="Datos de dispositivo" :subtitle="device.name ? device.name : null">
      <b-select
        v-model="perPage"
      >
      <option value="10" >10 por página</option>
      <option value="50">50 por página</option>
      <option value="100">100 por página</option>
      </b-select>
      <b-table 
        v-if="aliasesColumns" 
        :data="device.data" 
        :columns="columns"
        :per-page="perPage"
        :paginated="isPaginated"
        pagination-position="top"
        default-sort="id"
        sort-icon="arrow-down"
        default-sort-direction="desc"
      > </b-table>
      <p v-if="!device.data.length">No data yet</p>
    </portlet-base>
  </div>
</template>

<script>
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
      isPaginated:true,
      isPaginationSimple:true,
      perPage:10,
      columns: [
        {
          field: "id",
          label: "ID",
          numeric: true,
          sortable: true,
        },
        {
          field: "timestamp",
          label: "Fecha/Hora",
          sortable: true,
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