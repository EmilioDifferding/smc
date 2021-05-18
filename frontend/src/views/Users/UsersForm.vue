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
  </div>
</template>

<script>
export default {
  name: "UsersForm",
  data() {
    return { form: {} };
  },
  props: {
    user: {
      type: Object,
      default() {
        return {
          id: "",
          name: "",
          email: ""
        };
      },
    },
  },
  methods:{
    mapToFormData(){
      return{
        name: this.user.name,
        email: this.user.email,
      }
    }
  },
  mounted(){
    this.form = this.mapToFormData()
  }
};
</script>

<style>
</style>