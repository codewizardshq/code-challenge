<template>
  <div class="quiz-answer">
    <v-card flat>
      <!--
      <img src="/images/dragon1.png" />
      -->
      <v-card-text>
        <v-form ref="form" @submit.prevent="submit">
          <div class="text-field">
            <v-text-field
              autocomplete="off"
              v-model="fields.answer.value"
              v-bind="fields.answer"
              :disabled="isDisabled"
              @blur="onBlur"
            />
          </div>

          <v-btn
            x-large
            color="primary"
            v-if="showHint1"
            @click="showHint1Modal = true"
            >Hint #1</v-btn
          >
          <v-btn
            x-large
            color="primary"
            v-if="showHint2"
            @click="showHint2Modal = true"
            >Hint #2</v-btn
          >
          <v-btn x-large color="primary" :disabled="isDisabled" type="submit"
            >Submit</v-btn
          >
        </v-form>
      </v-card-text>
    </v-card>
    <v-dialog v-model="showSuccessModal" persistent max-width="400">
      <v-card>
        <v-card-title class="headline">Your answer was correct!</v-card-title>
        <div v-if="isLastQuiz">
          <v-card-text>
            Congratulations, {{ User.displayName }}!
            <br />
            Not only can you call yourself one of the best kid coders in the
            land, you also win a $100 CodeWizardsHQ Gift Certificate.
            <br />
            <br />
            Check your email tomorrow for your prize. You've qualified for the
            final boss level round of The Dragon Quest tomorrow at 8:00 AM CT
            April 24 and the chance to win $100 cash and free STEAM access code
            from Endless.
            <br />
            <br />
            Are you prepared?
            <br />
            <br />
            <span v-if="Quiz.awaitNextQuestion">
              That's all the questions available for now. The next question
              unlocks {{ Quiz.nextUnlockMoment.fromNow() }}
            </span>
            <v-card-actions>
              <v-btn block color="primary darken-1" @click="next">OKAY</v-btn>
            </v-card-actions>
          </v-card-text>
        </div>
        <div v-else-if="Quiz.awaitNextQuestion">
          <v-card-text>
            Congratulations, {{ User.displayName }}!
            <br />
            You've conquered Level {{ rank }}. {{ successMessage }}
            <br />
            <br />
            That's all the questions available for now. The next question
            unlocks {{ Quiz.nextUnlockMoment.fromNow() }}
          </v-card-text>
          <v-card-actions>
            <v-btn block color="primary darken-1" @click="next">OKAY</v-btn>
          </v-card-actions>
        </div>
        <div v-else>
          <v-card-text>
            Congratulations, {{ User.displayName }}!
            <br />
            You've conquered Level {{ rank }}. {{ successMessage }}
            <br />
            <br />
          </v-card-text>
          <v-card-actions>
            <v-btn block color="primary darken-1" @click="next"
              >NEXT QUESTION</v-btn
            >
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showRateLimitModal" persistent max-width="400">
      <v-card>
        <v-card-title class="headline">Woah slow down!</v-card-title>
        <v-card-text>
          We noticed you are submitting a lot of requests. Please wait 60
          seconds before submitting another answer.
        </v-card-text>
        <v-card-actions>
          <v-btn
            block
            color="primary darken-1"
            @click="showRateLimitModal = false"
            >OKAY</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showHint1Modal" persistent max-width="400">
      <v-card>
        <v-card-title class="headline">HINT #1</v-card-title>
        <v-card-text>{{ Quiz.hints[0] }}</v-card-text>
        <v-card-actions>
          <v-btn block color="primary darken-1" @click="showHint1Modal = false"
            >OKAY</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showHint2Modal" persistent max-width="400">
      <v-card>
        <v-card-title class="headline">HINT #2</v-card-title>
        <v-card-text>{{ Quiz.hints[1] }}</v-card-text>
        <v-card-actions>
          <v-btn block color="primary darken-1" @click="showHint2Modal = false"
            >OKAY</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <final-question-success v-if="showSuccessModal && isLastQuiz" />
  </div>
</template>

<script>
import * as api from "@/api";
import { User, Quiz } from "@/store";
import FinalQuestionSuccess from "@/components/FinalQuestionSuccess";

export default {
  name: "quizAnswer",
  components: {
    FinalQuestionSuccess
  },
  props: ["rank"],
  computed: {
    ...Quiz.mapState(),
    ...User.mapState(),
    isDisabled() {
      return this.isSubmitting || this.wasCorrect;
    },
    successMessage() {
      return this.successMessages[
        Math.floor(Math.random() * this.successMessages.length)
      ];
    },
    showHint1() {
      return this.Quiz.wrongCount > 0;
    },
    showHint2() {
      return this.Quiz.wrongCount > 1;
    }
  },
  data() {
    return {
      successMessages: [
        "Your coding skills are quite admirable.",
        "You are wiser than you look.",
        "The dragon senses you getting closer.",
        "Your perseverance is impressive.",
        "One step closer to battling the dragon.",
        "Keep going, the dragon awaits you.",
        "Go to the next level, young Pilgrim!",
        "You may continue on your coding journey.",
        "The grand prize could be yours.",
        "You must be the hero we're seeking."
      ],
      entryRank: -1,
      isLastQuiz: false,
      isSubmitting: false,
      wasCorrect: false,
      attemptsRemaining: 3,
      totalAttempts: 3,
      showSuccessModal: false,
      showRateLimitModal: false,
      showHint1Modal: false,
      showHint2Modal: false,
      fields: {
        answer: {
          label: "Your Answer",
          value: "",
          rules: [v => !!v || "You forgot to include an answer!"],
          errorMessages: [],
          successMessages: [],
          success: false
        }
      }
    };
  },
  mounted() {
    if (this.Quiz.rank === this.Quiz.maxRank - 1) {
      // eslint-disable-next-line no-console
      console.log("Is last quiz!!");
      this.isLastQuiz = true;
    }
  },
  methods: {
    onBlur() {
      this.fields.answer.errorMessages = [];
      if (!this.fields.answer.value) {
        this.$refs.form.resetValidation();
      }
    },
    async next() {
      try {
        this.showSuccessModal = false;
        this.fields.answer.value = "";
        this.fields.answer.successMessages = [];
        this.fields.answer.success = false;
        this.$refs.form.resetValidation();
        this.$emit("next");
      } catch (err) {
        await this.$store.dispatch("Snackbar/showError", err);
      }
    },
    async submit() {
      if (!this.$refs.form.validate()) {
        return;
      }

      if (this.isSubmitting) {
        return false;
      }
      this.isSubmitting = true;
      try {
        const isCorrect = await api.quiz.submit(this.fields.answer.value);

        if (isCorrect) {
          await this.$store.dispatch("Quiz/clearWrongCount");
          await api.auth.fetchState();
          await this.$store.dispatch("Quiz/refresh");
          this.showSuccessModal = true;
          this.fields.answer.successMessages = ["Your answer was correct!"];
          this.fields.answer.success = true;
        } else {
          this.$store.dispatch("Quiz/addWrongCount");
          this.$store.dispatch(
            "Snackbar/showError",
            "That answer was not correct"
          );
          this.fields.answer.errorMessages = ["Your answer was not correct"];
        }
      } catch (err) {
        if (err.status === 429) {
          this.showRateLimitModal = true;
        } else {
          this.$store.dispatch("Snackbar/showError", err);
        }
      }
      this.isSubmitting = false;
    }
  }
};
</script>
