<template>
  <div class="container">
    <portlet-base title="Lugares" subtitle="Listado">
      <template v-slot:head-actions>
        <router-link :to="{ name: 'places.create' }">
          <create-button> </create-button>
        </router-link>
      </template>

      <b-table :data="table.rows">
        <b-table-column field="id" label="ID" v-slot="props">
          {{ props.row.id }}
        </b-table-column>
        <b-table-column field="name" label="Nombre" v-slot="props">
          {{ props.row.name }}
        </b-table-column>

        <b-table-column field="actions" label="Acciones" v-slot="props">
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
      </b-table>
    </portlet-base>
  </div>
</template>

<script>
import CreateButton from "../../components/buttons/CreateButton";
import PortletBase from "../../components/portlets/PortletBase";
import { apiFactory } from "../../api/apiFactory";
const placesApi = apiFactory.get("places");
export default {
  name: "PlacesList",
  components: {
    CreateButton,
    PortletBase
  },
  computed: {
    table() {
      return {
        rows: this.places.map(obj => {
          let props = this.$router.resolve({
            name: "places.edit",
            params: { id: obj.id }
          });
          obj.to = props;
          return obj;
        })
      };
    }
  },
  data() {
    return {
      isLoading: false,
      places: []
    };
  },
  methods: {
    async fetchTableData() {
      this.isLoading = true;
      try {
        const data = await placesApi.get();
        this.places = data["places"];
        this.isLoading = false;
      } catch (error) {
        this.isLoading = false;
        this.$buefy.toast.open({
          message: `<strong class="has-text-light">${error.title}</strong> <br> ${error.content}`,
          type: "is-danger"
        });
      }
    },

    async onDelete(id) {
      this.$buefy.dialog.confirm({
        message: `Seguro que quiere borrar este elemento?`,
        onConfirm: async () => {
          try {
            await placesApi.delete(id);
            this.fetchTableData();
            this.$buefy.toast.open({
              message: "Se eliminó correctamente",
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
  mounted() {
    this.fetchTableData();
  }
};
</script>

<style>
</style>