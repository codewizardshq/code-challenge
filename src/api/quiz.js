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

async function submitFinal(answer, language) {
  const result = await request(routes.questionsapi_answer_final_question, {
    data: {
      text: answer,
      language
    }
  })
  return result;
}

export default {
  getQuestion,
  submit,
  submitFinal,
  getRank,
  resetRank
};
