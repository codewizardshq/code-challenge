import { mapState } from "vuex";
import * as api from "@/api";

const moduleName = "User";

function getDefaultState() {
  return {
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
  async refresh({ dispatch, commit }) {
    const user = api.auth.currentUser();
    if (user.auth) {
      const rank = await api.quiz.getRank();
      commit("set", { ...user, rank });
    } else {
      commit("clear", user);
    }
  }
};

const mutations = {
  set(state, user) {
    Object.assign(state, user);
    state.isAuthorized = true;
  },
  clear(state) {
    Object.assign(state, getDefaultState());
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
