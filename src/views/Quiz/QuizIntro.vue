<template>
  <div class="mt-6">
    <v-row justify="center">
      <div class="container">
        <speech-area>
          <template v-slot:title>Welcome</template>
          <template v-slot:default>
            <p class="text-center">Watch the video</p>
            <p class="text-center">
              <iframe
                width="500px"
                height="360px"
                src="https://www.youtube.com/embed/G1LcHvSJL8M"
                frameborder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
            </p>
            <p class="text-center">
              <v-btn color="secondary darken-2" @click="onClick" x-large
                >OK!
              </v-btn>
            </p>
          </template>
        </speech-area>
      </div>
    </v-row>
  </div>
</template>

<script>
import SpeechArea from "@/components/SpeechArea";

export default {
  name: "quiz",
  components: {
    SpeechArea
  },
  methods: {
    async onClick() {
      await this.$store.dispatch("Quiz/markAsSeen");
      await this.$router.push({ name: "quiz" });
    }
  }
};
</script>
