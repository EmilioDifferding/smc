<template>
  <div class="section">
    <div class="columns is-centered">
      <div class="card column is-4">
        <div class="card-header">
          <h1 class="card-header-title is-centered title">Inicio de sesion</h1>
        </div>
        <div class="card-content">
          <form action="#" @submit.prevent="onSubmit">
            <b-field label="Email" label-position="on-border" label-for="email">
              <b-input v-model="formData.email" type="email" id="email" name="email"></b-input>
            </b-field>
            <b-field label-position="on-border" label="Contraseña" label-for="password">
              <b-input v-model="formData.password" type="password" name="password" id="password"></b-input>
            </b-field>
            <b-button type="is-success submit" expanded @click="onSubmit()">Iniciar</b-button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiFactory } from '../api/apiFactory'
const usersApi = apiFactory.get('users')
import {EventBus} from '../utils'
import {mapActions, mapGetters} from 'vuex'
export default {
  name:'Login',
  data(){
    return{
      formData:{
        name:'',
        email:'',
        password:''
      },
      errorMsg: ''
    }
  },
  methods: {
    ...mapActions({
      signIn: 'auth/signIn'
    }),
    async onSubmit(){
      try{
        await this.signIn(this.formData)
        .then(()=>this.$router.replace({name:'devices'}))
      }catch(error){
        console.log(error)
      }
    }
  },
  
  // mounted () {
  //   EventBus.$on('failedRegistering', (msg) => {
  //     this.errorMsg = msg
  //   })
  //   EventBus.$on('failedAuthentication', (msg) => {
  //     this.errorMsg = msg
  //   })
  // },
  // beforeDestroy () {
  //   EventBus.$off('failedRegistering')
  //   EventBus.$off('failedAuthentication')
  // }
}
</script>

<style>

</style>
