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
    <v-btn v-if="votingEnabled" elevation="0" color="primary" block>Vote</v-btn>
    <v-btn v-if="!votingEnabled" elevation="0" color="deactivated" block
      >Voting Over</v-btn
    >
  </v-card>
</template>

<script>
export default {
  props: {
    display: Boolean,
    firstName: String,
    id: String,
    lastName: String,
    numVotes: Number,
    text: String,
    username: String,
    value: String,
    initials: String,
    votingEnabled: {
      type: Boolean,
      default: true
    }
  }
};
</script>
