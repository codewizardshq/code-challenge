<template>
  <v-toolbar
    color="dark2 pl-3 pr-3"
    flat
    class="secondary--text"
    :height="60"
    :max-height="60"
  >
    <div class="quiz-bar-rank" v-show="User.isAuthorized">
      <div class="level-display">Level</div>
      <div class="rank">{{ User.rank }}</div>
    </div>

    <span v-if="User.isAuthorized" class="barrow-bold">
      Welcome pilgrim {{ User.displayName }}
    </span>
    <v-btn
      v-else
      color="secondary"
      text
      x-large
      active-class="none"
      class="no-text-transform barrow-bold"
      :to="{ name: 'register' }"
    >
      Start your journey
    </v-btn>
    <v-spacer />
    <social-pop-over>
      <template v-slot:default="{ on }">
        <v-btn
          text
          x-large
          active-class=""
          color="secondary"
          class="no-text-transform barrow-bold"
          v-on="on"
        >
          Get your friends in on it
          <v-img
            class="ml-2 mb-2"
            alt="Share Icon"
            src="/images/shareicon.png"
          />
        </v-btn>
      </template>
    </social-pop-over>
  </v-toolbar>
</template>

<script>
import { User } from "@/store";
import SocialPopOver from "./SocialPopOver";

export default {
  name: "quizBar",
  components: {
    SocialPopOver
  },
  computed: {
    ...User.mapState()
  }
};
</script>
