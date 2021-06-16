import Vue from 'vue'
import VueRouter from 'vue-router'
import Auth from '@/views/Auth'
import Dashboard from '@/views/Dashboard'
import Upload from '@/views/Upload'

Vue.use(VueRouter)

const routes = [
  {
    path: '/auth',
    name: 'Auth',
    component: Auth,
    meta: { title: "ログイン | qumitoru" }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: "ダッシュボード | qumitoru" },
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload,
    meta: { title: "アンケートアップロード | qumitoru" },
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
