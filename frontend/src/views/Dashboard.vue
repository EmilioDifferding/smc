<template>
  <div>
    <div class="mobile-header p-2 pl-6 has-background-light">
      <div class="level is-mobile">
        <div class="level-left">
          <div class="level-item">
            <h1 class="title"><a href="/dispositivos"> SMC FCAL </a></h1>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <b-button @click="open = !open"><b-icon icon='menu'></b-icon></b-button>
          </div>
        </div>
      </div>
    </div>
    <div class="sidebar-page is-flex">
      <section class="sidebar-layout">
        <b-sidebar
          :position="position"
          :mobile="mobile"
          fullheight
          type="is-light"
          v-model="open"
          can-cancel
        >
          <div class="p-1 full-height" >
            <div class="block">
              <div class="level is-mobile hide-on-mobile">
                <div class="level-left"></div>
                <div class="level-right">
                  <div @click="open = !open"  class="level-item"><b-button  type="is-info"><b-icon icon="window-close" ></b-icon></b-button></div>
                </div>
              </div>
              <h1 class="title is-4">Menú</h1>
            </div>
            <div class="container">

              <div class="level is-mobile">
                <div class="level-left">
                  <h3 class="subtitle is-inline-flex"> <b-icon icon="account"></b-icon>  {{user.name}}</h3>
                </div>
                <div class="level-right">
                  <a class="p-1" @click="onLogout"><b-icon icon="logout"></b-icon></a>
                </div>
              </div>
            </div>
            <div class="container has-background-warning has-text-centered mt-3" v-if="hasPendings" @click="onConfirmRegister">
              <registration-button></registration-button>
            </div>
            <hr>
            <b-menu class="is-custom-mobile" :activable="activable">
              <b-menu-list>
                <b-menu-item
                  :to="{name:'devices'}"
                  tag="router-link"
                  icon="memory"
                  label="Dispositivos"
                ></b-menu-item>
                <b-menu-item  v-if="['administrador'].includes(role)"
                  :to="{name:'users'}"
                  tag="router-link"
                  icon="account"
                  label="Usuarios"
                ></b-menu-item>
                <b-menu-item v-if="['administrador'].includes(role)"
                  :to="{name:'places'}"
                  tag="router-link"
                  icon="map-marker-multiple"
                  label="Lugares"
                ></b-menu-item>
                <b-menu-item v-if="['administrador'].includes(role)"
                  :to="{name:'units'}"
                  tag="router-link"
                  icon="speedometer-medium"
                  label="Unidades"
                ></b-menu-item>
              </b-menu-list>
              
            </b-menu>
          </div>
        </b-sidebar>

        <div class="container">
          <router-view />
        </div>
      </section>
    </div>
    <!-- <sidebar></sidebar> -->
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
import RegistrationButton from '../components/buttons/RegistrationButton'
import {apiFactory} from '../api/apiFactory'
const usersApi = apiFactory.get('users')
export default {
  name:'Dashboard',
  components:{
    RegistrationButton,
  },
  data() {
    return {
      position:'static',
      expanOnHover: false,
      mobile: "fullwidth",
      reduce: false,
      activable: false,
      active:false,
      hasPendings:false,
      regData:{},
      open: false,
    };
  },
  methods:{
    ...mapActions({logout:'auth/logout'}),
    onLogout(){
      this.logout();
      this.$router.replace({name:'Login'})
    },
    async checkPendings(){
      let data = await usersApi.getPendings()
      this.hasPendings = data.is_pending
      this.regData = data
      
    },
    async onConfirmRegister(){
      try{
        let res = await usersApi.applyPendings(this.regData)
        this.regData={}
        this.hasPendings=false
        alert(res.msg)
      }catch(error){
        console.error(error);
      }
    },
  },
  computed:{
    ...mapGetters({
      user: 'auth/user'
    }),
     role(){
      return this.user? this.user.role.name: null
    }
  },
  mounted(){
    this.checkPendings()
  }
  
 
};
let cosas = document.querySelector('.sidebar-page');
console.log(cosas);
</script>

<style lang="scss" scoped>
.p-1 {
  padding: 1em;
}
.full-height{
  min-height: 100vh;
}
.sidebar-page {
  display: flex;
  flex-direction: column;
  width: 100%;
  // min-height: 100%;
  min-height: 100vh;
  .sidebar-layout {
    display: flex;
    flex-direction: row;
    background-color: #fff;
    min-height: 100vh;
  }
}
@media screen and (max-width: 1023px) {
  .b-sidebar {
    .sidebar-content {
      &.is-mini-mobile {
        &:not(.is-mini-expand),
        &.is-mini-expand:not(:hover) {
          .menu-list {
            li {
              a {
                span:nth-child(2) {
                  display: none;
                }
              }
              ul {
                padding-left: 0;
                li {
                  a {
                    display: inline-block;
                  }
                }
              }
            }
          }
          .menu-label:not(:last-child) {
            margin-bottom: 0;
          }
        }
      }
    }
  }
}
@media screen and (min-width: 1024px) {
  .b-sidebar {
    .sidebar-content {
      &.is-mini {
        &:not(.is-mini-expand),
        &.is-mini-expand:not(:hover) {
          .menu-list {
            li {
              a {
                span:nth-child(2) {
                  display: none;
                }
              }
              ul {
                padding-left: 0;
                li {
                  a {
                    display: inline-block;
                  }
                }
              }
            }
          }
          .menu-label:not(:last-child) {
            margin-bottom: 0;
          }
        }
      }
    }
  }
}
.is-mini-expand {
  .menu-list a {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
@media screen and (min-width: 1024px){
  .hide-on-mobile{
    display: none;
  }
}
</style>
