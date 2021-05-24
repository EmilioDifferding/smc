<template>
  <div class="container">
    <portlet-base title="Usuarios" subtitle="Listado">
      <template v-slot:head-actions>
        <router-link :to="{ name: 'users.create' }">
          <create-button></create-button>
        </router-link>
      </template>
      <b-table :data="table.rows">
        <b-table-column field="id" label="Id" v-slot="props">
          {{ props.row.id }}
        </b-table-column>
        <b-table-column field="name" label="Nombre" v-slot="props">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column field="email" label="E-mail" v-slot="props">
          {{ props.row.email }}
        </b-table-column>
        <b-table-column field="actions" label="Acciones" v-slot="props" v-if="['administrador'].includes(role)">
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
import { mapGetters } from "vuex";
import PortletBase from "../../components/portlets/PortletBase";
import CreateButton from "../../components/buttons/CreateButton";
import { apiFactory } from "../../api/apiFactory";
import users from "../../api/apis/users";
const usersApi = apiFactory.get("users");
export default {
  name: "UsersList",
  components: {
    PortletBase,
    CreateButton
  },
  data() {
    return {
      isLoading: false,
      users: []
    };
  },
  computed: {
    ...mapGetters({
      user: 'auth/user'
    }),
     role(){
      return this.user? this.user.role.name: null
    },
    table() {
      return {
        rows: this.users.map(obj => {
          let props = this.$router.resolve({
            name: "users.edit",
            params: { id: obj.id }
          });
          obj.to = props;
          return obj;
        })
      };
    }
  },
  methods: {
    async fetchUsers() {
      this.isLoading = true;
      try {
        let users = await usersApi.get();
        this.users = users.users;
        this.isLoading = false;
      } catch (error) {
        console.log(error);
        this.isLoading = false;
      }
    },
    async onDelete(id) {
      this.$buefy.dialog.confirm({
        message: `Seguro que desea borrar este elemento? la acción no puede deshacerse`,
        onConfirm: async () => {
          try {
            await usersApi.delete(id);
            this.fetchUsers();
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
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style>
</style>