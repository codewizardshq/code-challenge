<template>
  <div class="quiz-scroll">
    <v-card flat>
      <div class="scroll-title">{{ title }}</div>
      <v-card-text v-html="question" />
    </v-card>
  </div>
</template>

<script>
import { Progress } from "@/store";

export default {
  name: "quizScroll",
  async mounted() {
    try {
      this.$store.dispatch("Progress/fetch");
    } catch (err) {
      this.$store.dispatch("Snackbar/showError", err);
    }
  },
  computed: {
    ...Progress.mapState(),
    title() {
      return this.Progress.hasData ? "Level " + this.Progress.rank : "Loading";
    },
    question() {
      return !(this.Progress.isLoading || !this.Progress.hasData)
        ? this.Progress.question
        : "Loading...";
    }
  }
};
</script>
