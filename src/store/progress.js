import { mapState } from "vuex";
import { Quiz } from "@/api";

const moduleName = "Progress";

function getDefaultState() {
  return {
    rank: -1,
    question: "",
    hasData: false,
    isLoading: false
  };
}

const actions = {
  async fetch({ commit }) {
    commit("loading", true);
    const data = await Quiz.get();
    commit("rank", data.rank);
    commit("question", data.question);
    commit("loading", false);
  },
  async clear({ commit }) {
    commit("rank", -1);
  }
};

const mutations = {
  rank(state, value) {
    state.rank = value;
    state.hasData = value >= 0;
  },
  question(state, value) {
    state.question = value;
  },
  loading(state, value) {
    state.isLoading = value;
  }
};

const state = {
  ...getDefaultState()
};

export default {
  namespaced: true,
  name: moduleName,
  state,
  actions,
  mutations,
  mapState: () => mapState([moduleName])
};
