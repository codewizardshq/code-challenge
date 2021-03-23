<template>
  <div>
    <video :src="media" v-if="media.endsWith('mp4')" loop autoplay></video>
    <img :src="media" v-else :alt="caption" />
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
