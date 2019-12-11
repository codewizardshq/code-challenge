<template>
  <div class="quiz-answer">
    <v-card flat>
      <img src="/images/dragon1-dab.png" v-if="wasCorrect" />
      <img src="/images/dragon1.png" v-else />
      <v-card-text>
        <v-form ref="form" @submit.prevent="submit">
          <v-text-field
            autocomplete="off"
            v-model="fields.answer.value"
            v-bind="fields.answer"
            :disabled="isDisabled"
            @blur="onBlur"
          />

          <v-btn x-large color="primary" :disabled="isDisabled" type="submit">
            Submit
          </v-btn>

          <v-btn
            v-if="wasCorrect"
            x-large
            color="primary"
            type="submit"
            @click="next"
          >
            NEXT
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { Quiz } from "@/api";
import { Progress } from "@/store";

export default {
  name: "quizAnswer",
  computed: {
    ...Progress.mapState(),
    isDisabled() {
      return this.isSubmitting || !this.Progress.hasData || this.wasCorrect;
    }
  },
  data() {
    return {
      isSubmitting: false,
      wasCorrect: false,
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
  methods: {
    onBlur() {
      this.fields.answer.errorMessages = [];
      if (!this.fields.answer.value) {
        this.$refs.form.resetValidation();
      }
    },
    async next() {
      try {
        this.wasCorrect = false;
        this.fields.answer.value = "";
        this.fields.answer.successMessages = [];
        this.fields.answer.success = false;
        this.$refs.form.resetValidation();
        await this.$store.dispatch("Progress/fetch");
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
        const isCorrect = await Quiz.submit(this.fields.answer.value);
        if (isCorrect) {
          this.$store.dispatch(
            "Snackbar/showSuccess",
            "That answer was correct!"
          );
          this.wasCorrect = true;
          this.fields.answer.successMessages = ["Your answer was correct!"];
          this.fields.answer.success = true;
        } else {
          this.$store.dispatch(
            "Snackbar/showError",
            "That answer was not correct"
          );
          this.fields.answer.errorMessages = ["That answer was not correct"];
        }
      } catch (err) {
        this.$store.dispatch("Snackbar/showError", err);
      }
      this.isSubmitting = false;
    }
  }
};
</script>
