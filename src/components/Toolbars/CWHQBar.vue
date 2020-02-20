<template>
  <v-toolbar class="cwhq-bar" :height="height" :max-height="height">
    <v-container>
      <a href="https://github.com/codewizardshq/code-challenge"
        >See the source on Github</a
      >
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
