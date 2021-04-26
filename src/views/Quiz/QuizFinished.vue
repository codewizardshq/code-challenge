<template>
  <div class="mt-6 wrapper">
    <!-- <v-row justify="center"> -->
    <quiz-scroll>
      <template v-slot:title>Congratulations!</template>
      <template v-slot:default>
        <div>
          <p>Congratulations!</p>

          <p>
            You’ve completed the boss level of the Deep Space Crystal Chase.
          </p>

          <p>
            With your help, Nym defeats Glorm in an epic battle and retrieves
            the Xocron crystal. The Grand Poomba Fizzy finally restores peace to
            the galaxy.
          </p>

          <p>
            To win the grand prize of $100, share your entry with friends and
            family to vote. Voting is open from May 3-7. The top 3 players with
            the highest vote will be eligible for Wizard Panel review and to be
            crowned champion.
          </p>

          <p>Good luck!</p>

          <v-btn :to="{ name: 'voting' }" color="white" light
            >Cast Your Votes Here</v-btn
          ><br />
          <v-btn
            class="mr-3 mt-5"
            :style="{ backgroundColor: 'white !important' }"
            x-large
            color="blue"
            href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&amp;amp;src=sdkpreparse"
            target="_blank"
            icon
            ><v-icon>mdi-facebook</v-icon></v-btn
          >
          <v-btn
            class="mt-5"
            :style="{ backgroundColor: 'white !important' }"
            x-large
            color="blue"
            href="https://twitter.com/intent/tweet?text=CodeWizardsHQ%20Code%20Challenge&amp;url=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&amp;original_referer="
            target="_blank"
            icon
            ><v-icon>mdi-twitter</v-icon></v-btn
          >
        </div>
      </template>
    </quiz-scroll>
    <!-- </v-row> -->
  </div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
export default {
  name: "quiz",
  components: {
    QuizScroll
  },
  mounted() {}
};
</script>

<style lang="scss" scoped>
.wrapper {
  display: flex;
  justify-content: center;
}
</style>
