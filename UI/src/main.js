import { createApp } from 'vue'
import { createStore } from 'vuex'

import App from './App.vue'
import router from './router/'
import '@/assets/css/global.css'

// import firebase from 'firebase/app'
// import 'firebase/performance'

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

// if (firebase.apps.length === 0) {

//     console.log("Init Firebase App")

//     var firebaseConfig = {
//     apiKey: "AIzaSyCxGjwqMuzBJXPWz1ixhpFLpH0Gn-SMIl0",
//     authDomain: "lor-master-leaderboard.firebaseapp.com",
//     databaseURL: "https://lor-master-leaderboard-default-rtdb.firebaseio.com",
//     projectId: "lor-master-leaderboard",
//     storageBucket: "lor-master-leaderboard.appspot.com",
//     messagingSenderId: "659164123299",
//     appId: "1:659164123299:web:88206dcb77fc2d81642f16",
//     measurementId: "G-Q7ZNPR6Y79"
//     };
//     // Initialize Firebase
//     firebase.initializeApp(firebaseConfig);
//     const perf = firebase.performance();
//     console.log(perf)
//     // firebase.analytics();
// }

createApp(App).use(router).use(store).mount('#app')