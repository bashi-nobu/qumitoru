module.exports = {
  beforeEach: (browser) => browser.init(),
  'ページネーションの挙動': (browser) => {
    browser
      .url(browser.launch_url)
      // ログイン
      .useCss()
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(3000)
      // アップロード画面へ移動
      .click('a[href="/list"]')
      // 1秒待つ
      .pause(1000)
      .useXpath()
      .assert.elementCount('.v-data-table__wrapper table tbody tr', 10)
      .click('//button[contains(@aria-label, "Next page")]')
      .assert.elementCount('.v-data-table__wrapper table tbody tr', 1)
      .end();
  },
  '集計期間を変更することによる一覧表示の切り替え': (browser) => {
    browser
      .url(browser.launch_url)
      // ログイン
      .useCss()
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(3000)
      // 集計一覧画面へ移動
      .click('a[href="/list"]')
      // 1秒待つ
      .pause(1000)
      .useXpath()
      .assert.elementCount('.v-data-table__wrapper table tbody tr', 10)
      .click('//div[contains(@class, "date-picker-field")]')
      .pause(1000)
      .click('//div[contains(@class, "v-date-picker-header")]/button[contains(@aria-label, "Previous")]')
      .pause(1000)
      .click('//div[contains(@class, "v-date-picker-table--date")]/table/tbody/tr[2]/td[1]/button')
      .pause(5000)
      .assert.elementCount('.v-data-table__wrapper table tbody tr', 2)
      .end();
  },
  'アンケートを編集する': (browser) => {
    browser
      .url(browser.launch_url)
      .useCss()
      // ログイン
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(1000)
      // 集計結果一覧画面へ移動
      .click('a[href="/list"]')
      .waitForElementVisible('.score-data-list', 1000)
      // 1秒待つ
      .pause(1000)
      .click('.editBtn')
      .assert.containsText('.img-frame__title', '読み込んだアンケート')
      .click('.editStartBtn')
      .click('.v-select__slot')
      .useXpath()
      .click('//div[contains(@role, "listbox")]/div[6]')
      .click('//button[contains(@class, "submitBtn")]')
      .assert.containsText('//span[contains(@class, "updateResult")]', '更新が完了しました。')
      .end();
  }
};

// npm run test:e2e tests/e2e/specs/list.js
