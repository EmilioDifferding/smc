import axios from "axios";
import {apiFactory} from '../../api/apiFactory'
const usersApi = apiFactory.get('users')
export default {
    namespaced: true,

    state: {
        authenticated: false,
        user: null,
        token: '',
    },
    getters:{
        isAuthenticated: state =>{
            return state.authenticated
        },
        user: state => {
            return state.user
        },
        token: state => {
            return state.token
        }
    },
    mutations: {
        SET_AUTHENTICATED (state, value){
            state. authenticated = value;
        },
        SET_USER (state, obj){
            localStorage.setItem('user',JSON.stringify(obj))
            state.user = obj;
        },
        SET_TOKEN (state, value){
            console.log('SETTING TOKEN')
            localStorage.setItem('token', value)
            state.token = value
        }
    },
    actions: {
        async signIn({ commit, dispatch }, credentials){
            try {
                response =  await usersApi.authenticate(credentials)
                .then(res =>{
                    commit('SET_TOKEN', res.token)
                    localStorage.setItem('user',JSON.stringify(res.user))
                    return  dispatch('me')
                })
                
            } catch (error) {
                if (error.response) {
                    commit('SET_TOKEN', '')
                    commit('SET_USER', null)
                    console.error(error.response)
                }
            }
        },
        async me ({ commit }) {
            try {
                usersApi.showme().then(response =>{
                    if (response.status > 400){
                        throw e;
                    }
                    commit('SET_AUTHENTICATED', true);
                    commit('SET_USER', response);
                })
            } catch (e) {
                console.log('ME ERROR ')
                commit('SET_AUTHENTICATED', false);
                commit('SET_USER', null);
                commit('SET_TOKEN', '')
            }
        },
    }
}
function isValidJwt (jwt){
    if (!jwt || jwt.split('.').length < 3){
        return false
    }
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
}