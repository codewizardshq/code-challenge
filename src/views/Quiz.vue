<template>
  <div class="mt-6" v-if="!isLoading">
    <v-row justify="center">
      <quiz-scroll>
        <template v-slot:title>{{ title }}</template>
        <template v-slot:default>
          <img class="asset" :src="asset" v-if="!!asset" />
          <div class="scroll-content" v-html="question" />
        </template>
      </quiz-scroll>
      <quiz-answer @next="onNext" :isLoading="isLoading" v-if="!maxQuiz" />
    </v-row>
    <quiz-need-help />
  </div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import QuizAnswer from "@/components/QuizAnswer";
import QuizNeedHelp from "@/components/QuizNeedHelp";
import * as api from "@/api";
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
      maxQuiz: false,
      showIntro: true
    };
  },
  async mounted() {
    // document.getElementsByTagName("html")[0].style.overflowY = "hidden";
    // window.scrollTo(0, 0);
    await this.loadQuestion();
  },
  methods: {
    async onNext() {
      this.$store.dispatch("Quiz/setScores");
      this.$router.push({ name: "quiz-scores" });
    },
    async loadQuestion() {
      this.isLoading = true;
      this.actualQuestion = "";
      this.actualAsset = "";
      try {
        const data = await api.quiz.getQuestion();
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
    }
  },
  // beforeDestroy() {
  // 	// document.getElementsByTagName("html")[0].style.overflowY = "scroll";
  // },
  computed: {
    ...User.mapState(),
    title() {
      return this.maxQuiz ? "Challenge Complete!" : "Level " + this.User.rank;
    },
    question() {
      if (this.isLoading) {
        return "Loading...";
      }
      if (this.maxQuiz) {
        return "<center>Thanks for beta testing!</center>";
      }
      return this.actualQuestion;
    },
    asset() {
      return !this.isLoading ? this.actualAsset : "";
    }
  }
};
</script>
