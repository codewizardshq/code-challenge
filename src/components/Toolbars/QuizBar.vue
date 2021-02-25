<template>
  <v-toolbar
    :height="100"
    :max-height="100"
    class="secondary--text"
    color="dark2 quiz-bar"
    flat
  >
    <div
      v-show="User.isAuthorized && Quiz.quizHasStarted && !Quiz.quizHasEnded"
      class="quiz-bar-rank"
    >
      <div class="level-display">Level</div>
      <div class="rank">{{ User.rank }}</div>
    </div>
    <v-container fluid>
      <v-row>
        <v-col cols="2">
          <router-link :to="{ name: 'redirect' }">
            <img
              alt="CodeWizardsHQ Code Challenge"
              height="80"
              src="/images/logo-with-code-challenge.svg"
            />
          </router-link>
        </v-col>
        <v-col>
          <p
            v-if="User.isAuthorized"
            class="archivo mt-7 ml-10"
            style="position: relative;"
          >
            Welcome, {{ User.displayName }}
          </p>

          <router-link
            v-else
            :to="{ name: 'register' }"
            active-class="none"
            color="secondary"
            text
            x-large
            >Start your journey
          </router-link>
        </v-col>

        <v-col class="text-right mt-7">
          <v-menu offset-y>
            <template v-slot:activator="{ on: menu }">
              <a v-on="menu" href="#">Get Help</a>
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
            >Sign In
          </router-link>

          <router-link v-if="User.isAuthorized" :to="{ name: 'logout' }"
            >Logout
          </router-link>
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
