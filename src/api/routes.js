function route(path, type) {
  return {
    path,
    type
  };
}

export default {
  awsebapi_eb_health_check: route("/api/v1/eb/health", "GET"),
  userapi_register: route("/api/v1/users/register", "POST"),
  userapi_login: route("/api/v1/users/token/auth", "POST"),
  userapi_logout: route("/api/v1/users/token/remove", "POST"),
  userapi_hello: route("/api/v1/users/hello", "GET"),
  userapi_forgot: route("/api/v1/users/forgot", "POST"),
  userapi_refresh: route("/api/v1/users/token/refresh", "POST"),
  userapi_forgot_password: route("/api/v1/users/forgot", "POST"),
  userapi_reset_password: route("/api/v1/users/reset-password", "POST"),
  questionsapi_rank_reset: route("/api/v1/questions/reset", "DELETE"),
  questionsapi_answer_next_question: route("/api/v1/questions/answer", "POST"),
  questionsapi_answer_final_question: route("/api/v1/questions/final", "POST"),
  questionsapi_get_rank: route("/api/v1/questions/rank", "GET"),
  questionsapi_leaderboard: route("/api/v1/questions/leaderboard", "GET"),
  questions_api_next_question: route("/api/v1/questions/next", "GET"),
  voting_check: route("/api/v1/vote/check", "GET"),
  voting_ballot: route("/api/v1/vote/ballot", "GET"),
  voting_cast: id => {
    return route(`/api/v1/vote/${id}/cast`, "POST");
  },
  voting_confirm: route("/api/v1/vote/confirm", "POST")
};

// export default {
//   awsebapi_eb_health_check: '/api/v1/eb/health',
// catch_all                          GET      /<path:path>
// catch_all                          GET      /
// questionsapi.answer_next_question  POST     /api/v1/questions/answer
// questionsapi.get_rank              GET      /api/v1/questions/rank
// questionsapi.next_question         GET      /api/v1/questions/next
// send_css                           GET      /css/<path:path>
// send_fonts                         GET      /fonts/<path:path>
// send_images                        GET      /images/<path:path>
// send_js                            GET      /js/<path:path>
// static                             GET      /static/<path:filename>
// userapi.forgot_password            POST     /api/v1/users/forgot
// userapi.hello_protected            GET      /api/v1/users/hello
// userapi.login                      POST     /api/v1/users/token/auth
// userapi.logout                     POST     /api/v1/users/token/remove
// userapi.refresh                    POST     /api/v1/users/token/refresh
// userapi.register                   POST     /api/v1/users/register
// userapi.reset_password             POST     /api/v1/users/reset-password
// }
