module.exports = {
  beforeEach: (browser) => browser.init(),
  'スマホでは「集計一覧」「ダウンロード」は非表示': (browser) => {
    browser
      .resizeWindow(600, 700)
      .url(browser.launch_url)
      // ログイン
      .useCss()
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 3秒待つ
      .pause(3000)
      // アップロード画面へ移動
      .url(browser.launch_url+'/list')
      // 1秒待つ
      .pause(1000)
      .assert.not.containsText('.sidemenu', '集計一覧')
      .assert.not.containsText('.sidemenu', 'ダウンロード')
      .end();
  }
};
