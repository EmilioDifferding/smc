<template>
    <div class="columns is-multiline" v-if="form">
      <div class="column is-3">
        <b-field :label-position="labelPosition" label="Nombre">
          <b-input
            placeholder="Ej. Ultra Freezer"
            v-model="form.name"
          > </b-input>
        </b-field>
      </div>

      <div class="column is-3">
        <b-field :label-position="labelPosition" label="ID único">
          <b-input 
            placeholder="Dirección MAC"
            v-model="form.unic_id"
            > </b-input>
        </b-field>
      </div>

      <div class="column is-3">
        <b-field :label-position="labelPosition" label="Ubicación">
          <b-select 
          expanded
          placeholder="Seleccione"
          :loading="loadingPlaces"
          v-model="form.place"
          >
          <option 
          v-for="place in places"
          :value="place.id"
          :key="place.id"
          >
            {{place.name}}
          </option>
          </b-select>
        </b-field>
      </div>

      <measurements-mini-crud @on-new-item="addToTable($event)"></measurements-mini-crud>
      
      <!-- List of added measurements to the device -->
      <div class="pt-5 column is-full">
        <p class="title is-6">Lista de medidas</p>
        <b-table :data="aliases">
          <b-table-column field="unit" label="Unidad" v-slot="props">
            {{props.row.unit.name}} ({{props.row.unit.symbol}})
          </b-table-column>
          <b-table-column field="alias" label="Alias" v-slot="props">
            {{props.row.alias}}
          </b-table-column>
          <b-table-column field="min_limit" label="Valor mínimo" v-slot="props">
            <span v-if="props.row.min_limit">{{props.row.min_limit}}</span>
            <span class="has-text-grey-light" v-else> -sin valor- </span>
          </b-table-column>
          <b-table-column field="max_limit" label="Valor máximo" v-slot="props">
            <span v-if="props.row.max_limit">{{props.row.max_limit}}</span>
            <span class="has-text-grey-light" v-else> -sin valor- </span>
          </b-table-column>
          <b-table-column field="actions" label="Acciones" v-slot="props">
            <b-button type="is-danger" size="is-small" @click="deleteItem(props.row.alias)" >
              <b-icon icon="delete" ></b-icon>
            </b-button>
          </b-table-column>
        </b-table>
      </div>

    </div>

</template>

<script>
import MeasurementsMiniCrud from './MeasurementsMiniCrud'
import { apiFactory} from '../../api/apiFactory'
const placesApi = apiFactory.get('places')
const devicesApi = apiFactory.get('devices')
export default {
  name: "DeviceForm",
  components:{
    MeasurementsMiniCrud,
  },
  props:{
    device:{
      type: Object,
      default(){
        return{
          id:'',
          name:'',
          unic_id:'',
          place:'',
          aliases:[],
        }
      }
    }
  },
  // computed:{
  //   ms(){
  //     this.form.aliases=this.device.aliases
  //   }
  // },
  data() {
    return {
      loadingPlaces:false,
      labelPosition: "on-border",
      switchType: "is-success",

      form:{},
      aliases:[],
      places:[],
      selectedPlace:null,
      units:[],
    };
  },
  methods: {
    async loadPlaces(){
      this.loadingPlaces = true;
      try {
        const data = await placesApi.get();
        this.places = data['places'];
        this.loadingPlaces = false;
      } catch (error) {
        this.loadingPlaces=false
        console.log(error)
      }
    },

    addToTable(item){
      this.aliases.push(item);
      this.form.aliases=this.aliases;
    },
    deleteItem(item){
      this.aliases = this.aliases.filter( i => i.alias !== item);
      this.form.aliases = this.aliases
      console.log("DELETED", item)
    },
    mapToFormData(){
        this.loadAliases();
        return{
          name: this.device.name? this.device.name:'',
          unic_id: this.device.unic_id? this.device.unic_id: '',
          place: this.device.place? this.device.place.id :  null,
          aliases: this.aliases,
      }
    },
    loadAliases(){
      if (this.device.aliases.length > 0 ) {
        this.device.aliases.forEach(item => {
          item.alias = item.alias ? item.alias : item.name
          this.addToTable(item)
        });
      }
    }
  },
  created(){
    this.loadPlaces()
    this.form = this.mapToFormData()
    // this.ms
  }
};
</script>

<style lang="scss" >
  .has-lineup{
    border-top: 2px solid #eee;
  }
  .has-linedown{
    border-bottom: 2px solid #eee;
  }
</style>