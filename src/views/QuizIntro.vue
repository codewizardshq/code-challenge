<template>
  <div class="mt-6">
    <v-row justify="center">
      <quiz-scroll>
        <template v-slot:title>Welcome Pilgrim</template>
        <template v-slot:default>
          <p class="text-center">Watch the video</p>
          <p class="text-center">
            <iframe
              width="400px"
              height="300px"
              src="https://www.youtube.com/embed/Fk8zykXuR5k"
              frameborder="0"
              allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </p>
          <p class="text-center">
            <v-btn color="primary" @click="onClick" x-large>Continue</v-btn>
          </p>
        </template>
      </quiz-scroll>
    </v-row>
  </div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";

export default {
  name: "quiz",
  components: {
    QuizScroll
  },
  methods: {
    async onClick() {
      await this.$store.dispatch("Quiz/markAsSeen");
      this.$router.push({ name: "quiz" });
    }
  }
};
</script>
