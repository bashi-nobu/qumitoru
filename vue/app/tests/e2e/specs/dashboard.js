module.exports = {
  beforeEach: (browser) => browser.init(),
  '集計期間を変更することで表示スコアが切り替わる': (browser) => {
    browser
      .url(browser.launch_url)
      .waitForElementVisible('body', 2000)
      // ログイン
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(1000)
      .saveScreenshot('./screenshots/screenshot_dashboard0.png')
      .useXpath()
      .assert.containsText('(//div[contains(@class, "mainTitle")])[1]', '平均スコア')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[1]', '6.5')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[2]', '3.5')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[3]', '3.5')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[4]', '3.5')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[5]', '3.17')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[6]', '3.17')
      .assert.containsText('(//div[contains(@class, "mainTitle")])[2]', 'スコア推移')
      .click('//div[contains(@class, "date-picker-field")]')
      .pause(1000)
      .click('//button[contains(@aria-label, "Previous")]')
      .pause(1000)
      .click('//div[contains(@class, "v-date-picker-table--date")]/table/tbody/tr[2]/td[1]/button')
      .pause(5000)
      .saveScreenshot('./screenshots/screenshot_dashboard.png')
      .assert.containsText('(//div[contains(@class, "mainTitle")])[1]', '平均スコア')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[1]', '9.5')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[2]', '4.5')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[3]', '3.8')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[4]', '3.9')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[5]', '3.27')
      .assert.containsText('//div[contains(@class, "ave-score-frame")]/div[6]', '3.81')
      .end();
  }
};
