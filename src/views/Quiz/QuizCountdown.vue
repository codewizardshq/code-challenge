<template>
  <div class="mt-6">
    <v-row justify="center" align="center">
      <!--
      <speech-area v-if="Quiz.awaitNextQuestion">
        <template v-slot:title>Next Challenge</template>
        <template v-slot:default>
          <div v-if="Quiz.awaitNextQuestion">
            Congratulations, {{ User.displayName }}!
            <br />
            You've conquered Level {{ User.rank - 1 }}.
            <br />
            <br />That's all the questions available for now.
            <br />
            The next question unlocks at 8AM Central Time tomorrow.
            The next question unlocks {{ Quiz.nextUnlockMoment.fromNow() }}
          </div>
          <div v-else>
            Congratulations, {{ User.displayName }}!
            <br />
            You've conquered Level {{ User.rank - 1 }}.
            <br />
            <br />
          </div>
        </template>
      </speech-area>

      <speech-area v-else-if="!Quiz.quizHasStarted">
        <template v-slot:title>Woah Slow Down!</template>
        <template v-slot:default>
          <p class="text-center">The challenge has not yet begun!</p>
          <p>Challenge begins {{ Quiz.quizStartedMoment.fromNow() }}</p>
          <p>Challenge starts April 5th</p>
          <v-btn
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
          >
        </template>
      </speech-area>

      <img width="400px" src="/images/coming-soon.png" />-->
      <h2>The next question unlocks at 8AM Central Time tomorrow!</h2>
      <br />
    </v-row>
    <v-row justify="center" align="center">
      <h3>
        Share your success with friends and tag us to be featured.
        #CWHQChallenge #NymSavesTheGalaxy
      </h3>
    </v-row>
    <v-row justify="center" align="center">
      <v-card class="social-pop-over">
        <v-card-text>
          <v-row no-gutters class="pt-3">
            <social-media-link
              anchor-href="https://twitter.com/intent/tweet?text=CodeWizardsHQ%20Code%20Challenge&amp;url=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&amp;original_referer="
              icon-name="mdi-twitter"
            />
            <social-media-link
              anchor-href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&amp;amp;src=sdkpreparse"
              icon-name="mdi-facebook"
            />
            <social-media-link
              anchor-href="https://www.linkedin.com/company/codewizardshq"
              icon-name="mdi-linkedin"
            />
            <social-media-link
              anchor-href="mailto:?subject=Join%20me%20in%20the%20CodeWizardsHQ%20Code%20Challenge!"
              icon-name="mdi-email"
            />
          </v-row>
          <a class="mt-6" href="https://github.com/codewizardshq/code-challenge"
            >Check out the source code on GitHub!</a
          >
        </v-card-text>
      </v-card>
    </v-row>
    <!-- <quiz-need-help /> -->
  </div>
</template>

<script>
// import QuizNeedHelp from "@/components/QuizNeedHelp";
import SocialMediaLink from "@/components/SocialMediaLink";
import { Quiz, User } from "@/store";

export default {
  name: "quiz",
  components: {
    // QuizNeedHelp,
    SocialMediaLink
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
