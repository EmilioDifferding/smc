<template>
  <b-button
    title="crear"
    type="is-info"
  >Nuevo</b-button>
</template>

<script>
export default {
    name:'CreateButton',
    props:{
        disabled:{
            type: Boolean,
            default: false
        },
    }
}
</script>

<style>

</style>