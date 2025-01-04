import {createRouter, createWebHistory} from 'vue-router/auto'
import {Router, RouteRecordRaw} from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/welcome'
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  },
  {
    path: '/404',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: {title: 'AQT - Not Found'}
  },
  {
    path: '/home',
    component: () => import('@/pages/Home.vue'),
    meta: {title: 'AQT - Home'}
  },
  {
    path: '/login',
    component: () => import('@/pages/Login.vue'),
    meta: {title: 'AQT - Login'}
  },
  {
    path: '/not-found-page',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: {title: 'AQT - NotFoundPage'}
  },
  {
    path: '/person',
    component: () => import('@/pages/Person.vue'),
    meta: {title: 'AQT - Person'}
  },
  {
    path: '/register',
    component: () => import('@/pages/Register.vue'),
    meta: {title: 'AQT - Register'}
  },
  {
    path: '/welcome',
    component: () => import('@/pages/Welcome.vue'),
    meta: {title: 'AQT - Welcome'}
  },





  
]

const router: Router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, _, next) => {
  if (to.meta && to.meta.title) {
    document.title = to.meta.title as string
  } else {
    document.title = 'TJLinker'
  }
  next()
})

router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router



