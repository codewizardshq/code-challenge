<template>
  <v-dialog v-model="show" max-width="600">
    <v-card color="white" light>
      <v-card-title>
        <v-spacer />
        <v-btn icon x-large @click="show = false">X</v-btn></v-card-title
      >

      <h3>ALMOST DONE</h3>

      <p>
        Your vote has been cast! In order for your vote to count you must first
        confirm your it. Please check your inbox for the confirmation email.
      </p>
      <hr />
      <h4>
        Share this code with your friends!
      </h4>

      <v-card-text class="text-center">
        <v-btn icon class="mr-6" x-large color="cwhqBlue"
          ><v-icon>mdi-facebook</v-icon></v-btn
        >
        <v-btn icon class="mr-6" x-large color="cwhqBlue"
          ><v-icon>mdi-twitter</v-icon></v-btn
        >
        <v-btn icon class="mr-6" x-large color="cwhqBlue"
          ><v-icon>mdi-email</v-icon></v-btn
        >
      </v-card-text>
      <br />
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["value"],
  data() {
    return {
      show: this.value
    };
  }
};
</script>

<style scoped lang="scss">
.v-card__title .v-btn {
  z-index: 3;
  position: relative;
  top: -12px;
  right: -22px;
  font-size: 30px !important;
}

.v-btn i.v-icon {
  font-size: 60px !important;
}
h3 {
  text-align: center;
  padding-top: 30px;
  font-size: 40px;
  color: #0d1d41;
  position: relative;
  top: -90px;
  margin-bottom: -60px;
}

hr {
  margin-left: 80px;
  margin-right: 80px;
  height: 1px;
  margin-top: 40px;
  margin-bottom: 20px;
}

p {
  font-size: 20px;
  padding-left: 80px;
  padding-right: 80px;
}

h4 {
  text-align: center;
  padding-top: 30px;
  font-size: 30px;
  line-height: 40px;
  color: #0d1d41;
  margin-bottom: 30px;
}
</style>
