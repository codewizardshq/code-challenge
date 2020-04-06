import routes from "./routes";
import request from "./request";

async function getQuestion() {
  return request(routes.questions_api_next_question);
}

async function getRank() {
  return request(routes.questionsapi_get_rank);
}

async function resetRank() {
  await request(routes.questionsapi_rank_reset);
}

async function submit(answer) {
  const result = await request(routes.questionsapi_answer_next_question, {
    data: {
      text: answer
    }
  });
  return result.correct;
}

async function getLeaderboard() {
  return request(routes.questionsapi_leaderboard, { params: { per: 1500 } });
}

async function submitFinal(answer, language, checkOnly) {
  const result = await request(routes.questionsapi_answer_final_question, {
    data: {
      checkOnly,
      text: answer,
      language
    }
  });
  return result;
}

export default {
  getQuestion,
  submit,
  submitFinal,
  getRank,
  resetRank,
  getLeaderboard
};
