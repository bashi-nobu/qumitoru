module.exports = {
  webdriver: {
    start_process: true,
    // port: 9515
  },
  test_settings: {
    default: {
      silent: true,
      launch_url: 'http://localhost:8081'
    },
    chrome: {
      desiredCapabilities: {
        browserName: 'chrome',
        javascriptEnabled: true,
        acceptSslCerts: true,
        host: "localhost",
        port: 8081,
        loggingPrefs: { 'browser': 'ALL' },
        chromeOptions: {
          args: [
            '--use-fake-ui-for-media-stream',
            '--use-fake-device-for-media-stream',
            '--headless',
            '--no-sandbox',
            '--disable-gpu',
            '-ignore-certificate-errors',
            'window-size=1280,800',
            '--verbose'
          ],
          w3c: false
        }
      }
    },
    develop: {
      // "launch_url" : "http://dev.example.com",
      "desiredCapabilities": {
      }
    },
    production: {
      // "launch_url" : "http://wwww.example.com",
      "desiredCapabilities": {
      }
    }
  }
};
