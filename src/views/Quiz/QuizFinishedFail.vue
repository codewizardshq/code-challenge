<template>
  <div class="mt-6 wrapper">
    <!-- <v-row justify="center"> -->
    <quiz-scroll>
      <template v-slot:title>It's Over!</template>
      <template v-slot:default>
        <div>
          <p>Sorry {{ firstName }}, your mission has ended.</p>

          <p>
            Your efforts were admirable! Nym and the Allsnacks Alliance thank
            you.
          </p>

          <p>
            You can still vote for this year's winner from April May 3 to May 7
            and try again next year.
          </p>

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
import { User } from "@/store";
export default {
  name: "quiz-finished-fail",
  components: {
    QuizScroll
  },
  computed: {
    firstName() {
      return User.state.firstName;
    }
  }
};
</script>

<style lang="scss" scoped>
.wrapper {
  display: flex;
  justify-content: center;
}
</style>
