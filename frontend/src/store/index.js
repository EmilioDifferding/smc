import Vue from 'vue'
import Vuex from 'vuex'
import {isValidJwt} from '@/utils'
import auth from './modules/auth'
Vue.use(Vuex)
export default new Vuex.Store({
    state:{

    },
    actions:{

    },
    mutations:{

    },
    getters:{

    },
    modules:{
        auth,
    }
})
