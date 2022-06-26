import { defineStore } from "pinia"

import sets_en from "../data/en_us.json"

const sets_en_combined = [].concat(...sets_en)
const API_WEB_BASE =
  process.env.VUE_APP_LMT_SERVER == "test"
    ? "https://lormaster.herokuapp.com"
    : "https://lormaster.herokuapp.com"

//https://lormaster.herokuapp.com
//https://lormaster.azurewebsites.net
//https://lmttest.herokuapp.com

import { locales, localeNames } from "../pages/template"

export const useBaseStore = defineStore("base", {
  state: () => {
    return {
      locale: "en_us",
      portNum: "26531",
      API_WEB: API_WEB_BASE,
      sets_en: sets_en_combined.reduce((a, v) => ({ ...a, [v.cardCode]: v }), {}), // convert from array to key-value pair
      sets: sets_en_combined,
      IS_ELECTRON: window.ipcRenderer !== undefined,
      IS_DEV: process.env.NODE_ENV === "development",
    }
  },
  getters: {
    apiBase: (state) => {
      if (state.IS_ELECTRON) {
        return `http://127.0.0.1:${state.portNum}`
      }
      return API_WEB_BASE
      // return 'https://85pj77.deta.dev'
    },
  },
  actions: {
    changeLocale(newLocale) {
      // This is Card locale. For UI locale, change vue i-18n setting
      this.locale = newLocale
      this.loadSetsJson(newLocale)
    },
    async loadSetsJson(locale) {
      console.log("Computing Sets", locale)
      var loadModule

      if (!locales.includes(locale)) {
        console.log("Invalid locale, default to en_us")
        loadModule = await window["en_us"]()
      } else {
        loadModule = await window[locale]()
      }

      this.sets = [].concat(...loadModule.default)
    },
    initPortNum() {
      return new Promise((resolve) => {
        window.ipcRenderer.on("return-port", (event, port) => {
          console.log("New Port:", port)
          this.portNum = port
          resolve("resolved")
        })
        window.ipcRenderer.send("get-port")
      })
    },
  },
})
