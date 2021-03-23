<template>
  <div class="speech-area">
    <div class="speech-graphic"></div>

    <div class="speech-head">
      <div class="speech-title">
        <slot name="title" />
      </div>
    </div>

    <div class="speech-body">
      <slot name="default" />
    </div>
  </div>
</template>

<script>
export default {
  name: "SpeechArea",
  props: {
    answerInputType: {
      type: String,
      default: "text-field"
    },
    value: [String]
  }
};
</script>

<style lang="sass" scoped>
.speech-area
  position: relative

  .speech-head
    font-size: 30px
    position: relative
    top: 42px
    width: 100%
    z-index: 2

    .speech-title
      text-align: center
      position: relative
      left: -60px
      top: -8px

  .speech-body
    z-index: 1
    position: relative
    text-align: left
    width: 560px
    left: -60px
    top: 55px
    height: 495px

  .speech-graphic
    position: absolute
    z-index: 0
    width: 1200px
    height: 666px
    left: -111px
    background-image: url("/images/main-text-area.svg")
    background-size: contain
</style>
