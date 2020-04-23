<template>
  <v-container>
    <v-row>
      <v-col>
        <h2 class="ballot-header">
          Woah, voting has not started yet!
        </h2>
        <p>
          Our challengers are hard at work. Come back on April 26 5 PM CT to
          vote for the winner.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "VotingWoah"
};
</script>

<style lang="scss" scoped>
h2 {
  text-align: center;
  color: #0d1d41;
  font-family: "Barlow", sans-serif;
  font-weight: bold;
  margin-bottom: 12px;
}

p {
  text-align: center;
  color: #0d1d41;
  font-family: "Barlow", sans-serif;
}
</style>
