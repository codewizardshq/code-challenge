import Vue from "vue";
import routes from "./routes";
import request from "./request";

const eventKey = "_authChange";

const eventHandler = new Vue();

let state = {
  auth: false,
  email: null,
  displayName: null,
  firstName: null,
  lastName: null
};

async function setState(newState) {
  state = { ...state, ...newState };
  eventHandler.$emit(eventKey, state);
}

async function onAuthStateChange(callback) {
  eventHandler.$on(eventKey, callback);
}

async function offAuthStateChange(callback) {
  eventHandler.$on(eventKey, callback);
}

async function login(email, password) {
  await request(routes.userapi_login, {
    data: {
      username: email,
      password
    }
  });
  await fetchState();
}

async function createAccount(email, password, firstName, lastName) {
  await request(routes.userapi_register, {
    data: {
      username: email,
      password,
      email,
      firstname: firstName,
      lastname: lastName
    }
  });
  await login(email, password);
}

async function fetchState() {
  const userData = await request(routes.userapi_hello);
  await setState({
    email: userData.email,
    firstName: userData.firstname,
    lastName: userData.lastname,
    displayName: userData.firstname + " " + userData.lastname,
    auth: true
  })
}

async function autoLogin() {
  try {
    await fetchState();
  } catch (err) {
    if (err.status != 401) {
      return Promise.reject(err);
    }
  }
}

async function logout() {
  await request(routes.userapi_logout);
  await setState({ auth: false });
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
};
