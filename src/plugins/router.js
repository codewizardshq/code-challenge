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
      name: 'quiz'
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
    beforeEnter(to, from, next) {
      auth.logout().then(() => next({ name: "home" }));
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
    path: "/quiz",
    name: "quiz",
    component: () => import("@/views/Quiz/Quiz"),
    meta: {
      secured: true
    },
    beforeEnter: async (to, from, next) => {
      await store.dispatch("Quiz/refresh");

      if (store.state.Quiz.quizHasEnded) {
        next({ name: 'quiz-finished' });
        return;
      }

      if (!store.state.Quiz.quizHasStarted) {
        // quiz has not started
        next({ name: 'quiz-countdown' });
        return;
      }

      if (store.state.Quiz.awaitNextQuestion) {
        // next question is not unlocked
        next({ name: 'quiz-countdown' });
        return;
      }

      if (!store.state.Quiz.hasSeenIntro && store.state.User.rank == 0) {
        // user probably should see the intro video 
        next({ name: "quiz-intro" });
        return;
      }

      if (store.state.Quiz.isLastQuestion) {
        next({ name: 'quiz-final' });
        return;
      }

      // user is okay to take quiz 
      next();
    }
  },
  {
    path: "/quiz/countdown",
    name: "quiz-countdown",
    component: () => import("@/views/Quiz/QuizCountdown"),
    meta: {
      secured: true
    },
    beforeEnter: async (to, from, next) => {
      await store.dispatch("Quiz/refresh");

      if ((store.state.Quiz.quizHasEnded || store.state.Quiz.quizHasStarted) && !store.state.Quiz.awaitNextQuestion) {
        // quiz has not started
        next({ name: 'quiz' });
        return;
      }

      next();
    }
  },
  {
    path: "/quiz/finished",
    name: "quiz-finished",
    component: () => import("@/views/Quiz/QuizFinished")
  },
  {
    path: "/quiz/final",
    name: "quiz-final",
    component: () => import("@/views/Quiz/QuizFinalQuestion"),
    meta: {
      secured: true
    },
    beforeEnter: async (to, from, next) => {
      await store.dispatch("Quiz/refresh");

      if (!store.state.Quiz.isLastQuestion) {
        // user is not on the last question
        next({ name: 'quiz' });
        return;
      }

      next();
    }
  },
  {
    path: "/quiz/intro",
    name: "quiz-intro",
    component: () => import("@/views/Quiz/QuizIntro"),
    meta: {
      secured: true
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
