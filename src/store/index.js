import Vue from 'vue'
import Vuex from 'vuex'
import User from "./user";
import Progress from "./progress";
import Snackbar from "./snackbar";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    User,
    Progress,
    Snackbar
  }
})

export { User, Progress, Snackbar };
