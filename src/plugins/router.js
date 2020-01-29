import Vue from "vue";
import VueRouter from "vue-router";
import { auth, quiz } from "@/api";
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

const routes = [
  {
    path: "/home",
    name: "home",
    beforeEnter(to, from, next) {
      if (isChallengeOpen() || isChallengePending()) {
        next({ name: 'quiz' });
        return;
      }

      if (isChallengeClosed()) {
        next({ name: 'voting' })
        return;
      }
    }
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login"),
    meta: {
      anon: true
    }
  },
  {
    path: "/forgot-password",
    name: "forgot-password",
    component: () => import("@/views/ForgotPassword"),
    meta: { anon: true }
  },
  {
    path: "/reset-password/:token",
    name: "reset-password",
    component: () => import("@/views/ResetPassword")
  },
  {
    path: "/logout",
    name: "logout",
    async beforeEnter(to, from, next) {
      await store.dispatch("Quiz/reset");
      await auth.logout();
      next({ name: "login" });
    },
    meta: {
      secured: true
    }
  },
  {
    path: "/create-account",
    name: "register",
    component: () => import("@/views/Register/index.vue"),
    meta: {
      anon: true
    }
  },
  {
    path: "/admin",
    name: "admin",
    component: () => import("@/views/Admin.vue"),
    meta: {
      secured: true
    }
  },
  {
    path: "/voting",
    name: "voting",
    component: () => import("@/views/Voting/Ballot.vue"),
    meta: {
      challengeOver: true
    }
  },
  {
    // dev only
    path: "/leader-board",
    name: "leader-board",
    component: () => import("@/views/Voting/Leaderboard.vue")
  },
  {
    path: "/frequently-asked-questions",
    name: "faq",
    component: () => import("@/views/FAQ.vue")
  },
  {
    path: "/quiz",
    name: "quiz",
    component: async () => {
      await store.dispatch("Quiz/refresh");

      // CHALLENGE HAS NOT STARTED
      if (!isChallengeOpen()) {
        return import("@/views/Quiz/QuizCountdown");
      }

      // USER HAS FINISHED QUIZ
      if (store.state.Quiz.maxRank === store.state.User.rank - 1) {
        return import("@/views/Quiz/QuizFinished");
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
      if (isChallengeOpen() && !store.state.Quiz.hasSeenIntro && store.state.User.rank == 1) {
        next({ name: "quiz-intro" });
        return;
      }
      next();
    },
    meta: {
      secured: true,
      challengeOpenOrPending: true
    }
  },
  {
    path: "/quiz/intro",
    name: "quiz-intro",
    component: () => import("@/views/Quiz/QuizIntro"),
    meta: {
      secured: true,
      challengeOpenOrPending: true
    }
  },
  {
    path: "*",
    name: "redirect",
    redirect: {
      name: "home"
    }
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

router.beforeEach(async (to, from, next) => {
  const requireAuth = to.matched.some(record => record.meta.secured);
  const requireAnon = to.matched.some(record => record.meta.anon);
  const requireChallengePending = to.matched.some(record => record.meta.challengePending);
  const requireChallengeOpen = to.matched.some(record => record.meta.challengeOpen);
  const requireChallengeClosed = to.matched.some(record => record.meta.challengeOver);
  const requireChallengeOpenPending = to.matched.some(record => (record.meta.challengeOpenOrPending));

  if (requireChallengePending || requireChallengeOpen || requireChallengeClosed || requireChallengeOpenPending) {
    await store.dispatch("Quiz/refresh");

    const challengeIsClosed = isChallengeClosed();
    const challengeIsPending = isChallengePending();
    const challengeIsOpen = isChallengeOpen();

    if (!challengeIsClosed && requireChallengeClosed) {
      next({ name: 'home' });
      return;
    }

    if (!challengeIsOpen && requireChallengeOpen) {
      next({ name: 'home' });
      return;
    }

    if (!challengeIsPending && requireChallengePending) {
      next({ name: 'home' });
      return;
    }

    if ((!challengeIsOpen && !challengeIsPending) && requireChallengeOpenPending) {
      next({ name: 'home' });
      return;
    }
  }

  if (requireAuth || requireAnon) {
    const isAuthenticated = !!auth.currentUser().auth;

    if (!isAuthenticated && requireAuth) {
      next({ name: "register" });
      return;
    }

    if (isAuthenticated && requireAnon) {
      next({ name: "home" });
      return;
    }
  }

  next();
});

export default router;
