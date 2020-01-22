<template>
  <div class="quiz-scroll">
    <div class="scroll-head">
      <div class="scroll-title">
        <slot name="title"></slot>
      </div>
    </div>
    <div class="scroll-body" ref="body" :style="bodyStyles">
      <slot name="default"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "quizScroll",
  data() {
    return {
      minHeight: 800,
      offset: 200,
      interval: null
    };
  },
  computed: {
    bodyStyles() {
      return {
        top: -this.offset + "px",
        paddingTop: this.offset - 80 + "px"
      };
    }
  },
  methods: {
    fixHeightHack() {
      let height = 450;
      for (let child of this.$refs.body.children) {
        height += child.clientHeight;
      }
      this.offset = this.$refs.body.clientHeight - height;
    }
  },
  beforeDestroy() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  },
  mounted() {
    this.fixHeightHack();
    this.interval = setInterval(() => {
      this.fixHeightHack();
    }, 100);

    // console.log(this.offset);
    // this.offset = Math.min(this.$refs.body.clientHeight - this.minHeight, this.offset);
    // console.log(this.offset);
  }
};
</script>
