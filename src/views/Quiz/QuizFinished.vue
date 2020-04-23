<template>
  <div class="mt-6">
    <v-row justify="center">
      <quiz-scroll>
        <template v-slot:title>Congratulations!</template>
        <template v-slot:default>
          <div style="padding-left:130px; padding-right: 130px;">
            Congratulations young pilgrim!
            <br />
            <br />
            You've qualified for the final round of The Dragon Quest.
            <br /><br />
            To win the grand prize of $100 and a free STEAM access code from
            Endless, come back when the voting period begins, April 26 at 5:00
            PM CT, to gather votes and cast your vote on who you think has the
            best solution for the final answer.
            <br /><br />
            The player with the highest number of votes will be crowned the
            champion on May 1. Will you be the champion …
            <br /><br />Good luck! <br /><br />
          </div>
        </template>
      </quiz-scroll>
    </v-row>
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
