<template>
  <v-app class="cwhq-app public">
    <CWHQ-bar />
    <!-- <app-bar /> -->
    <quiz-bar />
    <v-main>
      <router-view />
    </v-main>
    <leaderboard-bar />
    <snackbar/>
    <mobile-warning />
  </v-app>
</template>

<script>
import AppBar from '@/components/Toolbars/AppBar';
import QuizBar from '@/components/Toolbars/QuizBar';
import CWHQBar from '@/components/Toolbars/CWHQBar';
import LeaderboardBar from '@/components/Toolbars/LeaderboardBar';
import MobileWarning from '@/components/MobileWarning';
import Snackbar from '@/components/Snackbar'

export default {
  name: 'App',
  components: {
    MobileWarning,
    AppBar,
    QuizBar,
    CWHQBar,
    LeaderboardBar,
    Snackbar
  }
};
</script>
