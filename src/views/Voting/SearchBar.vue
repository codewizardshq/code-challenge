<template>
  <div>
    <v-text-field outlined light prepend-inner-icon="mdi-magnify" placeholder="Search by name" v-model="text"></v-text-field>
  </div>
</template>

<script>
import * as api from '@/api';
export default {
  data() {
    return {
      text: ''
    };
  },
  watch: {
    text(text) {
      api.voting.search(text);
    }
  }
};
</script>

<style scoped></style>
