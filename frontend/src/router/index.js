import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'

Vue.use(VueRouter)


import routes from './routes'
// const routes = [
//   {
//     path: '/',
//     name: 'Home',
//     component: Home
//   },
  
// ]

const router = new VueRouter({
  mode: 'history',
  linkActiveClass: 'is-active',
  linkExactActiveClass: 'has-text-light',
  base: process.env.BASE_URL,
  routes
})

export default router
