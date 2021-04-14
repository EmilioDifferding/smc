<template>
  <router-view></router-view>
</template>

<script>
import UsersList from './UsersList'
export default {
    name: 'UsersIndex',
    components: {
        UsersList,
    }
}
</script>

<style>

</style>