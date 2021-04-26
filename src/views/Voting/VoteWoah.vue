<template>
  <div class="vote-woah-container">
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
  </div>
</template>

<script>
export default {
  name: "VotingWoah"
};
</script>

<style lang="scss" scoped>
.vote-woah-container {
  height: 100%;
  width: 100%;
  background: url("/images/space-background.jpg");
}

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
