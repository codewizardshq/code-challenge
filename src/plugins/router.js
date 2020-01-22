import Vue from "vue";
import VueRouter from "vue-router";
import { auth } from "@/api";
import store from "@/store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/home",
    name: "home",
    component: () => import("@/views/Home")
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
    path: "/reset-password",
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
    component: () => import("@/views/Quiz"),
    meta: {
      secured: true
    },
    beforeEnter: (to, from, next) => {
      if (!store.state.Quiz.hasSeenIntro && store.state.User.rank == 0) {
        next({ name: "quiz-intro" });
      } else {
        next();
      }
    }
  },
  {
    path: "/quiz-scores",
    name: "quiz-scores",
    component: () => import("@/views/QuizScores"),
    meta: {
      secured: true
    },
    beforeEnter: (to, from, next) => {
      if (!store.state.Quiz.hasScores) {
        next({ name: "quiz" });
      } else {
        next();
      }
    }
  },
  {
    path: "/quiz-intro",
    name: "quiz-intro",
    component: () => import("@/views/QuizIntro"),
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
    next({ name: "home" });
    return;
  }

  if (isAuthenticated && requireAnon) {
    next({ name: "home" });
    return;
  }

  next();
});

export default router;
