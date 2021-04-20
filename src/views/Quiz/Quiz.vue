<template>
  <v-container fluid class="container">
    <!-- <v-row justify="center" class="container-row"> -->
    <speech-area>
      <template v-slot:title style="font-size:25px;"
        >Nym's Crystal Chase</template
      >
      <template v-slot:default>
        <!--
          <img class="asset" :src="'/' + asset" v-if="!!asset" />
          -->
        <div v-html="question" />
      </template>
    </speech-area>

    <quiz-answer :rank="rank" @next="onNext" />
    <!-- </v-row> -->
    <quiz-need-help />
  </v-container>
</template>

<script>
import QuizNeedHelp from "@/components/QuizNeedHelp";
import QuizAnswer from "@/views/Quiz/QuizAnswer";
import { User, Quiz } from "@/store";
import SpeechArea from "@/components/SpeechArea";

export default {
  name: "quiz",
  components: {
    SpeechArea,
    QuizAnswer,
    QuizNeedHelp
  },
  data() {
    return {
      question: "",
      rank: "",
      asset: ""
    };
  },
  async created() {
    this.question = this.Quiz.question;
    this.rank = this.Quiz.rank;
    // this.asset = this.Quiz.asset;
  },
  methods: {
    async onNext(n) {
      this.$router.go(n);
    }
  },
  computed: {
    ...User.mapState(),
    ...Quiz.mapState()
  }
};
</script>

<style lang="scss" scoped>
.container {
  overflow: auto;
  display: flex;
  justify-content: center;

  @media screen and (max-width: 1500px) {
    flex-direction: column;
    align-items: center;
  }
}
</style>
