<template>
  <div id="container">
    <video
      class="transition-media"
      :src="media"
      v-if="media.endsWith('mp4')"
      autoplay
      loop
    ></video>
    <img class="transition-media" :src="media" v-else :alt="caption" />
    <p v-html="caption" v-if="!!caption" />
  </div>
</template>

<script>
export default {
  name: "QuizTransition",
  props: {
    caption: [String],
    media: [String]
  }
};
</script>

<style lang="sass" scoped>
#container
  margin: auto
  max-width: 900px

.transition-media
  width: 100%
</style>
