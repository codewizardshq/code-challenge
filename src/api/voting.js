import routes from "./routes";
import request from "./request";

function processBallotResponse(result) {
  if (result.items) {
    result.items = result.items.map(item => {
      return {
        // id: item[0],
        // text: item[1],
        // numVotes: item[2],
        // firstName: item[3],
        // lastName: item[4],
        // username: item[5],
        // displayName: item[6],
        // disqualified: item[7],
        ...item,
        ...{ initials: initials(item) }
      };
    });
  }
  return result;
}

function lastInitial(item) {
  if (item.lastName) {
    // lastName
    return item.lastName[0];
  }

  const split = item.username.split(" "); // userName
  return split.length >= 2 ? split[1] : "";
}

function firstInitial(item) {
  if (item.firstName) {
    // firstName
    return item.firstName[0];
  }
  if (item.displayName) {
    // displayName
    return item.displayName[0];
  }

  return item.displayName.split(" ")[0];
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
  let usePage = !page ? 1 : page;
  return processBallotResponse(
    await request(routes.voting_ballot_search, {
      params: { q: text, page: usePage, per }
    })
  );
}
export default {
  getBallot,
  cast,
  confirm,
  search
};
