import { shallowMount, createLocalVue } from '@vue/test-utils'
import App from '@/App.vue'
import Sidebar from '@/components/sidebar.vue'


import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(VueRouter)
const routes = [
  {
    path: '/',
    component: App
  }
]
const router = new VueRouter({
  routes
})

describe('App.vue', () => {
  it('is a Vue instance', () => {
    const wrapper = shallowMount(App, { localVue, router })
    expect(wrapper.isVueInstance).toBeTruthy()
  })
})

describe('App.vue', () => {
  it('has Sidebar component', () => {
    const wrapper = shallowMount(App, { localVue, router })
    const sidebar = wrapper.findComponent(Sidebar)
    expect(sidebar.is(Sidebar)).toBe(true)
  })
})

describe('App.vue', () => {
  it('未ログイン時はサイドバーは表示されない', () => {
    const wrapper = shallowMount(App, {
      localVue,
      router,
      data(){
        return {
          isLogin: false,
        }
      }
    })
    const sidebar = wrapper.find('#sidebar');
    expect(sidebar.isVisible()).toBe(false)
  })

  it('ログイン時はサイドバーが表示される', async() => {
    const $session = {
      start: function(){ return true },
      has: function(){ return true }
    }
    const wrapper = shallowMount(App, {
      localVue,
      router,
      mocks: {
        $session
      }
    })
    const sidebar = wrapper.find('#sidebar');
    expect(wrapper.vm.isLogin).toBe(true);
    await wrapper.vm.$nextTick() // wait rendering update
    expect(sidebar.isVisible()).toBe(true)
  })
})
