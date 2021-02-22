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
  name: "SpeechArea"
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

  .speech-body
    z-index: 1
    position: relative
    text-align: center
    margin-top: 100px

  .speech-graphic
    position: absolute
    z-index: 0
    width: 666px
    height: 2238px
    left: -166px
    background-image: url("/images/main-text-area.svg")
    background-size: contain
</style>
