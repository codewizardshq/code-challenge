<template>
  <v-container>
    <v-row>
      <v-col class="inside-div">
        <h2 class="ballot-header">
          Woah, voting has not started yet!
        </h2>
        <p>
          Our challengers are hard at work. Come back on May 3 to vote for the
          winner.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// TODO: this and VotingOver should be a single component with props
export default {
  name: "VotingWoah"
};
</script>

<style lang="scss" scoped>
.inside-div {
  background: gray;
}

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
