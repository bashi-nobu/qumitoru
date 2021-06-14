module.exports = {
  setupFiles: ["./tests/unit/setup.js"],
  "moduleFileExtensions": [
    "js",
    "json",
    "vue"
  ],
  "transformIgnorePatterns": [
      "node_modules/(?!vue-awesome|vuex-i18n|vue-sweetalert2)"
  ],
  "transform": {
      ".*\\.(vue)$": "<rootDir>/node_modules/vue-jest",
      "^.+\\.js$": "<rootDir>/node_modules/babel-jest"
  },
  "moduleNameMapper": {
      "^@/(.*)$": "<rootDir>/src/$1"
  }
};
