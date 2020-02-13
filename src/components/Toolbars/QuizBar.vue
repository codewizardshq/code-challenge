<template>
  <v-toolbar
    color="dark2 quiz-bar"
    flat
    class="secondary--text"
    :height="60"
    :max-height="60"
  >
    <div
      class="quiz-bar-rank"
      v-show="User.isAuthorized && Quiz.quizHasStarted && !Quiz.quizHasEnded"
    >
      <div class="level-display">Level</div>
      <div class="rank">{{ User.rank }}</div>
    </div>
    <v-container>
      <v-row>
        <v-col>
          <span v-if="User.isAuthorized" class="barrow-bold"
            >Welcome pilgrim {{ User.displayName }}</span
          >

          <router-link
            v-else
            color="secondary"
            text
            x-large
            active-class="none"
            :to="{ name: 'register' }"
            >Start your journey</router-link
          >
        </v-col>

        <v-col class="text-right">
          <v-menu offset-y>
            <template v-slot:activator="{ on: menu }">
              <a href="#" v-on="menu">Get Help</a>
            </template>
            <v-list class="list">
              <v-list-item :to="{ name: 'faq' }">
                <v-list-item-title>Check The FAQ</v-list-item-title>
              </v-list-item>
              <v-list-item href="https://discord.gg/HKnpzjQ" target="_blank">
                <v-list-item-title>Get Help On Discord</v-list-item-title>
              </v-list-item>
              <v-list-item href="https://www.facebook.com/events/501020200554546/" target="_blank">
                <v-list-item-title>Get Help On Facebook</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <router-link v-if="!User.isAuthorized" :to="{ name: 'login' }"
            >Sign In</router-link
          >

          <router-link v-if="User.isAuthorized" :to="{ name: 'logout' }"
            >Sign Out</router-link
          >
        </v-col>
      </v-row>
    </v-container>
  </v-toolbar>
</template>

<script>
import { User, Quiz } from "@/store";

export default {
  name: "quizBar",
  computed: {
    ...User.mapState(),
    ...Quiz.mapState()
  }
};
</script>

<style lang="scss" scoped>
.list {
  padding: 20px;
}
</style>
