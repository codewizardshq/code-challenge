<template>
  <v-app class="cwhq-app public">
    <CWHQ-bar />
    <app-bar />
    <quiz-bar />
    <v-content>
      <router-view />
    </v-content>
    <leaderboard-bar />
  </v-app>
</template>

<script>
import AppBar from "@/components/Toolbars/AppBar";
import QuizBar from "@/components/Toolbars/QuizBar";
import CWHQBar from "@/components/Toolbars/CWHQBar";
import LeaderboardBar from "@/components/Toolbars/LeaderboardBar";

export default {
  name: "App",
  components: {
    AppBar,
    QuizBar,
    CWHQBar,
    LeaderboardBar
  }
};
</script>
