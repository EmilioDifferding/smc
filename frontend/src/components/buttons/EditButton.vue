<template>
    <div>
        <a @click="callback($event)"
           :href="url"
        >
            <b-button type="is-info" size="is-small" title="Editar">
                <b-icon icon="pencil"></b-icon>
            </b-button>
        </a>
    </div>
</template>

<script>
    export default {
        name: "EditButton",
        props: {
            url: {
                type: String,
                default: '#'
            },
        },
        methods: {
            callback: function(e) {
                this.$emit('click', e)
            }
        }
    }
</script>

<style scoped>

</style>
