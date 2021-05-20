import axios from "axios";
// axios.defaults.withCredentials = true;
import {apiFactory} from '../../api/apiFactory';
import api  from "../../api/api";
const usersApi = apiFactory.get('users');
axios.defaults.headers.common['Authorization'] = `Bearer: ${localStorage.getItem('token')}`
export default {
    namespaced: true,

    state: {
        user: JSON.parse(localStorage.getItem('user')) || null,
        token: localStorage.getItem('token') || '',
    },
    getters:{
        isAuthenticated: state =>{
            return isValidJwt(state.token)
        },
        user: state => {
            return state.user
        },
        token: state => {
            return state.token
        }
    },
    mutations: {
        SET_USER (state, obj){
            localStorage.setItem('user',JSON.stringify(obj))
            state.user = obj;
        },
        SET_TOKEN (state, value){
            console.log('SETTING TOKEN')
            api.defaults.headers.common['Authorization'] = `Bearer: ${value}`
            localStorage.setItem('token', value)
            state.token = value
        }
    },
    actions: {
        logout({commit}){
            commit('SET_USER', null)
            commit('SET_TOKEN', '')
        },
        async signIn({ commit, dispatch }, credentials){
            try {
                console.log("LOGIN IN...")
                await axios.post(`${process.env.VUE_APP_API_URL}login`, credentials).then(response =>{
                    console.log(response)
                    commit('SET_USER', response.data.user);
                    commit('SET_TOKEN', response.data.token);
                })
            } catch (error) {
                if (error.response) {
                    commit('SET_USER', null)
                    commit('SET_TOKEN', '')
                    console.error(error.response)
                }
            }
        },
        async me ({ commit }) {
            try {
                usersApi.showme().then(response =>{
                    console.log(response)
                })
            } catch (e) {
                console.log('ME ERROR ')
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
    console.log(exp - now)
    return now < exp
}