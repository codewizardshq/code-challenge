import Vue from "vue";
import routes from "./routes";
import request from "./request";

const eventKey = "_authChange";

const eventHandler = new Vue();

let state = {
  auth: false,
  username: null,
  displayName: null,
  firstName: null,
  lastName: null,
  rank: -1
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

async function login(username, password) {
  await request(routes.userapi_login, {
    data: {
      username,
      password
    }
  });
  await fetchState();
}

async function createAccount(data) {
  await request(routes.userapi_register, { data }, false);
  await login(data.username, data.password, false);
}

async function requestPasswordReset(email) {
  await request(routes.userapi_forgot, { data: { email } });
}

async function fetchState() {
  const userData = await request(routes.userapi_hello, {}, state.auth);
  await setState({
    username: userData.username,
    firstName: userData.firstname,
    lastName: userData.lastname,
    displayName: userData.firstname + " " + userData.lastname,
    auth: true,
    rank: userData.rank
  });
}

async function autoLogin() {
  try {
    await fetchState();
  } catch (err) {
    if (err.status !== 401) {
      return Promise.reject(err);
    }
  }
}

async function logout() {
  await request(routes.userapi_logout, {}, false);
  await setState({ auth: false, rank: -1 });
}

function currentUser() {
  return { ...state };
}

async function forgotPassword(email) {
  return await request(
    routes.userapi_forgot_password,
    { data: { email } },
    false
  );
}

async function resetPassword(token, password) {
  return await request(
    routes.userapi_reset_password,
    { data: { token, password } },
    false
  );
}

async function doesUsernameExist(username) {
  return await request(routes.userapi_user_exists(username));
}

export default {
  doesUsernameExist,
  logout,
  login,
  autoLogin,
  fetchState,
  createAccount,
  currentUser,
  requestPasswordReset,
  onAuthStateChange,
  offAuthStateChange,
  forgotPassword,
  resetPassword
};
