import { mapState } from "vuex";
import { quiz } from "@/api";
import moment from "moment";

const moduleName = "Quiz";

function parseDateResponse(dateResponse) {
  const timeSplit = dateResponse.split(',');
  let daysString = "0 days";
  let timeString = "0:0:0";

  if (timeSplit.length == 1) {
    // returning only timeString 
    timeString = timeSplit[0];
  } else if (timeSplit.length == 2) {
    // returning days and timeString
    daysString = timeSplit[0];
    timeString = timeSplit[1];
  } else {
    throw new Error("Unexpected error with time response");
  }
  const days = parseInt(daysString);
  const time = timeString.split(':');
  const hours = time[0];
  const minutes = time[1];
  const seconds = time[2];
  return moment().add(days, "days").add(hours, "hours").add(minutes, "minutes").add(seconds, "seconds");
}

function getDefaultState() {
  return {
    hasSeenIntro: false,
    nextUnlockMoment: moment(),
    quizStartedMoment: moment(),
    question: "",
    asset: "",
    rank: 0,
    maxRank: 0,
    isLastQuestion: false,
    hints: ["", ""],
    wrongCount: !!localStorage.getItem("wrongCount") ? parseInt(localStorage.getItem("wrongCount")) : 0,
    quizHasStarted: false,
    quizHasEnded: false,
    awaitNextQuestion: false
  };
}

const state = {
  ...getDefaultState()
};

const actions = {
  async markAsSeen({ commit }) {
    commit("hasSeenIntro", true);
  },
  async addWrongCount({ state, commit }) {
    commit("wrongCount", state.wrongCount + 1);
  },
  async clearWrongCount({ commit }) {
    commit("wrongCount", 0);
  },
  async refresh({ state, commit }) {
    // get current rank and see if quiz has started
    try {
      const rank = await quiz.getRank();
      commit("maxRank", rank.maxRank);
      commit("quizStartedMoment", moment(rank.startsOn + "+0000", "MM/DD/YYYY HH:mm   Z"));

      if (rank.rank < 0) {
        commit("quizHasStarted", false);
        commit("awaitNextQuestion", false);
        commit("question", "");
        commit("asset", "");
        commit("rank", 0);
        commit("hints", ["", ""]);
        commit("nextUnlockMoment", parseDateResponse(rank.timeUntilNextRank))
        return;
      }
      commit("quizHasStarted", true);
      commit("rank", rank.rank);
    } catch (err) {
      if (err.status === 403) {
        commit("quizHasEnded", true);
        return;
      }
      throw new Error(err);
    }

    // get current question and see if question is even unlocked 
    try {
      const response = await quiz.getQuestion();
      commit("awaitNextQuestion", false);
      commit("question", response.question);
      commit("asset", response.asset);
      commit("rank", response.rank);
      commit("hints", response.hints);
      commit("nextUnlockMoment", moment());
      commit("isLastQuestion", response.rank === state.maxRank);
    } catch (err) {
      if (err.status === 404) {
        commit("awaitNextQuestion", true);
        commit("question", "");
        commit("asset", "");
        commit("rank", 0);
        commit("hints", ["", ""]);
        commit("nextUnlockMoment", parseDateResponse(err.data.timeUntilNextRank));
      } else if (err.status === 401) {
        commit("question", "");
        commit("asset", "");
        commit("rank", 0);
        commit("hints", ["", ""]);
      } else {
        console.error("An unexpected error occurred");
        console.error(err);
      }
    }
  }
};

const mutations = {
  quizHasStarted(state, value) {
    state.quizHasStarted = value;
  },
  hasSeenIntro(state, value) {
    state.hasSeenIntro = value;
  },
  awaitNextQuestion(state, value) {
    state.awaitNextQuestion = value;
  },
  nextUnlockMoment(state, value) {
    state.nextUnlockMoment = value;
  },
  question(state, value) {
    state.question = value;
  },
  rank(state, value) {
    state.rank = value;
  },
  asset(state, value) {
    state.asset = value;
  },
  quizStartedMoment(state, value) {
    state.quizStartedMoment = value;
  },
  wrongCount(state, value) {
    state.wrongCount = value;
    localStorage.setItem("wrongCount", state.wrongCount);
  },
  hints(state, value) {
    state.hints = value;
  },
  maxRank(state, value) {
    state.maxRank = value;
  },
  isLastQuestion(state, value) {
    state.isLastQuestion = value;
  },
  quizHasEnded(state, value) {
    state.quizHasEnded = value;
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
