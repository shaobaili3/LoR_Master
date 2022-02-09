import { createApp } from "vue"
import { createI18n } from "vue-i18n"

import App from "./Info.vue"
import "@/assets/css/global.css"

import { useBaseStore } from "../../store/StoreBase"
import { createPinia, mapState, mapActions } from "pinia"

const messages = require("@/assets/data/messages.js")

const i18n = createI18n({
  locale: "English", // set locale
  fallbackLocale: "English", // set fallback locale
  messages,
})

const app = createApp(App)

app.use(i18n)
app.use(createPinia())

app.mixin({
  computed: {
    ...mapState(useBaseStore, ["locale", "IS_ELECTRON"]),
  },
  methods: {
    ...mapActions(useBaseStore, ["changeLocale"]),
  },
})

app.mount("#app")
