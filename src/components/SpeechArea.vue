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

    <div class="answer-input">
      <input
        type="text"
        id="input-text-field"
        v-if="answerInputType === 'text-field'"
      />
      <textarea v-else></textarea>
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
    }
  }
};
</script>

<style lang="sass" scoped>
#input-text-field
  position: relative
  z-index: 2
  color: white
  width: 100%
  height: 100%

.speech-area
  position: relative

  .answer-input
    z-index: 1
    position: absolute
    width: 334px
    height: 75px
    right: -135px
    top: 290px


  .speech-head
    font-size: 30px
    position: relative
    top: 42px
    width: 100%
    z-index: 2

    .speech-title
      text-align: center
      position: relative
      left: -287px
      top: -8px

  .speech-body
    z-index: 1
    position: relative
    text-align: left
    width: 560px
    left: -287px
    top: 55px
    height: 495px

  .speech-graphic
    position: absolute
    z-index: 0
    width: 1200px
    height: 666px
    left: -333px
    background-image: url("/images/main-text-and-input-areas.svg")
    background-size: contain
</style>
