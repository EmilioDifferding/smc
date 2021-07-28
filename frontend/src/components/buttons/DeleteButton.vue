<template>
  <b-button
    type="is-danger"
    size="is-small"
    title="Eliminar"
    @click="callback($event)"
  >
    <b-icon icon="delete"></b-icon>
  </b-button>
</template>

<script>
export default {
  name: "DeleteButton",
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
};
</script>

<style>
</style>