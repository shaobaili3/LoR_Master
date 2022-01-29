import App from './Home.vue'

import template from '../template'

import { createRouter, createWebHistory } from 'vue-router'

const app = template(App)

import routes from '../../router/mainRouter'
const router = createRouter({
  history: createWebHistory(),
  routes, // short for `routes: routes`
})

app.use(router)

app.mount('#app')