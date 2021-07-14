module.exports = {
  beforeEach: (browser) => browser.init(),
  '無効なファイルをアップロードする': (browser) => {
    browser
      .url(browser.launch_url)
      .waitForElementVisible('body', 1000)
      // ログイン
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(1000)
      // アップロード画面へ移動
      .click('a[href="/upload"]')
      .waitForElementVisible('.upload-form', 1000)
      .setValue('input[type="file"]', require('path').resolve(__dirname + '/files/invalid_upload_file.jpg'))
      // 1秒待つ
      .pause(1000)
      .assert.containsText('#swal2-title', '読み取り失敗')
      .end();
  },
  '有効なファイルをアップロードする': (browser) => {
    browser
      .url(browser.launch_url)
      .waitForElementVisible('body', 1000)
      // ログイン
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(1000)
      // アップロード画面へ移動
      .click('a[href="/upload"]')
      .waitForElementVisible('.upload-form', 1000)
      .setValue('input[type="file"]', require('path').resolve(__dirname + '/files/valid_upload_file.jpg'))
      // 1秒待つ
      .pause(4000)
      .assert.containsText('#swal2-title', '読み取り成功')
      .end();
  },
  'アップロード済みのアンケート枚数が反映されている': (browser) => {
    browser
      .url(browser.launch_url)
      .waitForElementVisible('body', 1000)
      // ログイン
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(1000)
      // アップロード画面へ移動
      .click('a[href="/upload"]')
      .waitForElementVisible('.upload-form', 1000)
      // 1秒待つ
      .pause(4000)
      .assert.containsText('.uploadStatus', '現在1枚のアンケートがアップロードされています')
      .end();
  },
  'アンケートの集計開始ボタンをクリックすると集計を開始しましたと表示される': (browser) => {
    browser
      .url(browser.launch_url)
      .waitForElementVisible('body', 1000)
      // ログイン
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')
      // 1秒待つ
      .pause(1000)
      // アップロード画面へ移動
      .click('a[href="/upload"]')
      .waitForElementVisible('.upload-form', 1000)
      // 1秒待つ
      .pause(4000)
      .click('.startAggregateBtn')
      .pause(1000)
      .click('.startAggregateConfirmBtn')
      .pause(1000)
      .assert.containsText('#swal2-title', '集計を開始しました')
      .end();
  }
};
