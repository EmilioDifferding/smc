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
        let role = store.getters['auth/user'].role.name;
        if (to.matched.some(record => record.meta.requiresPermissions)) {
          to.matched.some(record => {
            if(record.meta.requiresPermissions) {
              let canGoNext = false;
              for (const [index, element] of record.meta.requiresPermissions.entries()){
                if (role === element){
                  canGoNext = true;
                  break;
                }
              };
              if (canGoNext){
                next()
              } else {
                next({name: 'devices'});
              }
            }
          })
        }
        next();
      }
      
  }else{
      next()
  }
})

export default router
