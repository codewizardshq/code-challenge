<template>
  <v-card
    class="ballot ballot-card"
    light
    elevation="0"
    @click="$emit('click')"
  >
    <div class="circle">
      {{ initials }}
    </div>
    <div class="username">
      {{ username }}
    </div>
    <div class="vote-count">
      {{ numVotes }} {{ numVotes.length == 1 ? "vote" : "votes" }}
    </div>

    <v-btn elevation="0" color="cwhqBlue" block>See Code</v-btn>
    <v-btn v-if="!isVotingDisabled" elevation="0" color="primary" block
      >Vote</v-btn
    >
  </v-card>
</template>

<script>
export default {
  props: [
    "display",
    "firstName",
    "id",
    "lastName",
    "numVotes",
    "text",
    "username",
    "value",
    "initials",
    "isVotingDisabled" // boolean, required
  ]
};
</script>
