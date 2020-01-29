<template>
  <v-card tile flat>
    <v-toolbar color="secondary" dark flat>
      <v-toolbar-title>
        <slot name="title"></slot>
      </v-toolbar-title>
    </v-toolbar>
    <slot></slot>
  </v-card>
</template>

<script>
export default {};
</script>
