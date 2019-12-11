import { mapState } from "vuex";

const moduleName = "Snackbar";

function getDefaultState() {
  return {
    isOpen: false,
    text: "",
    color: ""
  };
}

const state = {
  ...getDefaultState()
};

const actions = {
  async showInfo({ commit }, text) {
    commit("set", {
      text: text.message ? text.message : text,
      isOpen: true,
      color: "info"
    });
  },
  async showError({ commit }, text) {
    commit("set", {
      text: text.message ? text.message : text,
      isOpen: true,
      color: "error"
    });
  },
  async showSuccess({ commit }, text) {
    commit("set", {
      text: text.message ? text.message : text,
      isOpen: true,
      color: "success"
    });
  },
  async hide({ commit }) {
    commit("set", {
      isOpen: false
    });
  },
  async isOpen({ commit }, value) {
    commit("isOpen", value);
  }
};

const mutations = {
  set(state, data) {
    Object.assign(state, data);
  },
  isOpen(state, value) {
    state.isOpen = value;
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
