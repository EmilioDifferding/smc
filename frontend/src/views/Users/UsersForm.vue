<template>
  <div class="columns is-centered">
    <div class="column is-4 mt-4">
      <b-field
        class="mb-4"
        label-position="on-border"
        label="Nombre de usuario"
      >
        <b-input v-model="form.name" id="username"> </b-input>
      </b-field>
      <b-field
        class="mb-4"
        label-position="on-border"
        label="Correo electrónico"
      >
        <b-input v-model="form.email" type="email" id="email"> </b-input>
      </b-field>
      <b-field class="mb-4" label-position="on-border" label="Contraseña">
        <b-input v-model="form.password" type="password" id="password">
        </b-input>
      </b-field>
    </div>
    <div class="column is-4 mt-4">
      <b-field
      class="mb-4"
      label-position="on-border"
      label="Telegram ID">
        <b-input type="number" id="telegram_id" v-model="form.telegram_id"></b-input>
      </b-field>

      <b-field
        class="mb-4"
        label-position="on-border"
        label="Rol"
      >
        <b-select placeholder="Seleccione Rol" v-model="form.role" expanded>
          <option 
            v-for="role in roles"
            :value="role.id"
            :key="role.id"
          >{{role.name}}</option>
        </b-select>
      </b-field>
      
    </div>
  </div>
</template>

<script>
import {apiFactory} from '../../api/apiFactory';
const usersApi = apiFactory.get('users')
export default {
  name: "UsersForm",
  data() {
    return { 
      form: {},
      roles:[]
       };
  },
  props: {
    user: {
      type: Object,
      default() {
        return {
          id: "",
          name: "",
          email: "",
          role: '',
        };
      },
    },
  },
  methods:{
    async fetchRoles(){
      let {roles} = await usersApi.getRoles();
      this.roles = roles
    },
    mapToFormData(){
      return{
        name: this.user.name,
        email: this.user.email,
        role: this.user.role.id,
        telegram_id: this.user.telegram_id? this.user.telegram_id: null,
      }
    }
  },
  mounted(){
    this.form = this.mapToFormData()
    this.fetchRoles()
  }
};
</script>

<style>
</style>