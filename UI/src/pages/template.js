import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import '@/assets/css/global.css'

import { createStore, mapState, mapMutations } from 'vuex'

export default (App) => {

const locales = ['de_de', 'en_us', 'es_es', 'es_mx', 'fr_fr', 'it_it', 'ja_jp', 'ko_kr', 'pl_pl', 'pt_br', 'th_th', 'tr_tr', 'ru_ru', 'zh_tw']

locales.forEach(lo => {
    window[lo] = () => import('../../../Resource/'+lo+'.json')
});

const store = createStore({
    state () {
        return {
            locale: 'en_us',
            sets: import('../../../Resource/en_us.json')
        }
    },
    mutations: {
        setLocale (state, newLocale) {
            state.locale = newLocale
        },
        loadSets (state, newSets) {
            state.sets = newSets
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
    }
    
})

const messages = require('@/assets/data/messages.js')

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
            'sets'
        ])
    },
    // methods: {
    //   ...mapMutations([
    //     'changeLocale'
    //   ]),
    // }
})

app.mount('#app')
}
