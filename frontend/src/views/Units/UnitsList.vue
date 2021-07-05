<template>
  <div class="container">
    <portlet-base title="Unidades" subtitle="Listado">
      <template v-slot:head-actions>
        <router-link :to="{ name: 'units.create' }">
          <create-button></create-button>
        </router-link>
      </template>

      <!-- <b-table :data="table.rows">
        <b-table-column field="id" label="ID" v-slot="props">
          {{ props.row.id }}
        </b-table-column>

        <b-table-column field="name" label="Nombre" v-slot="props">
          {{ props.row.name }}
        </b-table-column>

        <b-table-column field="symbol" label="Simbolo" v-slot="props">
          {{ props.row.symbol }}
        </b-table-column>

        <b-table-column field="actions" label="Acciones" v-slot="props">
          <router-link :to="props.row.to.href">
            <b-button type="is-info" size="is-small" title="Editar">
              <b-icon icon="pencil"></b-icon>
            </b-button>
          </router-link>

          <b-button
            type="is-danger"
            size="is-small"
            title="Eliminar"
            @click="onDelete(props.row.id)"
          >
            <b-icon icon="delete"></b-icon
          ></b-button>
        </b-table-column>

        <b-loading
          :can-cancel="false"
          :is-full-page="false"
          v-model="isLoading"
        ></b-loading>
      </b-table> -->
      <client-table
        :data="table"
        @delete='onDelete'
      ></client-table>
    </portlet-base>
  </div>
</template>

<script>
import CreateButton from "../../components/buttons/CreateButton.vue";
import PortletBase from "../../components/portlets/PortletBase.vue";
import { apiFactory } from "../../api/apiFactory";
import ClientTable from '../../components/tables/ClientTable.vue';
const unitsApi = apiFactory.get("units");

export default {
  name: "UnitsList",
  components: {
    ClientTable,
    PortletBase,
    CreateButton,
  },
  data() {
    return {
      isLoading: false,
      units: [],
      table: {
        rows:[],
        columns:[
          {
            label: "Id",
            field: "id",
            type: "number"
          },
          {
            label: "Nombre",
            field: "name",
          },
          {
            label:'Simbolo',
            field:'symbol',
          },
          {
            label: "Acciones",
            field: "actions",
            type: "actions",
            sortable:false,
            html: true
          }
        ],
      }
    };
  },

  methods: {
    async fetchTableData() {
      this.isLoading = true;
      try {
        const data = await unitsApi.get();
        this.units = data['units'];
        this.table.rows = this.mapTableRows(this.units)
        this.isLoading = false;
      } catch (error) {
        this.isLoading = false;
        this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger",
        });
      }
    },
    mapTableRows(data){
      return data.map(obj => {
        let props = this.$router.resolve({
          name:'places.edit',
          params:{id:obj.id}
        });
        obj.actions = {
          edit:{
            url: props.href
          },
          delete:{
            url:'#'
          }
        }
        return obj;
      })
    },
    async onDelete(id) {
      this.$buefy.dialog.confirm({
        message: `Seguro que quiere borrar este elemento?`,
        onConfirm: async () => {
          try {
            await unitsApi.delete(id);
            this.fetchTableData();
            this.$buefy.toast.open({
              message: "Se eliminó correctamente",
              type: "is-success",
            });
          } catch (error) {
            this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger",
        });
          }
        },
      });
    },
  },
  mounted() {
    this.fetchTableData();
  },
};
</script>

<style>
</style>