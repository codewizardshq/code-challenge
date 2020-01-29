<template>
  <v-app>
    <CWHQ-bar />
    <app-bar />
    <quiz-bar />
    <v-content>
      <!-- <v-container> -->
      <router-view />
      <!-- </v-container> -->
    </v-content>
    <leaderboard-bar />
    <snackbar />
  </v-app>
</template>

<script>
import AppBar from "@/components/AppBar";
import QuizBar from "@/components/QuizBar";
import Snackbar from "@/components/Snackbar";
import CWHQBar from "@/components/CWHQBar";
import LeaderboardBar from "@/components/LeaderboardBar";

export default {
  name: "App",
  components: {
    AppBar,
    QuizBar,
    Snackbar,
    CWHQBar,
    LeaderboardBar
  }
};
</script>
