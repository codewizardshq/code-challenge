import routes from "./routes";
import request from "./request";

async function getBallot(page, per) {
  return request(routes.voting_ballot, {
    params: { page, per }
  });
}

async function cast(answerId, email) {
  return request(routes.voting_cast(answerId), { data: { email } });
}

async function confirm(token) {
  return request(routes.voting_confirm, { data: { token } });
}

export default {
  getBallot,
  cast,
  confirm
};
