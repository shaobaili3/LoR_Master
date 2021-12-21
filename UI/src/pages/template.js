import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import '@/assets/css/global.css'

import { createStore, mapState, mapMutations } from 'vuex'
import sets_en from '../../../Resource/en_us.json'

// concat to get rid of first layer array
// reduce to convert array to key-value pair
const sets_en_combined = [].concat(...sets_en)

import messages from '@/assets/data/messages.js'

export const locales = ['de_de', 'en_us', 'es_es', 'es_mx', 'fr_fr', 'it_it', 'ja_jp', 'ko_kr', 'pl_pl', 'pt_br', 'th_th', 'tr_tr', 'ru_ru', 'zh_tw']
export const localeNames = ['German', 'English', 'Spanish (Spain)', 'Spanish (Mexico)', 'French', 'Italian',  'Japanese', 'Korean', 'Polish', 'Portuguese', 'Thai', 'Turkish', 'Russian', 'Chinese']

export default (App) => {

locales.forEach(lo => {
    window[lo] = () => import('../../../Resource/'+lo+'.json')
});

const store = createStore({
    state () {
        return {
            locale: 'en_us',
            sets: sets_en_combined,
            IS_ELECTRON: window.ipcRenderer !== undefined,
            _champsFromDeck: {},
        }
    },
    getters: {
        champsFromDeck: (state) => state._champsFromDeck
    },
    mutations: {
        setLocale (state, newLocale) {
            state.locale = newLocale
        },
        loadSets (state, newSets) {
            state.sets = newSets
        },
        pushChampsFromDeck (state, newChampsFromDeck) {
            state._champsFromDeck[newChampsFromDeck.deckCode] = newChampsFromDeck.champs
        }
    },
    actions: {
        changeLocale ({ dispatch, commit }, newLocale) {
            commit('setLocale',newLocale)
            dispatch('loadSetsJson', newLocale)
        },
        async loadSetsJson({ commit }, locale) {
            console.log("Computing Sets", locale)
            var loadModule

            if (!locales.includes(locale)) {
                console.log("Invalid locale, default to en_us")
                loadModule = await window['en_us']()
            } else {
                loadModule = await window[locale]()
            }

            commit('loadSets', [].concat(...loadModule.default))
            // console.log(this.sets)
        },
        addChampsFromDeck( { commit }, { champs, deckCode } ) {
            commit('pushChampsFromDeck', { deckCode: deckCode, champs: champs })
        }
    }
    
})

const i18n = createI18n({
    locale: 'English', // set locale
    fallbackLocale: 'English', // set fallback locale
    messages,
})

const app = createApp(App)

app.use(i18n).use(store)

app.mixin({
    computed: {
        ...mapState([
            'locale',
            'sets',
            'IS_ELECTRON',
            'API',
        ])
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

app.mount('#app')
}

import "tailwindcss/tailwind.css"