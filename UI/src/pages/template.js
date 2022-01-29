import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import '@/assets/css/global.css'

import sets_en from '../../../Resource/en_us.json'
import { createPinia, mapState, mapActions } from 'pinia'

import { useBaseStore } from '../store/StoreBase'

// concat to get rid of first layer array
// reduce to convert array to key-value pair
const sets_en_combined = [].concat(...sets_en)

import messages from '@/assets/data/messages.js'

export const locales = ['de_de', 'en_us', 'es_es', 'es_mx', 'fr_fr', 'it_it', 'ja_jp', 'ko_kr', 'pl_pl', 'pt_br', 'th_th', 'tr_tr', 'ru_ru', 'zh_tw']
export const localeNames = ['German', 'English', 'Spanish (Spain)', 'Spanish (Mexico)', 'French', 'Italian',  'Japanese', 'Korean', 'Polish', 'Portuguese', 'Thai', 'Turkish', 'Russian', 'Chinese']

import mitt from 'mitt'

import metaData from '../store/modules/metaData'
import leaderboardData from '../store/modules/leaderboardData'
import deckLibData from '../store/modules/deckLibData'

const API_WEB_BASE = process.env.VUE_APP_LMT_SERVER == "test" ? "https://lmttest.herokuapp.com" : "https://lormaster.herokuapp.com"

export default (App) => {

locales.forEach(lo => {
    window[lo] = () => import('../../../Resource/'+lo+'.json')
});

// const store = createStore({
//     modules: {
//         metaData,
//         leaderboardData,
//         deckLibData
//     },
//     state () {
//         return {
//             locale: 'en_us',
//             portNum: '26531',
//             API_WEB: API_WEB_BASE,
//             sets_en: sets_en_combined.reduce((a, v) => ({ ...a, [v.cardCode]: v}), {}) , // convert from array to key-value pair
//             sets: sets_en_combined,
//             IS_ELECTRON: window.ipcRenderer !== undefined,
//             IS_DEV: process.env.NODE_ENV === 'development',
//         }
//     },
//     getters: {
//         apiBase( state ) {
//             if (state.IS_ELECTRON) {
//                 return `http://127.0.0.1:${state.portNum}`
//             }
//             return API_WEB_BASE
//             // return 'https://85pj77.deta.dev'
//         },
//     },
//     mutations: {
//         setLocale (state, newLocale) {
//             state.locale = newLocale
//         },
//         loadSets (state, newSets) {
//             state.sets = newSets
//         },
//         setPortNum (state, newPort) {
//             state.portNum = newPort
//         }
//     },
//     actions: {
//         changeLocale ({ dispatch, commit }, newLocale) {
//             commit('setLocale',newLocale)
//             dispatch('loadSetsJson', newLocale)
//         },
//         async loadSetsJson({ commit }, locale) {
//             console.log("Computing Sets", locale)
//             var loadModule

//             if (!locales.includes(locale)) {
//                 console.log("Invalid locale, default to en_us")
//                 loadModule = await window['en_us']()
//             } else {
//                 loadModule = await window[locale]()
//             }

//             commit('loadSets', [].concat(...loadModule.default))
//             // console.log(this.sets)
//         },
//     }
    
// })

const i18n = createI18n({
    locale: 'English', // set locale
    fallbackLocale: 'English', // set fallback locale
    messages,
})

const app = createApp(App)

const emitter = mitt()
app.config.globalProperties.$emitter = emitter
app.use(i18n)
// app.use(store)
app.use(createPinia())

app.mixin({
    computed: {
        ...mapState(useBaseStore, [
            'locale',
            'portNum',
            'sets',
            'sets_en',
            'API_WEB',
            'IS_ELECTRON',
            'IS_DEV',
            'apiBase'
        ]),
    },
    methods: {
        // ...mapMutations([
        //     'changeLocale'
        // ]),
        sendUserEvent(eventInfo) {
            if (window.ipcRenderer) {
                window.ipcRenderer.send('user-event', eventInfo)
            }
        },
        sendUserEventFormat(eventCategory, eventAction, eventLabel, eventValue) {
            if (window.ipcRenderer) {
                window.ipcRenderer.send('user-event', {
                    category: eventCategory,
                    action: eventAction,
                    label: eventLabel,
                    value: eventValue,
                })
            }
        }

    }
})

return app

}

import "tailwindcss/tailwind.css"