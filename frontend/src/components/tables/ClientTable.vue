<template>
  <vue-good-table
    :columns='columns'
    :group-options='groupOptions'
    :rows='rows'
    :search-options="searchOptions"
    :pagination-options="paginationOptions"
  >
        <div class="" slot="emptystate"> Sin datos aún</div>
        <!-- <template slot="table-row" slot-scope="props">
            <span v-if="props.column.type=== 'actions'">
                <div class="buttons">
                    <edit-button
                        v-if="Object.keys(props.formattedRow[props.column.field]).includes('edit')"
                        :url="props.formattedRow[props.column.field].edit.url"
                        @click="onEdit(props.row.id)"
                    ></edit-button>

                    <delete-button v-if="Object.keys(props.formattedRow[props.column.field]).includes('delete')"
                                       @click="onDelete(props.row.id)"
                        ></delete-button>
                </div>
            </span>
        </template> -->
        <template slot="table-row" slot-scope="props">
                <span v-if="props.column.type === 'actions'">
                    <div class="is-flex">
                        <edit-button v-if="Object.keys(props.formattedRow[props.column.field]).includes('edit')"
                                     :url="props.formattedRow[props.column.field].edit.url"
                                     @click="onEdit(props.row.id)"
                        ></edit-button>
                        <delete-button v-if="Object.keys(props.formattedRow[props.column.field]).includes('delete')"
                                       @click="onDelete(props.row.id)"
                        ></delete-button>
                        
                    </div>
                </span>
                
                
            </template>
  </vue-good-table>
</template>

<script>
import 'vue-good-table/dist/vue-good-table.css';
import { VueGoodTable } from 'vue-good-table';
import EditButton from '../buttons/EditButton.vue';
import DeleteButton from '../buttons/DeleteButton.vue';
export default {
    name: 'ClientTable',
    components:{
        VueGoodTable,
        DeleteButton,
        EditButton,
    },
    props: {
        data:{
            type:Object,
            default: function () {
                return {
                    columns: [],
                    rows: [],
                }
            },
            
        },
        searchEnabled: {
                type: Boolean,
                default: true,
            }
    },
    data(){
        return {
            groupOptions: {
                enabled: true,
                headerPosition: 'bottom',
            },
            searchOptions: {
                enabled: this.searchEnabled,
                placeholder: 'Buscar...',
            },
            paginationOptions: {
                enabled: true,
                mode: 'records',
                perPage: 10,
                position: 'bottom',
                rowsPerPageLabel: 'Registros por página',
                perPageDropdown: [25, 50, 100],
                dropdownAllowAll: true,
                setCurrentPage: 1,
                nextLabel: 'siguiente',
                prevLabel: 'previo',
                ofLabel: 'de',
                pageLabel: 'página', // for 'pages' mode
                allLabel: 'Todos',
            },
        };
    },
    computed: {
        columns() {
            return this.data.columns
        },
        rows() {
            // footer
            let obj = {};
            // for (let i = 0; i < this.columns.length; i++) {
            // //     let matched = this.data.footers.find( obj => obj.field === this.columns[i].field );
            // //     obj[this.columns[i].field] = matched? matched.value: null;
                
            // }
            // // rows
            obj.children = this.data.rows;
            console.log(obj)
            return [obj];
            // return this.data.rows
        },
    },
    methods:{
        onEdit(id) {
            this.$emit("edit", id);
        },
        onDelete(id) {
            this.$emit("delete", id);
        },
    }
}
</script>

<style>

</style>