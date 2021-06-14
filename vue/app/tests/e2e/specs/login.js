
module.exports = {
  beforeEach: (browser) => browser.init(),
  '無効なユーザー名・パスワードでログインする': (browser) => {
    browser
      .url(browser.launch_url)
      .waitForElementVisible('body', 1000)
      // ログインフォームが表示されているかどうか確認
      .assert.visible('.login-form')
      // ユーザー名・パスワードの入力欄が表示されているかどうか確認
      .assert.visible('input[type=text]')
      .assert.visible('input[type=password]')
      // 無効なユーザー名・パスワードを入力
      .setValue('input[type=text]', 'invaliduser')
      .setValue('input[type=password]', 'invalidpassword')
      .click('button[type="button"]')
      .pause(1000)
      .assert.containsText('#swal2-title', 'エラー')
      .assert.containsText('.swal2-html-container', 'ユーザー名もしくはパスワード、または両方が間違っています')
      .end();
  },
  '有効なユーザー名・パスワードでログインする&ログアウトする': (browser) => {
    browser
      .url(browser.launch_url)
      .waitForElementVisible('body', 1000)
      // ログインフォームが表示されているかどうか確認
      .assert.visible('.login-form')

      // ユーザー名・パスワードの入力欄が表示されているかどうか確認
      .assert.visible('input[type=text]')
      .assert.visible('input[type=password]')

      // 有効なユーザー名・パスワードを入力
      .setValue('input[type=text]', 'validuser')
      .setValue('input[type=password]', 'validpassword')
      .click('button[type="button"]')

      // 1秒待つ
      .pause(2000)
      // ログインに成功すると「ダッシュボード」が表示される
      .assert.visible('.dashboard-frame')

      // サイドメニューのログアウトボタンをクリックするとログイン画面へ遷移する
      .click('.logoutBtn')
      .waitForElementVisible('body', 1000)
      // ログインフォームが表示されているかどうか確認
      .assert.visible('.login-form')
      .end();
  },
};
