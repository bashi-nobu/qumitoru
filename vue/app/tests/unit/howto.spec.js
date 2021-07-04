import { shallowMount } from '@vue/test-utils'
import Howto from '@/views/Howto.vue'
import Vue from "vue"
import Vuetify from "vuetify";

Vue.use(Vuetify);

const $session = {
  start: function(){ return true },
  has: function(){ return true },
  get: function(){ return 1 },
}

describe('Howto.vue', () => {
  it('使い方画面が表示される', () => {
    const wrapper = shallowMount(Howto, {
      mocks: {
        $session
      }
    })
    expect(wrapper.isVueInstance).toBeTruthy()
    expect(wrapper.find('.howtoFrame').exists()).toBeTruthy()
  })
})
