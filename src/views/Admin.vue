<template>
  <v-btn @click="resetRank" :disabled="isSubmitting">Reset Rank</v-btn>
</template>

<script>
import * as api from "@/api";
export default {
  name: "home",
  data() {
    return {
      isSubmitting: false
    };
  },
  methods: {
    async resetRank() {
      this.isSubmitting = true;
      try {
        await api.quiz.resetRank();
        window.location.reload();
      } catch (err) {
        alert(err);
      }
      this.isSubmitting = false;
    }
  }
};
</script>
