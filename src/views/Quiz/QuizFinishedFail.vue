<template>
  <div class="mt-6">
    <v-row justify="center">
      <quiz-scroll>
        <template v-slot:title>It's Over!</template>
        <template v-slot:default>
          <div style="padding-left:130px; padding-right: 130px;">
            Sorry {{ firstName }}, your mission has ended.
            <br />
            <br />
            Your efforts were admirable! Nym and the Allsnacks Alliance thank
            you.
            <br />
            <br />
            You can still vote for this year's winner from April 26-30 and try
            again next year.
            <br /><br />
            <v-btn :to="{ name: 'voting' }" color="white" light
              >Cast Your Votes Here</v-btn
            ><br />
            <!-- <v-btn
              class="mr-3 mt-5"
              :style="{ backgroundColor: 'white !important' }"
              x-large
              color="blue"
              href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&amp;src=sdkpreparse"
              icon
              ><v-icon>mdi-facebook</v-icon></v-btn
            >
            <v-btn
              class="mt-5"
              :style="{ backgroundColor: 'white !important' }"
              x-large
              color="blue"
              href="https://twitter.com/intent/tweet?text=The%20Dragon%20Quest%20%E2%80%93%20Code%20Challenge&url=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&original_referer="
              icon
              ><v-icon>mdi-twitter</v-icon></v-btn
            > -->
          </div>
        </template>
      </quiz-scroll>
    </v-row>
  </div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import { User } from "@/store";
export default {
  name: "quiz-finished-fail",
  components: {
    QuizScroll,
  },
  computed: {
    firstName() {
      return User.firstName;
    },
  },
  mounted() {},
};
</script>
