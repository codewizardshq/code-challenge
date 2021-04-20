<template>
  <div class="speech-area">
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
  margin-top: 50px
  z-index: 5
  width: 670px
  height: 666px
  background-size: contain
  background-image: url("/images/main-text-area.svg")

  .speech-head
    font-size: 30px
    position: relative
    top: 42px
    width: 100%
    z-index: 2

    .speech-title
      text-align: center
      position: relative
      top: -8px
      font-family: "Seymour One", sans-serif
      text-transform: uppercase

  .speech-body
    z-index: 1
    position: relative
    text-align: left
    margin-left: 48px
    width: 560px
    top: 55px
    height: 495px
</style>
