import routes from "./routes";
import request from "./request";

async function getBallot() {
  return request(routes.voting_ballot);
}

export default {
  getBallot
};
