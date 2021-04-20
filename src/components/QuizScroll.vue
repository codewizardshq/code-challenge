<template>
  <div class="quiz-scroll" ref="scroll">
    <div class="scroll-head">
      <div class="scroll-title">
        <slot name="title"></slot>
      </div>
    </div>
    <div class="divider" />
    <div class="scroll-body" ref="body">
      <slot name="default"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "quizScroll"
};
</script>

<style lang="scss" scoped>
.quiz-scroll {
  width: 550px;
  height: 650px;
  display: flex;
  margin-top: 30px;
  flex-direction: column;
  border: 8px solid #c2cfe1;
  background: url("/images/module-background.png");
  background-size: cover;

  .divider {
    height: 5px;
    width: 100%;
    background-color: #c2cfe1;
  }

  .scroll-head {
    .scroll-title {
      text-align: center;
      margin-top: 10px;
      font-size: 50px;
      top: 42px;
      color: white !important;
      font-family: "buWicked";
    }
  }

  .scroll-body {
    text-align: center;
    margin-top: 30px;
    padding: 0 40px;
    font-size: 22px;

    .asset {
      text-align: center;
      margin-bottom: 35px;
    }

    .scroll-content {
      width: 420px;
      margin-left: auto;
      margin-right: auto;
      font-size: 24px;
      color: #031e41 !important;
      font-family: "Barrow2Light";
      letter-spacing: 2px;
      text-align: left;
      white-space: pre-wrap;

      pre {
        font-size: 18px;
        white-space: pre-wrap;
      }
    }
  }
}
</style>
