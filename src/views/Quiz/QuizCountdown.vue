<template>
  <div class="mt-6">
    <v-row justify="center">
      <quiz-scroll v-if="Quiz.awaitNextQuestion">
        <template v-slot:title>Next Challenge</template>
        <template v-slot:default>
          <div v-if="Quiz.awaitNextQuestion">
            Congratulations, {{ User.displayName }}!
            <br />
            You've conquered Level {{ User.rank }}.
            <br />
            <br />That's all the questions available for now.
            <br />
            The next question unlocks {{ Quiz.nextUnlockMoment.fromNow() }}
          </div>
          <div v-else>
            Congratulations, {{ User.displayName }}!
            <br />
            You've conquered Level {{ User.rank }}.
            <br />
            <br />
          </div>
        </template>
      </quiz-scroll>
      <quiz-scroll v-else-if="!Quiz.quizHasStarted">
        <template v-slot:title>Woah Slow Down!</template>
        <template v-slot:default>
          <p class="text-center">The challenge has not yet begun!</p>
          <p>Challenge begins: {{ Quiz.quizStartedMoment.fromNow() }}</p>
        </template>
      </quiz-scroll>
    </v-row>
    <quiz-need-help />
  </div>
</template>

<script>
import QuizNeedHelp from "@/components/QuizNeedHelp";
import QuizScroll from "@/components/QuizScroll";
import { Quiz, User } from "@/store";
export default {
  name: "quiz",
  components: {
    QuizScroll,
    QuizNeedHelp
  },
  computed: {
    ...User.mapState(),
    ...Quiz.mapState()
  },
  methods: {
    async onClick() {
      await this.$store.dispatch("Quiz/markAsSeen");
      this.$router.push({ name: "quiz" });
    }
  }
};
</script>
