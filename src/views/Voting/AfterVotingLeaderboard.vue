<template>
  <div class="after-vote-wrapper">
    <h1>Voting Has Ended!</h1>
    <BallotLeaders :voting-enabled="false" />
  </div>
</template>

<script>
import BallotLeaders from "@/views/Voting/BallotLeaders";
export default {
  name: "AfterVotingLeaderboard",
  components: {
    BallotLeaders
  }
};
</script>

<style lang="scss" scoped>
.after-vote-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: url("/images/space-background.jpg");
}
</style>
