<template>
  <v-toolbar class="cwhq-bar" :height="height" :max-height="height">
    <v-container>
      <a href="https://codewizardshq.com/challenge">Back to CodeWizardsHQ</a>
    </v-container>
  </v-toolbar>
</template>

<script>
export default {
  data() {
    return {
      height: 23
    };
  }
};
</script>

<style lang="scss" scoped>
.cwhq-bar .v-toolbar__content {
  background-color: #fdc743;
  // display: none !important;
  text-align: right;
  padding: 3px;
  line-height: 17.4px;

  a {
    color: #fff;
    text-decoration: none;
    margin-left: 4px;
    margin-right: 4px;
    font-family: "Barlow", sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: rgb(1, 30, 65);

    &:hover {
      text-decoration: underline;
    }

    &:not(:last-child):after {
      content: "|";
      position: relative;
      left: 4px;
    }
  }
}
</style>
