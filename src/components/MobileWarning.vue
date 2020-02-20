<template>
  <div class="mobile-warning" v-if="show">
    <img src="/images/logo-small.png" class="mt-6 mb-6" />
    <h2 class="mb-3">Come back on your desktop!</h2>
    <p class="pa-10">
      Our Coding Challenge platform was not created for mobile phones. Please visit challenge.codewizardshq.com from your desktop for the best experience.
    </p>
    <v-btn color="button" @click="show = false">Show me anyways</v-btn>
  </div>
</template>

<script>
export default {
  data() {
    return {
      show: true
    };
  }
};
</script>
