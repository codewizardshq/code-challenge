<template>
  <div class="mt-6">
    <v-row justify="center" v-if="!isLoading">
      <quiz-scroll
        :title="title"
        :question="question"
        :asset="asset"
        :isLoading="isLoading"
      />
      <quiz-answer :isLoading="isLoading" v-if="!maxQuiz" />
    </v-row>
    <quiz-need-help />
  </div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import QuizAnswer from "@/components/QuizAnswer";
import QuizNeedHelp from "@/components/QuizNeedHelp";
import { quiz } from "@/api";
import { User } from "@/store";

export default {
  name: "quiz",
  components: {
    QuizScroll,
    QuizAnswer,
    QuizNeedHelp
  },
  data() {
    return {
      isLoading: false,
      actualQuestion: "",
      actualAsset: "",
      maxQuiz: false
    };
  },
  async mounted() {
    document.getElementsByTagName("html")[0].style.overflowY = "hidden";
    window.scrollTo(0, 0);
    this.isLoading = true;
    try {
      const data = await quiz.getQuestion();
      this.actualQuestion = data.question;
      this.actualAsset = data.asset;
    } catch (err) {
      if (!!err && !!err.status && err.status == 404) {
        this.maxQuiz = true;
      } else {
        this.$store.dispatch("Snackbar/showError", err);
      }
    }
    this.isLoading = false;
  },
  beforeDestroy() {
    document.getElementsByTagName("html")[0].style.overflowY = "scroll";
  },
  computed: {
    ...User.mapState(),
    title() {
      return this.maxQuiz ? "No more for today" : "Level " + this.User.rank;
    },
    question() {
      if (this.isLoading) {
        return "Loading...";
      }
      if (this.maxQuiz) {
        return "<center>That's all the questions for today check back tomorrow!</center>";
      }
      return this.actualQuestion;
    },
    asset() {
      return !this.isLoading ? this.actualAsset : "";
    }
  }
};
</script>
