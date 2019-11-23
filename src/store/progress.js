import { mapState } from "vuex";

const moduleName = "Progress";

function getDefaultState() {
  return {
    rank: 21
  }
}

const state = {
  ...getDefaultState()
};

export default {
  namespaced: true,
  name: moduleName,
  state,
  mapState: () => mapState([moduleName])
}

