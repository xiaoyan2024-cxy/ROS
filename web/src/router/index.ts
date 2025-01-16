import {createRouter, createWebHistory} from 'vue-router';
import root from './root';

import { ADMIN_USER_TOKEN, USER_TOKEN } from '/@/store/constants'

// 路由权限白名单
const allowList = ['adminLogin', 'login', 'register', 'portal', 'search', 'detail', '403', '404']
// 前台登录地址
const loginRoutePath = '/index/login'
// 后台登录地址
const adminLoginRoutePath = '/adminLogin'

// 用于创建一个路由实例，管理应用的路由配置和导航行为。
const router = createRouter({
  //使用 HTML5 模式的路由历史记录
  history: createWebHistory(),
  routes: root,
});

// 是 Vue Router 提供的一个导航守卫（navigation guard），用于在每次路由导航之前执行一些逻辑。它可以用来检查用户的身份验证状态、权限等，并决定是否允许导航继续。
router.beforeEach(async (to, from, next) => {
  console.log(to, from)

  /** 后台路由 **/
  if (to.path.startsWith('/admin')) {
    if (localStorage.getItem(ADMIN_USER_TOKEN)) {
      if (to.path === adminLoginRoutePath) {
        next({ path: '/' })
      } else {
        next()
      }
    } else {
      if (allowList.includes(to.name as string)) {
        // 在免登录名单，直接进入
        next()
      } else {
        next({ path: adminLoginRoutePath, query: { redirect: to.fullPath } })
      }
    }
    // next()
  }

  /** 前台路由 **/
  if (to.path.startsWith('/index')) {
    if (localStorage.getItem(USER_TOKEN)) {
      if (to.path === loginRoutePath) {
        next({ path: '/' })
      } else {
        next()
      }
    } else {
      if (allowList.includes(to.name as string)) {
        // 在免登录名单，直接进入
        next()
      } else {
        next({ path: loginRoutePath, query: { redirect: to.fullPath } })
      }
    }
    // next()
  }

});

router.afterEach((_to) => {
  // 回到顶部
  document.getElementById("html")?.scrollTo(0, 0)
});

export default router;
