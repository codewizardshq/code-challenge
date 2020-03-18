import routes from './routes';
import request from './request';

function lastInitial(item) {
  if (item.lastName) {
    return item.lastName[0];
  }

  const split = item.username.split(' ');
  return split.length >= 2 ? split[1] : '';
}

function firstInitial(item) {
  if (item.firstName) {
    return item.firstName[0];
  }
  if (item.display) {
    return item.display[0];
  }

  return item.username.split(' ')[0];
}

function initials(item) {
  return `${firstInitial(item)}${lastInitial(item)}`;
}

async function getBallot(page, per) {
  const result = await request(routes.voting_ballot, {
    params: { page, per }
  });

  if (result.items) {
    result.items = result.items.map(item => {
      return { ...item, ...{ initials: initials(item) } };
    });
  }
  return result;
}

async function cast(answerId, email) {
  return request(routes.voting_cast(answerId), { data: { email } });
}

async function confirm(token) {
  return request(routes.voting_confirm, { data: { token } });
}

async function search(text) {
  return request(routes.voting_ballot_search, { query: { search: text } });
}

export default {
  getBallot,
  cast,
  confirm,
  search
};
