module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ["plugin:vue/vue3-essential", "eslint:recommended"],
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "babel-eslint",
  },
  rules: {
    // "no-unused-vars": "off",
    "vue/multi-word-component-names": "off",
    "no-unused-vars": "off",
  },
}
