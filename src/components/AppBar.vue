<template>
  <v-app-bar
    color="dark"
    flat
    dark
    :height="100"
    :max-height="100"
    class="pl-4"
  >
    <div class="d-flex align-center">
      <router-link :to="{ name: 'home' }">
        <v-img
          alt="CodewizardsHQ Logo"
          contain
          src="/images/logo-small.png"
          transition="scale-transition"
        />
      </router-link>
    </div>

    <v-spacer></v-spacer>

    <!-- <v-btn :to="{ name: 'home' }" v-bind="buttonProps">
      Home
		</v-btn>-->

    <!-- <v-btn :to="{ name: 'about' }" v-bind="buttonProps">
      About
		</v-btn>-->
    <v-btn :to="{ name: 'quiz' }" v-bind="buttonProps" v-if="User.isAuthorized"
      >Quiz</v-btn
    >
    <help-pop-over>
      <template v-slot:default="{ on }">
        <v-btn v-on="on" v-bind="buttonProps">Get Help</v-btn>
      </template>
    </help-pop-over>
    <v-btn
      :to="{ name: 'login' }"
      v-bind="buttonProps"
      v-if="!User.isAuthorized"
      >Sign In</v-btn
    >
    <v-btn
      :to="{ name: 'register' }"
      v-bind="buttonProps"
      v-if="!User.isAuthorized"
      >Create Account</v-btn
    >
    <v-btn
      :to="{ name: 'logout' }"
      v-bind="buttonProps"
      v-if="User.isAuthorized"
      >Sign Out</v-btn
    >
  </v-app-bar>
</template>

<script>
import { User } from "@/store";
import HelpPopOver from "./HelpPopOver";
export default {
  name: "appBar",
  components: {
    HelpPopOver
  },
  computed: {
    ...User.mapState()
  },
  data() {
    return {
      buttonProps: {
        text: true,
        xLarge: true,
        class: "barrow-bold"
      }
    };
  },
  methods: {
    getHelp() {}
  }
};
</script>
