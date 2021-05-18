import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import { apiFactory } from '@/api/apiFactory'
import { isValidJwt, EventBus } from '@/utils'
import axios from 'axios'

const usersApi = apiFactory.get('users')
export default new Vuex.Store({
  state: {
    user: null,
    jwt: localStorage.getItem('token') || '',
  },

  actions: {
    login(context, userData){
      /**
       * envia las credenciales al server,
       * si es aprovado devuelve el token y el objeto user
       * llama a las mutaciones setJwt y SetUser
       */
      // console.log(userData)
      return usersApi.authenticate(userData)
        .then(response =>{
          console.log(`RESPONSE:`);
          console.log(response)
          context.commit('setJwtToken', {jwt: response});
          context.commit('setUserData', response.user)
        })
        .catch(error => {
          alert('error autenticando', error)
          EventBus.$emit('failedAuthentication', error)
        }) 
    },

    auth ({commit}){
      // if (this.getters.isAuthenticated){
      //   commit('setJwtToken', localStorage.getItem('token'))

      // }
    }
  },


  mutations: {
    setUserData(state, payload){
      console.log('setUserData Payload = ', payload);
      localStorage.setItem('user', JSON.stringify(payload))
      state.user = payload
    },
    setJwtToken(state, payload){
      console.log('setJwtToken payload = ', payload)
      localStorage.token = payload.jwt.token
      state.jwt = payload.jwt.token
      }
  },

  getters: {
    isAuthenticated: state => {
      state.jwt = localStorage.getItem('token')
      return isValidJwt(state.jwt)
    },

    user: state => {
      return state.user; 
    }
  },
  modules: {
  }
})
