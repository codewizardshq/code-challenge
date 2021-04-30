import Vue from "vue";
import VueRouter from "vue-router";
import { auth } from "@/api";
import store from "@/store";
import moment from "moment";

Vue.use(VueRouter);

function isChallengeOpen() {
  return store.state.Quiz.quizHasStarted && !store.state.Quiz.quizHasEnded;
}

function isChallengePending() {
  return !store.state.Quiz.quizHasStarted && !store.state.Quiz.quizHasEnded;
}

function isChallengeClosed() {
  return store.state.Quiz.quizHasEnded;
}

async function logout() {
  await store.dispatch("Quiz/reset");
  await auth.logout();
}

// dates for determining components to render

// start and end time for questions before boss question
let mainQuestionsStartTime = moment("5 Apr 2021 08:00:00 CDT");
let mainQuestionsEndTime = moment("25 Apr 2021 23:59:59 CDT");

// start and end time for boss question (final question)
let bossStartTime = moment("26 Apr 2021 08:00:00 CDT");
let bossEndTime = moment("30 Apr 2021 23:59:59 CDT");

// start and end time for voting
let votingStartTime = moment("3 May 2021 08:00:00 CDT");
let votingEndTime = moment("7 May 2021 23:59:59 CDT");

// easy route testing by passing a date string below
const getCurrentTime = function() {
  return moment();
};

const routes = [
  // testing route
  {
    path: "/testing",
    component: () => import("@/views/Voting/App"),
    children: [
      {
        path: "vote",
        name: "vote",
        component: () => import("@/views/Voting/Ballot")
      }
    ]
  },
  {
    // basically a dynamic home page
    path: "/",
    name: "redirect",
    beforeEnter(to, from, next) {
      // for testing
      if (to.path === "/testing/vote") {
        next({ path: "/testing/vote" });
        return;
      }
      if (isChallengeOpen() || isChallengePending()) {
        next({ name: "quiz" });
        return;
      }

      if (isChallengeClosed()) {
        next({ name: "voting" });
        return;
      }
    }
  },
  {
    // public routes
    path: "/",
    component: () => import("@/views/Public/App"),
    children: [
      {
        path: "frequently-asked-questions",
        name: "faq",
        component: () => import("@/views/Public/FAQ")
      }
    ]
  },
  // FOR EXTERNAL IFRAME
  {
    path: "/iframe/leaderboard",
    name: "iframe-leaderboard",
    component: () => import("@/views/IFrame/Leaderboard")
  },
  {
    // account routes
    path: "/",
    component: () => import("@/views/Public/App"),
    children: [
      {
        path: "login",
        name: "login",
        component: () => import("@/views/Accounts/Login"),
        meta: { anon: true }
      },
      {
        path: "forgot-password",
        name: "forgot-password",
        component: () => import("@/views/Accounts/ForgotPassword")
      },
      {
        path: "reset-password/:token",
        name: "reset-password",
        component: () => import("@/views/Accounts/ResetPassword")
      },
      {
        path: "create-account",
        name: "register",
        component: () => {
          return import("@/views/Accounts/Register");
        },
        meta: { anon: true, challengeOpenOrPending: true }
      },
      {
        path: "logout",
        name: "logout",
        beforeEnter: (to, from, next) =>
          logout().then(() => next({ name: "login" })),
        meta: { auth: true }
      },
      {
        path: "admin",
        name: "admin",
        component: () => import("@/views/Accounts/Admin"),
        meta: { auth: true }
      },
      {
        path: "super-secret-rank-page",
        name: "super-secret-rank-page",
        component: () => import("@/views/Accounts/SuperSecretRank"),
        meta: { auth: true }
      }
    ]
  },
  {
    // voting routes
    path: "/",
    component: () => import("@/views/Voting/App"),
    children: [
      {
        path: "voting",
        name: "voting",
        component: () => {
          const now = getCurrentTime();

          // show VoteWoah if before vote start time
          if (now < votingStartTime) {
            return import("@/views/Voting/VoteWoah");
          }

          // show VotingOver if past vote end time
          if (now > votingEndTime) {
            // TODO: add a leaderboard here once built
            return import("@/views/Voting/VotingOver");
          }

          // show Ballot otherwise
          return import("@/views/Voting/Ballot");
        }
      }
    ]
  },
  {
    // quiz routes
    path: "/",
    component: () => import("@/views/Public/App"),
    meta: { secured: true, challengeOpenOrPending: true },
    children: [
      {
        path: "quiz",
        name: "quiz",
        component: async () => {
          const now = getCurrentTime();

          // time before challenge has started
          if (now < mainQuestionsStartTime) {
            // TODO: update QuizCountdown's content for 2022's before start time
            return import("@/views/Quiz/QuizCountdown");
          }

          // time during main quiz
          if (now >= mainQuestionsStartTime && now <= mainQuestionsEndTime) {
            // USER HAS FINISHED QUIZ
            // TODO: for 2022 import a 'you finished now wait for boss' component
            // if done will all questions except boss

            // NORMAL QUIZ MODE
            return import("@/views/Quiz/Quiz");
          }

          // time between main questions ending and boss starting
          if (now > mainQuestionsEndTime && now < bossStartTime) {
            // TODO: for 2022 make an await final boss component, or start passing props to QuizCountdown

            // MUST WAIT FOR NEXT QUESTION
            return import("@/views/Quiz/QuizCountdown");
          }

          // time during boss final question
          if (now >= bossStartTime && now <= bossEndTime) {
            // user has finished the boss question
            if (store.state.Quiz.maxRank === store.state.User.rank - 1) {
              return import("@/views/Quiz/QuizFinished");
            }

            // User did not make the cut
            if (
              store.state.Quiz.rankToday == store.state.Quiz.maxRank &&
              store.state.User.rank != store.state.Quiz.rankToday
            ) {
              return import("@/views/Quiz/QuizFinishedFail");
            }

            // show boss question
            if (store.state.Quiz.isLastQuestion) {
              return import("@/views/Quiz/QuizFinalQuestion");
            }
          }

          // time after boss question ends and before voting
          if (now > bossEndTime && now < votingStartTime) {
            // user has finished the boss question
            if (store.state.Quiz.maxRank === store.state.User.rank - 1) {
              return import("@/views/Quiz/QuizFinished");
            }

            // if time is up and they did not finish, they failed
            return import("@/views/Quiz/QuizFinishedFail");
          }

          // times after voting starts are handled in the route guard
          // TODO: make a component that alerts before redirect to /voting for better user experience
        },
        beforeEnter(from, to, next) {
          const now = getCurrentTime();

          // redirect if all sections of quiz are over
          if (now >= votingStartTime) {
            next("/voting");
          }

          // USER MUST SEE INTRO VIDEO
          if (
            isChallengeOpen() &&
            !store.state.Quiz.hasSeenIntro &&
            store.state.User.rank == 1
          ) {
            next({ name: "quiz-intro" });
            return;
          }
          next();
        }
      },
      {
        path: "/quiz/intro",
        name: "quiz-intro",
        component: () => import("@/views/Quiz/QuizIntro")
      }
    ]
  },
  {
    // quiz routes
    path: "/",
    component: () => import("@/views/Public/App"),
    meta: { secured: false },
    children: [
      {
        path: "voting-tips",
        name: "voting-tips",
        component: () => import("@/views/Public/VotingFAQ")
      },
      {
        path: "voting-rules",
        name: "voting-rules",
        component: () => import("@/views/Public/VotingRules")
      },
      {
        path: "mission",
        name: "mission",
        component: () => import("@/views/Public/MissionPrep")
      }
    ]
  },
  {
    path: "*",
    name: "wildcard",
    redirect: { name: "redirect" }
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

router.beforeEach(async (to, from, next) => {
  // for testing
  if (to.path === "/testing/vote") {
    next();
    return;
  }

  const requireAuth = to.matched.some(record => record.meta.secured);
  const requireAnon = to.matched.some(record => record.meta.anon);
  const requireChallengePending = to.matched.some(
    record => record.meta.challengePending
  );
  const requireChallengeOpen = to.matched.some(
    record => record.meta.challengeOpen
  );
  const requireChallengeClosed = to.matched.some(
    record => record.meta.challengeOver
  );
  const requireChallengeOpenPending = to.matched.some(
    record => record.meta.challengeOpenOrPending
  );
  if (
    requireChallengePending ||
    requireChallengeOpen ||
    requireChallengeClosed ||
    requireChallengeOpenPending
  ) {
    try {
      await store.dispatch("Quiz/refresh");

      const challengeIsClosed = isChallengeClosed();
      const challengeIsPending = isChallengePending();
      const challengeIsOpen = isChallengeOpen();

      if (!challengeIsClosed && requireChallengeClosed) {
        next({ name: "redirect" });
        return;
      }

      if (!challengeIsOpen && requireChallengeOpen) {
        next({ name: "redirect" });
        return;
      }

      if (!challengeIsPending && requireChallengePending) {
        next({ name: "redirect" });
        return;
      }

      if (
        !challengeIsOpen &&
        !challengeIsPending &&
        requireChallengeOpenPending
      ) {
        next({ name: "redirect" });
        return;
      }
    } catch (err) {
      //continue
    }
  }

  if (requireAuth || requireAnon) {
    const isAuthenticated = !!auth.currentUser().auth;

    if (!isAuthenticated && requireAuth) {
      next({ name: "register" });
      return;
    }

    if (isAuthenticated && requireAnon) {
      next({ name: "redirect" });
      return;
    }
  }

  next();
});

export default router;
