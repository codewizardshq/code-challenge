<template>
  <v-container>
    <QuizScroll class="scroll">
      <template v-slot:title>
        Voting Level Complete
      </template>
      <template v-slot:default>
        <p>
          Congratulations to the top 10 students with the most votes! Thank you
          everyone for participating. Finalists will receive a notification and
          your code will be reviewed by the Galactic Wizard Panel on May 10-13.
          Our grand prize winner will be announced May 14.
        </p>
        <Leaderboard />
      </template>
    </QuizScroll>
  </v-container>
</template>

<script>
// TODO: this and VoteWoah should be a single component with props
import Leaderboard from "@/components/Leaderboard";
import QuizScroll from "@/components/QuizScroll";
export default {
  name: "VotingOver",
  components: { Leaderboard, QuizScroll }
};
</script>

<style lang="scss" scoped>
.scroll {
  margin: 0 auto;
}
</style>
