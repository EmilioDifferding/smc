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
            <b-menu class="is-custom-mobile" :activable="false">
              <b-menu-list>
                <b-menu-item
                  class="sidebarmenu__item"
                  v-for="row in sidebarItems"
                  :key="row.name"
                  @click="currentRow = row"
                  :icon="row.icon"
                  :tag="row.tag"
                  :to="row.to"
                  :label="row.name"
                >

                </b-menu-item>
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
export default {
  data() {
    return {
      expanOnHover: false,
      mobile: "reduced",
      reduce: false,
      activable: false,
      active:false,
      sidebarItems:[
        {
          name:'Dispositivos',
          icon: 'memory',
          to: {name: 'devices'},
          tag: 'router-link'
        },
        {
          name:'Lugares',
          icon: 'map-marker-multiple',
          to: {name: 'places'},
          tag: 'router-link'
        },
        {
          name:'Unidades',
          icon: 'speedometer-medium',
          to: {name: 'units'},
          tag: 'router-link'
        }

      ]
    };
  },
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
