import { createApp } from 'vue'
import { createStore } from 'vuex'

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

createApp(App).use(router).use(store).mount('#app')