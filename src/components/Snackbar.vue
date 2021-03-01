<template>
  <v-snackbar v-model="isOpen" :color="color">
    {{ Snackbar.text }}
  </v-snackbar>
</template>

<script>
import { Snackbar } from "@/store";

export default {
  data() {
    return {
      isOpen: false
    };
  },
  watch: {
    "Snackbar.isOpen"(value) {
      if (this.isOpen !== value) {
        this.isOpen = value;
      }
    },
    async isOpen(value) {
      if (this.Snackbar.isOpen !== value) {
        await this.$store.dispatch("Snackbar/isOpen", value);
      }
    }
  },
  computed: {
    ...Snackbar.mapState(),
    color() {
      return Snackbar.color;
    }
  }
};
</script>
