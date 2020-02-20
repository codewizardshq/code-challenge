<template>
  <div class="mobile-warning" v-if="show">
    <img src="/images/logo-small.png" class="mt-6 mb-6" />
    <h2 class="mb-3">This site is not designed for mobile devices!</h2>
    <p class="pa-10">
      As much as we appreciate mobile first design, it does not always apply.
      This is a code challenge and requires full use of your brain and keyboard.
      Please visit this page on your phone or desktop to continue.
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
