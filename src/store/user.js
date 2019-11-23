import { mapState } from "vuex";

const moduleName = "User";

function getDefaultState() {
  return {
    username: "",
    name: "",
    isAuthroized: false
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

