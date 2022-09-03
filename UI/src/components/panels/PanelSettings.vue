<template>
  <div class="flex h-full justify-center">
    <div class="w-0 max-w-xl flex-1">
      <div class="flex h-full flex-col px-2 sm:px-0">
        <div class="pb-3 pt-1 text-left text-3xl sm:pt-0 sm:pb-5">{{ $t("str.settings") }}</div>
        <div class="settings-list">
          <div class="settings-list-item" v-if="IS_ELECTRON">
            <div class="settings-title">
              {{ $t("settings.options.autoLaunch") }}
              {{ autoLaunch ? $t("settings.enabled") : $t("settings.disabled") }}
            </div>
            <button class="settings-btn" v-if="autoLaunch" @click="setAutoLaunch(false)">
              {{ $t("settings.disable") }}
            </button>
            <button class="settings-btn" v-if="!autoLaunch" @click="setAutoLaunch(true)">
              {{ $t("settings.enable") }}
            </button>
          </div>
          <div class="settings-list-item">
            <locale-changer
              :title="$t('str.languages')"
              :options="$i18n.availableLocales"
              :optionDefault="$i18n.locale"
              :input="changeMainUILocale"
            ></locale-changer>
          </div>
          <div class="settings-list-item">
            <locale-changer
              :title="$t('settings.options.cardLanguage')"
              :swapNames="cardLocaleNames"
              :options="cardLocales"
              :optionDefault="locale"
              :input="changeCardLocale"
            ></locale-changer>
          </div>
          <div class="settings-list-item" v-if="IS_ELECTRON">
            <div class="settings-title">
              {{ $t("settings.options.resetTrackerBounds") }}
            </div>
            <button class="settings-btn" @click="resetTrackerWindow">
              {{ $t("settings.reset") }}
            </button>
          </div>
        </div>
        <div class="pt-10 text-gray-300">LMT v{{ currentVersion }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import LocaleChanger from "../base/LocaleChanger.vue"
import { locales as cardLocales, localeNames as cardLocaleNames } from "../../pages/template"

import { useBaseStore } from "../../store/StoreBase"
import { mapActions, mapWritableState } from "pinia"

const currentVersion = require("../../../package.json").version

export default {
  components: {
    LocaleChanger,
  },
  data() {
    return {
      cardLocales: cardLocales,
      cardLocaleNames: cardLocaleNames,
      // Options
      autoLaunch: null,
      debugInfos: "",
      currentVersion,
    }
  },
  computed: {
    ...mapWritableState(useBaseStore, ["portNum"]),
  },
  mounted() {
    try {
      if (!this.IS_ELECTRON) {
        return
      }
      this.initLocalSettings()
    } catch (err) {
      console.log(err)
    }
  },
  methods: {
    ...mapActions(useBaseStore, ["changeLocale"]),

    changeMainUILocale(newLocale) {
      console.log("Changing locale")
      this.$i18n.locale = newLocale
      if (window.ipcRenderer) {
        window.ipcRenderer.send("changed-locale", newLocale)
      } else {
        window.localStorage.setItem("lmt-settings-ui-locale", newLocale)
      }
    },
    changeCardLocale(newLocale) {
      console.log("Change Card Locale to:", newLocale)
      this.changeLocale(newLocale)
      if (window.ipcRenderer) {
        window.ipcRenderer.send("changed-card-locale", newLocale)
      }
      if (!this.IS_ELECTRON) {
        window.localStorage.setItem("lmt-settings-card-locale", newLocale)
      }
    },

    // Local Settings
    initLocalSettings() {
      window.ipcRenderer.on("check-auto-launch-return", (event, isEnabled) => {
        this.autoLaunch = isEnabled
      })

      window.ipcRenderer.on("debug-info-display", (event, info) => {
        console.log(info)
        this.debugInfos = info
      })

      window.ipcRenderer.on("return-port", (event, port) => {
        console.log("New Port:", port)
        // this.portNum = port
        // this.$store.commit('setPortNum', port)
        this.portNum = port
      })

      window.ipcRenderer.send("get-port")

      this.checkAutoLaunch()
    },

    checkAutoLaunch() {
      window.ipcRenderer.send("check-auto-launch")
    },
    setAutoLaunch(enable) {
      window.ipcRenderer.send("set-auto-launch", enable)
    },

    resetTrackerWindow() {
      if (this.IS_ELECTRON) {
        window.ipcRenderer.send("reset-deck-window-bounds")
      }
    },
  },
}
</script>

<style scoped>
.title {
  font-size: 32px;
  text-align: left;
  padding: 10px 0px 20px 0px;
}
</style>
