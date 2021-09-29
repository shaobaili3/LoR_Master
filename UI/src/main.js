import { createApp } from 'vue'
import { createStore } from 'vuex'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import router from './router/'
import '@/assets/css/global.css'

const store = createStore({
  state () {
      return {
          activeRegion: 0,
          players: [],
      }
  },
  mutations: {
    storePlayers (state, payload) {
      state.players[payload.id] = payload.obj;
    },
    changeRegion (state, newRegion) {
        state.activeRegion = newRegion
    }
  }
})

const messages = require('./assets/data/messages.js')

const i18n = createI18n({
  locale: 'English', // set locale
  fallbackLocale: 'English', // set fallback locale
  messages,
})

createApp(App).use(i18n).use(router).use(store).mount('#app')