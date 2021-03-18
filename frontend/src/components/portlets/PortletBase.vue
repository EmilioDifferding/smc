<template>
  <section class="section">
    <div class="container ">
      <nav class="level">
        <div class="level-left">
          <div class="level-item">
            <h3>
              <span class="subtitle">{{ title }} </span> |
              <small>{{ subtitle }}</small>
            </h3>
          </div>
        </div>

        <div class="level-right">
          <div class="level-item">
            <slot name="head-actions"></slot>
          </div>
        </div>
      </nav>
    </div>

    <div class="section box mt-2">
      <slot></slot>
      <div class="columns is-right">
        <div class="column is-3 is-offset-9">
          <slot name="action-footer"></slot>
        </div>
      </div>
    </div>



  </section>
</template>

<script>
export default {
  name: "PortletBase",
  props: {
    id: String,
    title: String,
    subtitle: String,
  },
};
</script>

<style>
</style>