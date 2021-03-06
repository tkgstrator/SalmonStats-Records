import Vue from 'vue'
import Router from 'vue-router'
import { normalizeURL, decode } from '@nuxt/ufo'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _48a3cb6e = () => interopDefault(import('../pages/database.vue' /* webpackChunkName: "pages/database" */))
const _38d82274 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))
const _694bbca0 = () => interopDefault(import('../pages/ocean.vue' /* webpackChunkName: "pages/ocean" */))

// TODO: remove in Nuxt 3
const emptyFn = () => {}
const originalPush = Router.prototype.push
Router.prototype.push = function push (location, onComplete = emptyFn, onAbort) {
  return originalPush.call(this, location, onComplete, onAbort)
}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: '/',
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/database",
    component: _48a3cb6e,
    name: "database___ja"
  }, {
    path: "/en",
    component: _38d82274,
    name: "index___en"
  }, {
    path: "/ocean",
    component: _694bbca0,
    name: "ocean___ja"
  }, {
    path: "/en/database",
    component: _48a3cb6e,
    name: "database___en"
  }, {
    path: "/en/ocean",
    component: _694bbca0,
    name: "ocean___en"
  }, {
    path: "/",
    component: _38d82274,
    name: "index___ja"
  }],

  fallback: false
}

function decodeObj(obj) {
  for (const key in obj) {
    if (typeof obj[key] === 'string') {
      obj[key] = decode(obj[key])
    }
  }
}

export function createRouter () {
  const router = new Router(routerOptions)

  const resolve = router.resolve.bind(router)
  router.resolve = (to, current, append) => {
    if (typeof to === 'string') {
      to = normalizeURL(to)
    }
    const r = resolve(to, current, append)
    if (r && r.resolved && r.resolved.query) {
      decodeObj(r.resolved.query)
    }
    return r
  }

  return router
}
