import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/Home')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/About')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login')
  },
  {
    path: '/logout',
    name: 'logout',
    component: () => import('@/views/Login')
  },
  {
    path: '/create-account',
    name: 'register',
    component: () => import('@/views/Register')
  },
  {
    path: '/quiz',
    name: 'quiz',
    component: () => import('@/views/Quiz')
  },
  {
    path: '*',
    name: 'redirect',
    redirect: {
      name: 'home'
    }
  },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
