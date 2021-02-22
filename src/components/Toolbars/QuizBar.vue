<template>
  <v-toolbar
    color="dark2 quiz-bar"
    flat
    class="secondary--text"
    :height="100"
    :max-height="100"
  >
    <div
      class="quiz-bar-rank"
      v-show="User.isAuthorized && Quiz.quizHasStarted && !Quiz.quizHasEnded"
    >
      <div class="level-display">Level</div>
      <div class="rank">{{ User.rank }}</div>
    </div>
    <v-container fluid>
      <v-row>
        <v-col>
          <router-link :to="{ name: 'redirect' }">
            <img
              src="/images/logo-with-code-challenge.svg"
              height="80"
              alt="CodeWizardsHQ Code Challenge"
            />
          </router-link>

          <span
            v-if="User.isAuthorized"
            class="archivo"
            style="position: absolute; top: 40%; left: 15%;"
            >Welcome, {{ User.displayName }}</span
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

        <v-col class="text-right mt-7">
          <v-menu offset-y>
            <template v-slot:activator="{ on: menu }">
              <a href="#" v-on="menu">Get Help</a>
            </template>
            <v-list class="list">
              <v-list-item :to="{ name: 'faq' }">
                <v-list-item-title>Check The FAQ</v-list-item-title>
              </v-list-item>
              <!-- FIXME: uncomment this when we have a CodeChallenge discord
              <v-list-item href="https://discord.gg/NuKfKZ8" target="_blank">
                <v-list-item-title>Get Help On Discord</v-list-item-title>
              </v-list-item> -->
              <v-list-item
                href="https://www.facebook.com/events/501020200554546/"
                target="_blank"
              >
                <v-list-item-title>Get Help On Facebook</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <router-link v-if="!User.isAuthorized" :to="{ name: 'login' }"
            >Sign In</router-link
          >

          <router-link v-if="User.isAuthorized" :to="{ name: 'logout' }"
            >Logout</router-link
          >
        </v-col>
      </v-row>
    </v-container>
  </v-toolbar>
</template>

<script>
import { Quiz, User } from "@/store";

export default {
  name: "quizBar",
  computed: {
    ...User.mapState(),
    ...Quiz.mapState()
  }
};
</script>

<style lang="sass" scoped>
.list
  padding: 20px

.v-toolbar__content
  background-image: url("/images/navbar-patterned-background.png")
</style>
d
