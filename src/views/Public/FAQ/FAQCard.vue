<template>
  <v-card-text>
    <v-card color="dark">
      <v-card-title><slot name="title"/></v-card-title>
      <v-card-text><slot /></v-card-text>
    </v-card>
  </v-card-text>
</template>

<script>
export default {};
</script>
