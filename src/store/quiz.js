import { mapState } from "vuex";

const moduleName = "Quiz";

function getDefaultState() {
  return {
    hasSeenIntro: false,
    hasScores: false
  };
}

const state = {
  ...getDefaultState()
};

const actions = {
  async markAsSeen({ commit }) {
    commit("hasSeenIntro", true);
  },
  async setScores({ commit }) {
    commit("scores", true);
  }
};

const mutations = {
  hasSeenIntro(state, value) {
    state.hasSeenIntro = value;
  },
  scores() {
    state.hasScores = true;
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
