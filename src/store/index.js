import Vue from 'vue'
import Vuex from 'vuex'
import User from "./user";
import Progress from "./progress";

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
    Progress
  }
})

export { User, Progress };
