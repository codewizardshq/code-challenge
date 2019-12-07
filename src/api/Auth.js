import Vue from "vue";

const storageKey = "_authKey";
const eventKey = "_authChange";

const eventHandler = new Vue();

let state = {
  uid: null,
  email: null,
  displayName: null,
  firstName: null,
  lastName: null
};

async function setState(newState) {
  state = { ...state, ...newState };
  localStorage.setItem(eventKey, JSON.stringify(state));
  eventHandler.$emit(eventKey, state);
}

async function loadState() {
  const json = localStorage.getItem(eventKey);
  if (!!json) {
    setState(JSON.parse(json));
  }
}

async function onAuthStateChange(callback) {
  eventHandler.$on(eventKey, callback);
}

async function offAuthStateChange(callback) {
  eventHandler.$on(eventKey, callback);
}

async function login(email, password) {
  await setState({
    uid: email,
    email,
    displayName: email
  });
}

async function createAccount(username, email, password, firstName, lastName) {
  await setState({
    uid: email,
    username,
    email,
    firstName,
    lastName,
    displayName: username
  });
}

async function autoLogin() {
  await loadState();
}

async function logout() {
  await setState({ uid: null });
}


function currentUser() {
  return { ...state };
}

export default {
  logout,
  login,
  autoLogin,
  createAccount,
  currentUser,
  onAuthStateChange,
  offAuthStateChange
}