<template>
  <v-container>
    <v-row>
      <v-col class="inside-div">
        <h2 class="ballot-header">
          Voting is over!
        </h2>
        <p>
          Please check back soon for the results.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// TODO: this and VoteWoah should be a single component with props
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
