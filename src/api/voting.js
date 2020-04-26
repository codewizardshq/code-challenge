import routes from "./routes";
import request from "./request";

function processBallotResponse(result) {
  if (result.items) {
    result.items = result.items.map(item => {
      return {
        id: item[0],
        text: item[1],
        numVotes: item[2],
        firstName: item[3],
        lastName: item[4],
        username: item[5],
        displayName: item[6],
        ...{ initials: initials(item) }
      };
    });
  }
  return result;
}

function lastInitial(item) {
  if (item[4]) {
    // lastName
    return item[4][0];
  }

  const split = item[5].split(" "); // userName
  return split.length >= 2 ? split[1] : "";
}

function firstInitial(item) {
  if (item[3]) {
    // firstName
    return item[3][0];
  }
  if (item[6]) {
    // displayName
    return item[6][0];
  }

  return item[5].split(" ")[0];
}

function initials(item) {
  return `${firstInitial(item)}${lastInitial(item)}`;
}

async function getBallot(page, per) {
  return processBallotResponse(
    await request(routes.voting_ballot, {
      params: { page, per }
    })
  );
}

async function cast(answerId, email) {
  return request(routes.voting_cast(answerId), { data: { email } });
}

async function confirm(token) {
  return request(routes.voting_confirm, { data: { token } });
}

async function search(text, page, per) {
  return processBallotResponse(
    await request(routes.voting_ballot_search, {
      params: { q: text, page, per }
    })
  );
}

export default {
  getBallot,
  cast,
  confirm,
  search
};
