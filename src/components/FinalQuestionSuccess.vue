<template>
  <div :class="`overlay ${dynamicClass}`" v-if="isOpen">
    <img src="/images/complete_joy.svg" />
    <div class="content">
      <v-btn @click="onClick">Continue</v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: "FinalQuestionSuccess",
  data() {
    return {
      dynamicClass: "idle",
      isOpen: true,
      isClosing: false
    };
  },
  mounted() {
    setTimeout(() => {
      if (this) {
        this.onClick();
      }
    }, 1000 * 4);
  },
  methods: {
    onClick() {
      if (this.isClosing) {
        return;
      }
      this.isClosing = true;
      this.dynamicClass = "hidden";
      setTimeout(() => {
        this.isOpen = false;
      }, 1000);
    }
  }
};
</script>

<style lang="scss" scoped>
$top: 100px;
.overlay {
  background-color: rgba(0, 0, 0, 0.3);
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 10000;

  transition: 1s;
  opacity: 1;

  &.hidden {
    opacity: 0;
  }

  img {
    display: block;
    width: 700px;
    height: auto;
    margin: auto;
    top: $top;
    position: relative;
    animation-name: victoryAnimation;
    animation-duration: 2s;
  }

  .content {
    position: relative;
    margin: auto;
    width: 600px;
    display: block;
    text-align: center;
    border-radius: 12px;
    // background-color: #fff;
    height: 200px;
    top: $top - 70px;
  }

  @keyframes victoryAnimation {
    0% {
      top: -1000px;
    }
    100% {
      top: $top;
    }
  }
}
</style>
