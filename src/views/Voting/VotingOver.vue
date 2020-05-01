<template>
  <v-container>
    <v-row>
      <v-col>
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
export default {
  name: 'VotingWoah',
};
</script>

<style lang="scss" scoped>
h2 {
  text-align: center;
  color: #0d1d41;
  font-family: 'Barlow', sans-serif;
  font-weight: bold;
  margin-bottom: 12px;
}

p {
  text-align: center;
  color: #0d1d41;
  font-family: 'Barlow', sans-serif;
}
</style>
