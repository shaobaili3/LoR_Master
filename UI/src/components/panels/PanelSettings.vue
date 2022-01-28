<template>
  <div class="title">{{ $t("str.settings") }}</div>
  <div class="settings-list">
    <div class="settings-list-item" v-if="IS_ELECTRON">
      <div class="settings-title">{{ $t("settings.options.autoLaunch") }} {{ autoLaunch ? $t("settings.enabled") : $t("settings.disabled") }}</div>
      <button class="settings-btn" v-if="autoLaunch" @click="setAutoLaunch(false)">{{ $t("settings.disable") }}</button>
      <button class="settings-btn" v-if="!autoLaunch" @click="setAutoLaunch(true)">{{ $t("settings.enable") }}</button>
    </div>
    <div class="settings-list-item">
      <locale-changer :title="$t('str.languages')" :options="$i18n.availableLocales" :optionDefault="$i18n.locale" :input="changeMainUILocale"></locale-changer>
    </div>
    <div class="settings-list-item" v-if="!IS_ELECTRON">
      <locale-changer :title="$t('settings.options.cardLanguage')" :swapNames="cardLocaleNames" :options="cardLocales" :optionDefault="locale" :input="changeCardLocale"></locale-changer>
    </div>
    <div class="settings-list-item" v-if="IS_ELECTRON">
      <div class="settings-title">{{ $t("settings.options.resetTrackerBounds") }}</div>
      <button class="settings-btn" @click="resetTrackerWindow">{{ $t("settings.reset") }}</button>
    </div>
  </div>

  <!-- <div class="debug-info">
        {{debugInfos}}
      </div> -->
</template>

<script>
import LocaleChanger from '../base/LocaleChanger.vue'
import { locales as cardLocales, localeNames as cardLocaleNames} from '../../pages/template'
import { mapActions } from 'vuex'

export default {
  components: {
    LocaleChanger
  },
  data() {
    return {
      cardLocales: cardLocales,
      cardLocaleNames: cardLocaleNames,
      // Options
      autoLaunch: null,
      debugInfos: "",
    }
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
    ...mapActions([
      'changeLocale'
    ]),

    changeMainUILocale(newLocale) {
      console.log("Changing locale")
      this.$i18n.locale = newLocale
      if (window.ipcRenderer) {
        window.ipcRenderer.send('changed-locale', newLocale)
      } else {
        window.localStorage.setItem('ui-locale', newLocale)
      }
    },
    changeCardLocale(newLocale) {
      console.log("Change Card Locale to:", newLocale)
      this.changeLocale(newLocale)
      if (!this.IS_ELECTRON) {
        window.localStorage.setItem('card-locale', newLocale)
      }
    },

    // Local Settings
    initLocalSettings() {
      window.ipcRenderer.on('check-auto-launch-return', (event, isEnabled) => {
        this.autoLaunch = isEnabled
      })

      window.ipcRenderer.on('debug-info-display', (event, info) => {
        console.log(info)
        this.debugInfos = info
      })

      window.ipcRenderer.on('return-port', (event, port) => {
        console.log("New Port:", port)
        // this.portNum = port
        this.$store.commit('setPortNum', port)
      })

      window.ipcRenderer.send("get-port")

      this.checkAutoLaunch()
    },

    checkAutoLaunch() {
      window.ipcRenderer.send("check-auto-launch")
    },
    setAutoLaunch(enable) {
      window.ipcRenderer.send('set-auto-launch', enable)
    },

    resetTrackerWindow() {
      if (this.IS_ELECTRON) {
        window.ipcRenderer.send('reset-deck-window-bounds')
      }
    },
  }
}
</script>