import { shallowMount } from '@vue/test-utils'
import Upload from '@/views/Upload.vue'
import Vue from "vue"
import Vuetify from "vuetify";

Vue.use(Vuetify);

const $session = {
  start: function(){ return true },
  has: function(){ return true },
  get: function(){ return 1 },
}

describe('Upload.vue', () => {

  it('ログインしていない場合はアンケート画像アップロード画面が表示されない', () => {
    const wrapper = shallowMount(Upload)
    expect(wrapper.find('.upload-form').exists()).toBeTruthy()
  })

  it('ログイン済みの場合はアンケート画像のアップロードフォームが表示される', () => {
    const wrapper = shallowMount(Upload, {
      mocks: {
        $session
      }
    })
    expect(wrapper.isVueInstance).toBeTruthy()
    expect(wrapper.find('.upload-form').exists()).toBeTruthy()
  })

  it('uploadFilesCountが0の場合は集計開始ボタンが表示されない', async() => {
    const wrapper = shallowMount(Upload, {
      mocks: {
        $session
      }
    })
    wrapper.setData({
      uploadFilesCount: 0
    })
    expect(wrapper.find('.startCalculateBtn').exists()).toBe(false)
  })

  it('uploadFilesCountが0以上の場合は集計開始ボタンが表示される', async() => {
    const wrapper = shallowMount(Upload, {
      mocks: {
        $session
      }
    })
    wrapper.setData({
      uploadFilesCount: 1
    })
    expect(wrapper.find('.upload-form').exists()).toBeTruthy()
  })

})