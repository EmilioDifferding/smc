<template>
  <div class="container">
    <portlet-base title="Dispositivos" subtitle="Listado">
      <template slot="head-actions" v-if="['administrador'].includes(role)">
        <router-link to="crear">
          <create-button> </create-button>
        </router-link>
      </template>
      <!-- <b-table :data="table.rows" class="pt-5">
        <b-table-column field="id" label="ID" v-slot="props">
          {{ props.row.id }}
        </b-table-column>
        <b-table-column field="name" label="Nombre" v-slot="props">
          <router-link :to="props.row.id + '/data'">
            {{ props.row.name }}
            <span> <b-icon type="is-success" icon="file-eye"></b-icon></span>
          </router-link>
        </b-table-column>
        <b-table-column field="unic_id" label="Código único" v-slot="props">
          {{ props.row.unic_id }}
        </b-table-column>
        <b-table-column field="place" label="Lugar" v-slot="props">
          {{ props.row.place.name }}
        </b-table-column>
        <b-table-column
          field="actions"
          label="Acciones"
          v-slot="props"
          v-if="['administrador'].includes(role)"
        >
          <div class="buttons">
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
              <b-icon icon="delete"></b-icon>
            </b-button>
          </div>
        </b-table-column>

        <b-loading
          :can-cancel="false"
          :is-full-page="false"
          v-model="isLoading"
        ></b-loading>
      </b-table> -->

      <client-table
        :data='table'
        @delete='onDelete'
      >
        
      </client-table>
    </portlet-base>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ClientTable from "../../components/tables/ClientTable.vue";
import PortletBase from "../../components/portlets/PortletBase";
import CreateButton from "../../components/buttons/CreateButton";
import { apiFactory } from "../../api/apiFactory";

const devicesApi = apiFactory.get("devices");
export default {
  name: "DeviceList",
  components: {
    PortletBase,
    CreateButton,
    ClientTable
  },
  data() {
    return {
      isLoading: false,
      devices: [],

      table: {
        columns: [
          {
            label: "Id",
            field: "id",
            type: "number"
          },
          {
            label: "Nombre",
            field: "name",
            html:true
          },
          {
            label: "Código",
            field: "unic_id"
          },
          {
            label: "Ubicación",
            field: "place.name"
          },
          {
            label: "Acciones",
            field: "actions",
            type: "actions",
            html: true
          }
        ],
        rows: []
      }
    };
  },
  computed: {
    ...mapGetters({
      user: "auth/user"
    }),
    role() {
      return this.user ? this.user.role.name : null;
    }
    // table() {
    //   return {
    //     rows: this.devices.map(obj => {
    //       let props = this.$router.resolve({
    //         name: "device.edit",
    //         params: { id: obj.id }
    //       });
    //       obj.to = props;
    //       return obj;
    //     })
    //   };
    // }
  },
  methods: {
    async fetchTableData() {
      this.isLoading = true;
      try {
        const data = await devicesApi.get({ user: this.user.id });
        this.devices = data["devices"];
        this.table.rows = this.mapTableRows(this.devices);
        this.isLoading = false;
      } catch (error) {
        this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`
            ? error.title
            : `${error}`,
          type: "is-danger"
        });
        this.isLoading = false;
      }
    },
    mapTableRows(data) {
      return data.map(obj => {
        let props = this.$router.resolve({
          name: "device.edit",
          params: { id: obj.id }
        });
        obj.actions = {
          edit: {
            url: props.href
          },
          delete: {
            url: "#"
          }
        };
        let dataProp = this.$router.resolve({
          name: 'device.data',
          params:{id:obj.id}
        })
        obj.name = `<a href="${dataProp.href}">
            ${obj.name}
            
          </a>`
        return obj;
      });
    },
    async onDelete(id) {
      this.$buefy.dialog.confirm({
        message: `Seguro que desea borrar este elemento? la acción no puede deshacerse`,
        onConfirm: async () => {
          try {
            await devicesApi.delete(id);
            this.fetchTableData();
            this.$buefy.toast.open({
              message: "El Dispositivo fue eliminado correctamente",
              type: "is-success"
            });
          } catch (error) {
            this.$buefy.toast.open({
              message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
              type: "is-danger"
            });
          }
        }
      });
    }
  },
  created() {
    this.fetchTableData();
  }
};
</script>

<style>
</style>