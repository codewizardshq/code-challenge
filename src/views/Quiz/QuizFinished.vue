<template>
  <div class="mt-6 wrapper">
    <!-- <v-row justify="center"> -->
    <quiz-scroll>
      <template v-slot:title>Congratulations!</template>
      <template v-slot:default>
        <div>
          <p>Congratulations young pilgrim!</p>

          <p>You've qualified for the final round of The Dragon Quest.</p>

          <p>
            To win the grand prize of $100 and a free STEAM access code from
            Endless, come back when the voting period begins, April 26 at 5:00
            PM CT, to gather votes and cast your vote on who you think has the
            best solution for the final answer.
          </p>

          <p>
            The player with the highest number of votes will be crowned the
            champion on May 1. Will you be the champion …
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
