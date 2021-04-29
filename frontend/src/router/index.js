import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'

Vue.use(VueRouter)


import routes from './routes'
import store from '@/store'

const router = new VueRouter({
  mode: 'history',
  linkActiveClass: 'is-active',
  linkExactActiveClass: 'has-text-light',
  base: process.env.BASE_URL,
  routes
})
router.beforeEach ((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!store.getters['auth/isAuthenticated'] && to.name !== 'Login') {
        next({
          name: 'Login',
          params: { nextUrl: to.fullPath }
        });
      } else {
        next();
      }
      
  }else{
      next()
  }
})

export default router
