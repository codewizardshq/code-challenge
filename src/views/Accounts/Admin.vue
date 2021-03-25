<template>
  <v-container>
    <v-btn @click="resetRank" :disabled="isSubmitting">Reset Rank</v-btn>
    <v-btn @click="syncQuestions" :disabled="loading" :loading="loading"
      >Sync Questions</v-btn
    >
  </v-container>
</template>

<script>
import * as api from "@/api";
export default {
  name: "home",
  data() {
    return {
      isSubmitting: false,
      loading: false
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
    },

    async syncQuestions() {
      this.loading = true;
      try {
        await api.quiz.syncQuestions();
        alert("Done");
      } catch (e) {
        alert(e.message);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
