import { shallowMount } from '@vue/test-utils'
import Dashboard from '@/views/Dashboard.vue'
import Vue from "vue"
import Vuetify from "vuetify";
import flushPromises from "flush-promises";
import axios from 'axios'

Vue.use(Vuetify);

jest.mock('axios')

const response = {
  data:
    {
      "categoryAveList": [6.5, 3.5, 3.6, 3.7, 3.17, 3.18],
      "dailyScoreData": [
          [
              ["take_at", "総合評価"],
              ["05-30", 5.88],
              ["05-31", 6.88],
              ["06-01", 6.63],
              ["06-02", 5.63],
              ["06-03", 8.13],
              ["06-04", 4.75]
          ],
          [
              ["take_at", "料理"],
              ["05-30", 3.5],
              ["05-31", 3.25],
              ["06-01", 3.5],
              ["06-02", 3.0],
              ["06-03", 4.0],
              ["06-04", 2.5]
          ],
          [
              ["take_at", "接客"],
              ["05-30", 3.0],
              ["05-31", 4.0],
              ["06-01", 3.75],
              ["06-02", 3.0],
              ["06-03", 3.75],
              ["06-04", 3.0]
          ],
          [
              ["take_at", "清潔感"],
              ["05-30", 3.75],
              ["05-31", 3.0],
              ["06-01", 3.5],
              ["06-02", 3.25],
              ["06-03", 3.75],
              ["06-04", 2.25]
          ],
          [
              ["take_at", "雰囲気"],
              ["05-30", 3.0],
              ["05-31", 3.0],
              ["06-01", 3.5],
              ["06-02", 2.75],
              ["06-03", 3.5],
              ["06-04", 2.5]
          ],
          [
              ["take_at", "コスパ"],
              ["05-30", 2.75],
              ["05-31", 3.0],
              ["06-01", 3.25],
              ["06-02", 3.0],
              ["06-03", 3.5],
              ["06-04", 2.75]
          ],
          [
              ["take_at", "take_at"],
              ["05-30", "05-30"],
              ["05-31", "05-31"],
              ["06-01", "06-01"],
              ["06-02", "06-02"],
              ["06-03", "06-03"],
              ["06-04", "06-04"]
          ]
      ]
    }
}
axios.get.mockImplementation((url) => {
  return Promise.resolve(response)
})


describe('Dashboard.vue', () => {

  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('ダッシュボード画面が表示される', () => {
    const wrapper = shallowMount(Dashboard, vuetify, { sync: false });
    expect(wrapper.isVueInstance).toBeTruthy()
    expect(wrapper.find('.dashboard-frame').exists()).toBeTruthy()
  })

  it('スコアが表示される', async() => {
    const wrapper = shallowMount(Dashboard, vuetify, { sync: false });
    await flushPromises();
    expect(wrapper.find('.ave-score-frame').exists()).toBeTruthy()
    expect(wrapper.findAll('scorebox-stub').at(0).attributes().categoryscore).toBe('6.5')
    expect(wrapper.findAll('scorebox-stub').at(1).attributes().categoryscore).toBe('3.5')
    expect(wrapper.findAll('scorebox-stub').at(2).attributes().categoryscore).toBe('3.6')
    expect(wrapper.findAll('scorebox-stub').at(3).attributes().categoryscore).toBe('3.7')
    expect(wrapper.findAll('scorebox-stub').at(4).attributes().categoryscore).toBe('3.17')
    expect(wrapper.findAll('scorebox-stub').at(5).attributes().categoryscore).toBe('3.18')
  })

  it('チャートが表示される', async() => {
    const wrapper = shallowMount(Dashboard, vuetify, { sync: false });
    await flushPromises();
    expect(wrapper.find('.line-chart-frame').exists()).toBeTruthy()
  })
})
