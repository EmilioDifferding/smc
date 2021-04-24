import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import { apiFactory } from '@/api/apiFactory'
import { isValidJwt, EventBus } from '@/utils'
import axios from 'axios'

const usersApi = apiFactory.get('users')
export default new Vuex.Store({
  state: {
    users: [],
    isLoading: false,
    user: {},
    jwt: localStorage.getItem('token') || '',
  },
  mutations: {
    setUsers(state, payload){
      state.users = payload
    },
    setLoadingFalse(state, payload){
      state.isLoading = !state.isLoading
    },

    setUserData(state, payload){
      console.log('setUserData Payload = ', payload);
      state.userData = payload.userData
    },

    setJwtToken(state, payload){
      console.log('setJwtToken payload = ', payload)
      localStorage.token = payload.jwt.token
      state.jwt = payload.jwt.token
      }
  },
  actions: {
    async loadUsers (context){
      context.commit('setLoadingFalse')
      const { users } = await usersApi.get(localStorage.getItem('token'))
      context.commit('setLoadingFalse')
      return context.commit('setUsers', users);
    },
    login(context, userData){
      context.commit('setUserData', { userData });
      // console.log(userData)
      return usersApi.authenticate(userData)
        .then(response =>{
          console.log(response);
          context.commit('setJwtToken', {jwt: response});
        })
        .catch(error => {
          alert('error autenticando', error)
          EventBus.$emit('failedAuthentication', error)
        }) 
    }

  },
  getters: {
    isAuthenticated(state){
      state.jwt = localStorage.getItem('token')
      return isValidJwt(state.jwt)
    }
  },
  modules: {
  }
})
