<template>
    <div class="">
        <p>Tiene pendiente confirmar el registro con el bot de telegram</p>
        <b-button
            title="Confirmar el registro para recibir alertas del bot"
            @click="callback($event)"
        >Confirmar</b-button>

    </div>
</template>

<script>
export default {
    name:'RegistrationButton',
    methods:{
        callback: function (e) {
            this.$emit('click', e)
        }
    }

}
</script>

<style>

</style>