import Vue from "vue";
import App from "./App.vue";
import router from "./plugins/router";
import vuetify from "./plugins/vuetify";
import "./plugins/moment";
import store from "./store";
import "@/styles/styles.scss";
import { auth } from "@/api";
import './plugins/codemirror';
Vue.config.productionTip = false;

(async function () {
  auth.onAuthStateChange(function () {
    store.dispatch("User/refresh");
  });

  await auth.autoLogin();
  await store.dispatch('Quiz/refresh');

  new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
  }).$mount("#app");
})();
