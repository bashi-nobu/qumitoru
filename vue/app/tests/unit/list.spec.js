import { shallowMount } from '@vue/test-utils'
import List from '@/views/List.vue'
import Vue from "vue"
import Vuetify from "vuetify";

Vue.use(Vuetify);

const $session = {
  start: function(){ return true },
  has: function(){ return true },
  get: function(){ return 1 },
}

describe('List.vue', () => {
  it('集計結果一覧画面が表示される', () => {
    const wrapper = shallowMount(List, {
      mocks: {
        $session
      }
    })
    expect(wrapper.isVueInstance).toBeTruthy()
    expect(wrapper.find('.scoreDataListFrame').exists()).toBeTruthy()
  })
})
