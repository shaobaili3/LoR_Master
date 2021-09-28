import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'

import App from './PageInfo.vue'
import '@/assets/css/global.css'

const messages = require('../../assets/data/messages.js')

const i18n = createI18n({
    locale: 'English', // set locale
    fallbackLocale: 'English', // set fallback locale
    messages,
})

createApp(App).use(i18n).mount('#app')