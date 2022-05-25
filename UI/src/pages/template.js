import { createApp } from "vue"
import { createI18n } from "vue-i18n"

import sets_en from "../data/en_us.json"
import { createPinia, mapState, mapActions } from "pinia"

import { useBaseStore } from "../store/StoreBase"

import VueVirtualScroller from "vue-virtual-scroller"
// import Popper from "vue3-popper"

import TooltipDirective from "../directives/TooltipDirective"

import "vue-virtual-scroller/dist/vue-virtual-scroller.css"
import "@/assets/css/global.css"

// concat to get rid of first layer array
// reduce to convert array to key-value pair
const sets_en_combined = [].concat(...sets_en)

import messages from "@/assets/data/messages.js"

export const locales = [
  "de_de",
  "en_us",
  "es_es",
  "es_mx",
  "fr_fr",
  "it_it",
  "ja_jp",
  "ko_kr",
  "pl_pl",
  "pt_br",
  "th_th",
  "tr_tr",
  "ru_ru",
  "zh_tw",
  "zh_cn",
]
export const localeNames = [
  "Deutsch",
  "English",
  "Español (ES)",
  "Español (LATAM)",
  "Français",
  "Italiano",
  "日本語",
  "한국어",
  "Polski",
  "Português",
  "คำเมือง",
  "Türkçe",
  "Русский язык",
  "繁體中文",
  "简体中文",
]

import mitt from "mitt"

export default (App) => {
  locales.forEach((lo) => {
    window[lo] = () => import("../data/" + lo + ".json")
  })

  const i18n = createI18n({
    locale: "English", // set locale
    fallbackLocale: "English", // set fallback locale
    messages,
  })

  const app = createApp(App)

  const emitter = mitt()
  app.config.globalProperties.$emitter = emitter
  app.use(i18n)
  app.use(createPinia())
  app.use(VueVirtualScroller)

  app.directive("tooltip", TooltipDirective)
  // app.component("Popper", Popper)
  // app.use(FloatingVue, {
  //   themes: {
  //     "card-tooltip": {
  //       $extend: "tooltip",
  //       triggers: ["click"],
  //       boundary: "body",
  //       delay: {
  //         show: 20,
  //         hide: 0,
  //       },
  //     },
  //   },
  // })

  app.mixin({
    computed: {
      ...mapState(useBaseStore, [
        "locale",
        "portNum",
        "sets",
        "sets_en",
        "API_WEB",
        "IS_ELECTRON",
        "IS_DEV",
        "apiBase",
      ]),
    },
    methods: {
      // ...mapMutations([
      //     'changeLocale'
      // ]),
      sendUserEvent(eventInfo) {
        if (window.ipcRenderer) {
          window.ipcRenderer.send("user-event", eventInfo)
        }
      },
      sendUserEventFormat(eventCategory, eventAction, eventLabel, eventValue) {
        if (window.ipcRenderer) {
          window.ipcRenderer.send("user-event", {
            category: eventCategory,
            action: eventAction,
            label: eventLabel,
            value: eventValue,
          })
        }
      },
    },
  })

  return app
}

import "tailwindcss/tailwind.css"
