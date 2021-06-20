import { shallowMount } from '@vue/test-utils'
import Download from '@/views/Download.vue'
import Vue from "vue"
import Vuetify from "vuetify";

Vue.use(Vuetify);

const $session = {
  start: function(){ return true },
  has: function(){ return true },
  get: function(){ return 1 },
}

describe('Download.vue', () => {
  it('ダウンロード画面が表示される', () => {
    const wrapper = shallowMount(Download, {
      mocks: {
        $session
      }
    })
    expect(wrapper.isVueInstance).toBeTruthy()
    expect(wrapper.find('.downloadFrame').exists()).toBeTruthy()
  })
})
