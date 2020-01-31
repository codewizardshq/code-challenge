<template>
  <v-container>
    <v-card color="white" light v-if="!showSuccess">
      <v-card-title>
        Confirming your vote <v-progress-circular class="ml-3" indeterminate />
      </v-card-title>
      <v-card-text>
        Please do not refresh the page or upset the web browser in any way.
      </v-card-text>
    </v-card>

    <v-dialog v-model="showSuccess" max-width="600">
      <v-card color="white" light v-if="showSuccess">
        <v-card-title>
          Your vote has been cast!
        </v-card-title>
        <v-card-text>
          Thanks for voting
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="cwhqBlue"
            tile
            @click="$router.push({ name: 'redirect' })"
            >Okay</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import * as api from "@/api";

export default {
  data() {
    return {
      showSuccess: false
    };
  },
  async mounted() {
    const token = this.$route.query.token;
    if (token === undefined) {
      alert("No token provided");
      this.$router.push({ name: "redirect" });
    }
    this.showSuccess = true;
    await api.voting.confirm(token);
    this.success = true;
  }
};
</script>
