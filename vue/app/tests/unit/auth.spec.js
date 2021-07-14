import { mount, shallowMount } from '@vue/test-utils'
import Auth from '@/views/Auth.vue'
import Vue from "vue"
import Vuetify from "vuetify";
import flushPromises from "flush-promises";
import axios from 'axios'

Vue.use(Vuetify);

jest.mock('axios')

const response = {
  data: {
      token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJ2BHvKzLlC0",
      userid: 1,
      username: "admin"
  },
  status: 200,
  statusText: "OK"
}
axios.post.mockImplementation((url) => {
  return Promise.resolve(response)
})


describe('Auth.vue', () => {
  const wrapper = shallowMount(Auth)
  it('is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })

  it('ログインフォームが表示されている', () => {
    expect(wrapper.find('.login-card').exists()).toBeTruthy()
    expect(wrapper.find('.login-form').exists()).toBeTruthy()
  })
})

describe('Auth.vue check validation patarn', () => {
  let vuetify;

  it('ユーザー名が五文字以下の場合はヴァリデーションメッセージが表示される', async() => {
    const wrapper = mount(Auth, { vuetify });
    wrapper.find('input[type="text"]').setValue("abc")
    await flushPromises();
    expect(wrapper.findAll('.v-messages__message').at(0).exists()).toBeTruthy()
    expect(wrapper.findAll('.v-messages__message').at(0).text()).toBe('ユーザー名は5文字以上でなければなりません')
  })

  it('パスワードが五文字以下の場合はヴァリデーションメッセージが表示される', async() => {
    const wrapper = mount(Auth, { vuetify });
    wrapper.find('input[type="password"]').setValue("abc")
    await flushPromises();
    expect(wrapper.findAll('.v-messages__message').at(0).exists()).toBeTruthy()
    expect(wrapper.findAll('.v-messages__message').at(0).text()).toBe('パスワードは5文字以上でなければなりません')
  })

  it('ユーザー名&パスワードが未入力の場合はヴァリデーションメッセージが表示される', async() => {
    const wrapper = mount(Auth, { vuetify });
    wrapper.find('button').trigger('click')
    await flushPromises();
    expect(wrapper.findAll('.v-messages__message').at(0).text()).toBe('ユーザー名は必須です')
    expect(wrapper.findAll('.v-messages__message').at(1).text()).toBe('パスワードは必須です')
  })
})

describe("Auth.vue check login and logout method", () => {
  let vuetify

  test("何も入力されずにログインボタンを押してもイベントはトリガーしない", async() => {
    const wrapper = mount(Auth, { vuetify });

    wrapper.find('button').trigger('click')
    await flushPromises();

    expect(wrapper.vm.valid).toBeFalshy;
  });

  test("有効なユーザー名・パスワードを入力後にログインボタンを押すと＄sessionにユーザー情報が保存される", async() => {
    const wrapper = mount(Auth, { vuetify, sync: false });

    wrapper.find("input[type='text']").setValue('dummy_username');
    wrapper.find("input[type='password']").setValue('dummy_password');
    wrapper.find('.login-btn').trigger('click')
    expect(wrapper.vm.loading).toBe(true)
    await flushPromises()
    expect(wrapper.vm.$session.get('token')).toBe(response.data.token);
    expect(wrapper.vm.$session.get('username')).toBe(response.data.username);
    expect(wrapper.vm.$session.get('userid')).toBe(response.data.userid);
  });

  test("ユーザー名・パスワードを入力後にログインボタンを押すと円形プログレスバーが表示される", async() => {
    const wrapper = mount(Auth, { vuetify, sync: false });

    wrapper.find("input[type='text']").setValue('dummy_username');
    wrapper.find("input[type='password']").setValue('dummy_password');
    wrapper.find('.login-btn').trigger('click')
    expect(wrapper.vm.loading).toBe(true)
  });

});
