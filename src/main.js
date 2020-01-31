// don't mess with this order
import "@/styles/fonts.scss";
import "@/styles/styles.scss";

import Vue from "vue";
import App from "./App.vue";

import vuetify from "./plugins/vuetify";
import router from "./plugins/router";
import "./plugins/moment";
import "./plugins/codemirror";
import "./plugins/highlightjs";

import store from "./store";
import { auth } from "@/api";

Vue.config.productionTip = false;

(async function() {
  auth.onAuthStateChange(function() {
    store.dispatch("User/refresh");
  });

  try {
    await auth.autoLogin();
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error("Was unable to authenticate user");
  }

  try {
    await store.dispatch("Quiz/refresh");
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error("Was unable to refresh question status", err.reason);
  }

  new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
  }).$mount("#app");
})();
