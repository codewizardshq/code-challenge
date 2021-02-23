import Vue from "vue";
import VueRouter from "vue-router";
import { auth } from "@/api";
import store from "@/store";

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

const routes = [
  {
    // basically a dynamic home page
    path: "/",
    name: "redirect",
    beforeEnter(to, from, next) {
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
          return import("@/views/Voting/VotingOver");
          // if (isChallengeClosed()) {
          //   return import("@/views/Voting/Ballot");
          // } else {
          //   return import("@/views/Voting/VoteWoah");
          // }
        }
      }
      // {
      //   path: "vote-confirmation",
      //   name: "voting-confirmation",
      //   meta: {
      //     challengeOver: true
      //   },
      //   component: () => import("@/views/Voting/Confirm")
      // }
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
          // CHALLENGE HAS NOT STARTED
          if (!isChallengeOpen()) {
            return import("@/views/Quiz/QuizCountdown");
          }

          // USER HAS FINISHED QUIZ
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

          // MUST WAIT FOR NEXT QUESTION
          if (store.state.Quiz.awaitNextQuestion) {
            return import("@/views/Quiz/QuizCountdown");
          }

          // SHOW THE LAST QUESTION
          if (store.state.Quiz.isLastQuestion) {
            return import("@/views/Quiz/QuizFinalQuestion");
          }

          // NORMAL QUIZ MODE
          return import("@/views/Quiz/Quiz");
        },
        beforeEnter(from, to, next) {
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
