import Vue from "vue";
import VueRouter from "vue-router";
import { Auth } from "@/api";

Vue.use(VueRouter);

const routes = [
  {
    path: "/home",
    name: "home",
    component: () => import("@/views/Home")
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/About")
  },
  {
    path: "/get-help",
    name: "get-help",
    component: () => import("@/views/GetHelp")
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
    path: "/logout",
    name: "logout",
    beforeEnter(to, from, next) {
      Auth.logout().then(() => next({ name: "home" }));
    },
    meta: {
      secured: true
    }
  },
  {
    path: "/create-account",
    name: "register",
    component: () => import("@/views/Register"),
    meta: {
      anon: true
    }
  },
  {
    path: "/quiz",
    name: "quiz",
    component: () => import("@/views/Quiz"),
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
  const isAuthenticated = !!Auth.currentUser().uid;
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
