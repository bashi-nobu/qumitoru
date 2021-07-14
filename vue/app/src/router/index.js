import Vue from 'vue'
import VueRouter from 'vue-router'
import Auth from '@/views/Auth'
import Dashboard from '@/views/Dashboard'
import Upload from '@/views/Upload'
import List from '@/views/List'
import Download from '@/views/Download'
import Howto from '@/views/Howto'

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
  {
    path: '/list',
    name: 'List',
    component: List,
    meta: { title: "集計結果一覧 | qumitoru" }
  },
  {
    path: '/download',
    name: 'Download',
    component: Download,
    meta: { title: "ダウンロード | qumitoru" },
  },
  {
    path: '/howto',
    name: 'Howto',
    component: Howto,
    meta: { title: "使い方 | qumitoru"},
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
