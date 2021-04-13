<template>
  <v-toolbar
    :height="80"
    :max-height="80"
    class="secondary--text"
    color="dark2 quiz-bar"
    src="/images/cwhq-pattern-bg.png"
    flat
  >
    <div
      v-show="User.isAuthorized && Quiz.quizHasStarted && !Quiz.quizHasEnded"
      class="quiz-bar-rank"
    >
      <!-- <div class="level-display">Level</div> -->
      <div class="rank">
        <p class="rank-text">{{ User.rank }}</p>
      </div>
    </div>
    <v-container fluid>
      <v-row>
        <v-col cols="3">
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
            class="archivo mt-7 primary--text welcome-text"
          >
            Welcome, {{ User.displayName }}
          </p>

          <div v-else class="mt-7">
            <router-link
              :to="{ name: 'register' }"
              active-class="none"
              color="secondary"
              class="archivo"
              text
              x-large
              >Start your journey
            </router-link>
          </div>
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
              <v-list-item href="https://discord.gg/NAufNzsJ8t" target="_blank">
                <v-list-item-title>Get Help On Discord</v-list-item-title>
              </v-list-item>
              <v-list-item
                href="https://www.facebook.com/events/212184353938197/"
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

<style lang="scss" scoped>
.list {
  padding: 20px;
}

.welcome-text {
  color: #f7e4c4 !important;
}

@media screen and (max-width: 1000px) {
  .welcome-text {
    display: none;
  }
}

.v-toolbar__content {
  background-image: url("/images/navbar-patterned-background.png");
}
</style>
