import { mapState } from "vuex";
import * as api from "@/api";
import Vue from "vue";

const moduleName = "User";

function getDefaultState() {
  return {
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    displayName: "",
    rank: 0,
    isAuthorized: false
  };
}

const state = {
  ...getDefaultState()
};

const actions = {
  async refresh({ commit }) {
    const user = api.auth.currentUser();
    user.rank = user.rank + 1;
    if (user.auth) {
      commit("set", user);
    } else {
      commit("clear", user);
    }
  }
};

const mutations = {
  set(state, user) {
    for (const [key, value] of Object.entries(user)) {
      Vue.set(state, key, value);
    }
    state.isAuthorized = true;
  },
  clear(state) {
    for (const [key, value] of Object.entries(getDefaultState())) {
      Vue.set(state, key, value);
    }
  }
};

export default {
  namespaced: true,
  name: moduleName,
  state,
  actions,
  mutations,
  mapState: () => mapState([moduleName])
};
