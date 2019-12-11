import { mapState } from "vuex";
import { Auth } from "@/api";

const moduleName = "User";

function getDefaultState() {
  return {
    firstName: "",
    lastName: "",
    email: "",
    displayName: "",
    isAuthorized: false
  };
}

const state = {
  ...getDefaultState()
};

const actions = {
  async refresh({ dispatch, commit }) {
    const user = Auth.currentUser();
    if (user.uid) {
      commit("set", user);
      dispatch("Progress/fetch", null, { root: true });
    } else {
      commit("clear", user);
      dispatch("Progress/clear", null, { root: true });
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
