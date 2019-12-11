<template>
  <div class="mt-6">
    <v-row justify="center">
      <quiz-scroll />
      <quiz-answer />
    </v-row>
    <quiz-need-help />
  </div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import QuizAnswer from "@/components/QuizAnswer";
import QuizNeedHelp from "@/components/QuizNeedHelp";

export default {
  name: "quiz",
  components: {
    QuizScroll,
    QuizAnswer,
    QuizNeedHelp
  },
  mounted() {
    document.getElementsByTagName("html")[0].style.overflowY = "hidden";
    window.scrollTo(0, 0);
  },
  beforeDestroy() {
    document.getElementsByTagName("html")[0].style.overflowY = "scroll";
  }
};
</script>
