<template>
  <div class="container">
    <portlet-base title="Usuarios" subtitle="Listado">
      <template v-slot:head-actions>
        <router-link :to="{ name: 'users.create' }">
          <create-button></create-button>
        </router-link>
      </template>
      <b-table :data="users">
        <b-table-column field="id" label="Id" v-slot="props">
            {{ props.row.id }}
        </b-table-column>
        <b-table-column field="name" label="Nombre" v-slot="props">
            {{ props.row.name }}
        </b-table-column>
        <b-table-column field="email" label="E-mail" v-slot="props">
            {{ props.row.email }}
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
import { mapState } from 'vuex'
import PortletBase from "../../components/portlets/PortletBase";
import CreateButton from "../../components/buttons/CreateButton";
export default {
  name: "UsersList",
  components: {
    PortletBase,
    CreateButton
  },
  data(){
      return {
        //   isLoading: false,
      }
  },
  computed: mapState({
          users: state => state.users,
          isLoading: state =>state.isLoading,
    }),
    beforeMount(){
        this.$store.dispatch('loadUsers')
    }

};
</script>

<style>
</style>