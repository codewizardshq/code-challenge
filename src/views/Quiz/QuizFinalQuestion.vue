<template>
  <div class="mt-6" v-if="!isLoading">
    <v-container>
      <v-row justify="center">
        <v-col>
          <page-card>
            <template #title>
              <v-toolbar-title>Final Question</v-toolbar-title>
            </template>
            <br />
            <v-card-text v-html="question"></v-card-text>
            <v-card-title>Code your answer!</v-card-title>

            <v-form ref="form" @submit.prevent="submit">
              <v-card-text v-if="!!errorMessage">
                <v-alert prominent type="error" color="red darken-4">
                  <v-row align="center">
                    <v-col class="grow">{{ errorMessage }}</v-col>
                    <v-col class="shrink">
                      <v-btn color="white" light @click="errorMessage = false"
                        >Dismiss</v-btn
                      >
                    </v-col>
                  </v-row>
                </v-alert>
              </v-card-text>
              <v-card-text v-if="hasRightAnswer">
                <v-alert prominent type="success" color="secondary darken-2">
                  <v-row align="center">
                    <v-col class="grow">
                      You got the right answer! Go ahead and review your code.
                      When you're ready to submit go ahead and click "Submit
                      Answer"
                    </v-col>
                  </v-row>
                </v-alert>
              </v-card-text>
              <v-card-text>
                <v-select
                  v-bind="fields.language"
                  v-model="fields.language.value"
                />
                <code-editor
                  v-bind="fields.code"
                  v-model="fields.code.value"
                  :language="fields.language.value"
                />
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn
                  :disabled="isSubmitting"
                  large
                  color="secondary darken-2"
                  @click="checkAnswer"
                  >Check Answer</v-btn
                >
                <v-btn
                  type="submit"
                  v-if="hasRightAnswer"
                  :disabled="isSubmitting || !hasRightAnswer"
                  large
                  color="secondary darken-2"
                  >Submit Answer</v-btn
                >
              </v-card-actions>
            </v-form>
          </page-card>
        </v-col>
      </v-row>
      <br />
      <br />
    </v-container>
    <!-- <quiz-need-help /> -->
  </div>
</template>

<script>
import CodeEditor from "./CodeEditor";
import PageCard from "@/components/PageCard";
import * as api from "@/api";
import { User, Quiz } from "@/store";

export default {
  name: "quiz",
  components: {
    CodeEditor,
    PageCard
  },
  data() {
    const jsCode = `function calculateAnswer(){
  // this is where you write your code
  // good luck!
}
// we check your answer by looking at the output var
var output = calculateAnswer();`;
    const pyCode = `def calculateAnswer():
  # this is where you write your code
  # good luck!
  
# we check your answer by what you print
print(calculateAnswer())`;
    return {
      isLoading: false,
      isSubmitting: false,
      hasRightAnswer: false,
      question: "",
      rank: "",
      asset: "",
      errorMessage: false,
      pyCode,
      jsCode,
      fields: {
        code: {
          label: "Enter your code",
          value: jsCode
        },
        language: {
          label: "Choose your language",
          value: "javascript",
          items: ["javascript", "python"]
        }
      }
    };
  },
  watch: {
    ["fields.language.value"](val) {
      if (val === "javascript") {
        this.fields.code.value = this.jsCode;
      } else {
        this.fields.code.value = this.pyCode;
      }
    },
    ["fields.code.value"](val) {
      if (this.fields.language.value === "javascript") {
        this.jsCode = val;
      } else {
        this.pyCode = val;
      }
    }
  },
  async mounted() {
    this.question = this.Quiz.question;
    this.rank = this.Quiz.rank;
    this.asset = this.Quiz.asset;
  },
  methods: {
    async makeRequest(checkOnly) {
      const response = await api.quiz.submitFinal(
        this.fields.code.value,
        this.fields.language.value === "javascript" ? "js" : "python",
        checkOnly
      );
      const isCorrect = response.correct;

      if (isCorrect) {
        return true;
      } else {
        if (response.js_error) {
          return Promise.reject(response.js_error);
        } else {
          return Promise.reject(
            "Hmmm.... Your code doesn't seem to generate the correct answer. Try again."
          );
        }
      }
    },
    async checkAnswer() {
      if (this.isSubmitting) {
        return false;
      }
      this.hasRightAnswer = false;
      this.errorMessage = false;
      this.isSubmitting = true;

      try {
        const response = await this.makeRequest(true);
        if (response !== true) {
          return Promise.reject(response);
        } else {
          this.hasRightAnswer = true;
        }
      } catch (err) {
        this.errorMessage = err;
      }
      this.isSubmitting = false;
    },
    async submit() {
      if (this.isSubmitting) {
        return false;
      }
      this.hasRightAnswer = false;
      this.errorMessage = false;
      this.isSubmitting = true;

      try {
        const response = await this.makeRequest(false);
        if (response !== true) {
          return Promise.reject(response);
        } else {
          this.$router.go();
        }
      } catch (err) {
        this.errorMessage = err;
      }
      this.isSubmitting = false;
    }
  },
  computed: {
    ...User.mapState(),
    ...Quiz.mapState()
  }
};
</script>
