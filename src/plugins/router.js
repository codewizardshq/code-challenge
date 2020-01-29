import Vue from "vue";
import VueRouter from "vue-router";
import { auth } from "@/api";
import store from "@/store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/home",
    name: "home",
    redirect: {
      name: "quiz"
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
    component: () => import("@/views/Voting/Ballot.vue")
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
      console.log("Start");
      await store.dispatch("Quiz/refresh");

      // CHALLENGE IS OVER
      if (store.state.Quiz.quizHasEnded) {
        console.log("Ended");
        return import("@/views/Quiz/QuizFinished");
      }

      // CHALLENGE HAS NOT STARTED
      if (!store.state.Quiz.quizHasStarted) {
        console.log("Not started");
        return import("@/views/Quiz/QuizCountdown");
      }

      // USER HAS FINISHED QUIZ
      console.log(store.state.Quiz.maxRank, store.state.User.rank - 1);
      if (store.state.Quiz.maxRank === store.state.User.rank - 1) {
        console.log("Has finished");
        return import("@/views/Quiz/QuizFinished");
      }

      // MUST WAIT FOR NEXT QUESTION
      if (store.state.Quiz.awaitNextQuestion) {
        console.log("Must await");
        return import("@/views/Quiz/QuizCountdown");
      }

      // SHOW THE LAST QUESTION
      if (store.state.Quiz.isLastQuestion) {
        console.log("Last question");
        return import("@/views/Quiz/QuizFinalQuestion");
      }
      // NORMAL QUIZ MODE
      return import("@/views/Quiz/Quiz");
    },
    beforeEnter(from, to, next) {
      // USER MUST SEE INTRO VIDEO
      if (!store.state.Quiz.hasSeenIntro && store.state.User.rank == 1) {
        next({ name: "quiz-intro" });
        return;
      }
      next();
    },
    meta: {
      secured: true
    }
  },
  {
    path: "/quiz/intro",
    name: "quiz-intro",
    component: () => import("@/views/Quiz/QuizIntro"),
    async beforeEnter(to, from, next) {
      await store.dispatch("Quiz/refresh");
      next();
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

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!auth.currentUser().auth;
  const requireAuth = to.matched.some(record => record.meta.secured);
  const requireAnon = to.matched.some(record => record.meta.anon);

  if (!isAuthenticated && requireAuth) {
    next({ name: "register" });
    return;
  }

  if (isAuthenticated && requireAnon) {
    next({ name: "home" });
    return;
  }

  next();
});

export default router;
