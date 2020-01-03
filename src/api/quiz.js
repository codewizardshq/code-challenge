import routes from "./routes";
import request from "./request";

async function getQuestion() {
  return request(routes.questions_api_next_question);
}

async function getRank() {
  return (await request(routes.questionsapi_get_rank)).rank;
}

async function submit(answer) {
  const result = await request(routes.questionsapi_answer_next_question, {
    data: {
      text: answer
    }
  });
  return result.correct;
}

export default {
  getQuestion,
  submit,
  getRank
};
