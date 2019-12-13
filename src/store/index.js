import Vue from "vue";
import Vuex from "vuex";
import User from "./user";
import Snackbar from "./snackbar";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    User,
    Snackbar
  }
});

export { User, Snackbar };
