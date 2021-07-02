<template>
  <div class="" >
    <form @keydown.enter="enterPressed">
      
    <div class="columns is-centered">
      <div class="column is-4 mt-4">
        <b-field
          class="mb-4"
          label-position="on-border"
          label="Nombre de usuario"
        >
          <b-input v-model="form.name" id="username" required> </b-input>
        </b-field>
        <b-field
          class="mb-4"
          label-position="on-border"
          label="Correo electrónico"
        >
          <b-input v-model="form.email" type="email" id="email" required> </b-input>
        </b-field>
        <b-field class="mb-4" label-position="on-border" label="Contraseña">
          <b-input v-model="form.password" type="password" id="password" password-reveal>
          </b-input>
        </b-field>
      </div>
      <div class="column is-4 mt-4">
        <b-field class="mb-4" label-position="on-border" label="Telegram ID">
          <b-input
            type="number"
            id="telegram_id"
            v-model="form.telegram_id"
          ></b-input>
        </b-field>

        <b-field class="mb-4" label-position="on-border" label="Rol">
          <b-select placeholder="Seleccione Rol" v-model="form.role" expanded>
            <option v-for="role in roles" :value="role.id" :key="role.id">{{
              role.name
            }}</option>
          </b-select>
        </b-field>
      </div>
    </div>
    </form>


    <div class="section">
      <h1 class="title has-text-centered">Lista de dispositivos</h1>

      <b-table
        :data="devices"
        :columns="table.columns"
        :checked-rows.sync="checkedDevices"
        checkable
      >
      </b-table>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from "vuex";
  import { apiFactory } from "../../api/apiFactory";
  const usersApi = apiFactory.get("users");
  const devicesApi = apiFactory.get("devices");
  export default {
    name: "UsersForm",
    data() {
      return {
        form: {},
        roles: [],
        devices: [],
        checkedDevices: [],
      };
    },
    props: {
      user: {
        type: Object,
        default() {
          return {
            id: "",
            name: "",
            email: "",
            role: "1",
            devices: []
          };
        }
      }
    },
    computed: {
      ...mapGetters({
        userCreator: "auth/user"
      }),
      table() {
        return {
          columns: [
            {
              field: "id",
              label: "ID",
              numeric: true
            },
            {
              field: "name",
              label: "Nombre"
            },
            {
              field: "place.name",
              label: "Ubicación"
            }
          ],
          rows: this.devices
        };
      }
    },
    watch: {
      checkedDevices: function(oldValue, newValue) {
        this.form.devices = this.checkedDevices;
      }
    },

    methods: {
      enterPressed(event){
        let errors = [];
        errors.push(`<b class="has-text-warning">Verifique los siguientes datos</b>`)
        if (!this.form.name) {
          errors.push(`<li>Nombre es requerido</li>`)
        }
        if (!this.form.email) {
          errors.push(`<li>Email es requerido</li>`)
        }
        if(!this.user.id && !this.form.password){
          errors.push(`<li>Una contraseña es obligatoria!</li>`)
        }
        if(this.form.password && this.form.password.length < 8){
            errors.push(`<li>La contraseña debe tener almenos 8 caracteres</li>`)
          }
        if (errors.length > 1) {
          this.$buefy.snackbar.open({
                    message: `${errors.join('')}`,
                    type: 'is-danger',
                    position: 'is-top',
                    actionText: 'Ok',
                    indefinite: true,
                    
                })
        } else {
          this.$emit('onEnter', event)
        }
      },
      validateInputs(){},
      syncTable(items) {
        items.forEach(dev => {
          this.form.devices.forEach(fd => {
            if (fd.id === dev.id) {
              this.checkedDevices.push(dev);
            }
          });
        });
      },
      async fetchRoles() {
        let { roles } = await usersApi.getRoles();
        this.roles = roles;
      },
      async fetchDevices() {
        let { devices } = await devicesApi.get({ user: this.userCreator.id });
        this.devices = devices;
        return devices;
      },
      mapToFormData() {
        return {
          name: this.user.name,
          email: this.user.email,
          role: this.user.role.id? this.user.role.id: 2,
          telegram_id: this.user.telegram_id ? this.user.telegram_id : null,
          devices: this.user.devices
        };
      }
    },
    created() {
      this.form = this.mapToFormData();
      this.fetchRoles();
      this.fetchDevices().then(items => this.syncTable(items));
    }
  };
</script>

<style>
</style>