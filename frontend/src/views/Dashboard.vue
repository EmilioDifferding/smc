<template>
    <div class="sidebar-page">
      <section class="sidebar-layout">
        <b-sidebar
          position="static"
          :mobile="mobile"
          :reduce="reduce"
          type="is-light"
          open
        >
          <div class="p-1 full-height">
            <div class="block">
              <h1 class="title">SMC FCAL</h1>
            </div>
            <div class="container">

              <div class="level">
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
            <b-menu class="is-custom-mobile" :activable="false">
              <b-menu-list>
                <b-menu-item
                  :to="{name:'devices'}"
                  tag="router-link"
                  icon="memory"
                  label="Dispositivos"
                ></b-menu-item>
                <b-menu-item v-if="['administrador'].includes(role)"
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
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
import RegistrationButton from '../components/buttons/RegistrationButton'
import {apiFactory} from '../api/apiFactory'
const usersApi = apiFactory.get('users')
export default {
  name:'Dashboard',
  components:{
    RegistrationButton
  },
  data() {
    return {
      expanOnHover: false,
      mobile: "reduced",
      reduce: false,
      activable: false,
      active:false,
      hasPendings:false,
      regData:{},
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
</script>

<style lang="scss" scoped>
.p-1 {
  padding: 1em;
}
.full-height{
  height: 100vh;
  // background-color: green;
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
</style>
