const API = 'https://lormaster.herokuapp.com/meta'

const requestWaitTime = 1000 // ms
import axios from 'axios'

export default {
  namespaced: true,
  state () {
    return {
      request: null,
      metaGroups: null,
      lastRequestTime: null,
      isLoading: false,
    }
  },
  getters: {
  },
  mutations: {
    setMetaGroups (state, newMetaGroups) {
      state.metaGroups = newMetaGroups
    },
    setLastRequestTime(state, time) {
      state.lastRequestTime = time
    },
    setIsLoading(state, isLoading) {
      state.isLoading = isLoading
    }
  },
  actions: {
    cancelRequest({ state }) {
      state.request.cancel();
    },
    fetchMetaGroups ( { commit } ) {

      console.log("Start fetching meta group info")

      var promise = new Promise(resolve => setTimeout(resolve, 1000))
      commit('setIsLoading', true)
      
      return promise.then((e) => {
        console.log("Retrieved meta data")
        commit('setIsLoading', false)
        var newMetaGroups = [{
          id: "faction_Demacia_Name faction_MtTargon_Name Pantheon Taric",
          code: "CICQCAQBAIAQGBQIAECAMCQBAUDACCACAYFRIIBBEIWTUPABAEBAMJQBAIBAMAQS",
          playNum: 6643,
          playRate: 0.05443029677334776,
          winRate: 0.5355580754900373,
          decks: [{
            code: "CICQCAQBAIAQGBQIAECAMCQBAUDACCACAYFRIIBBEIWTUPABAEBAMJQBAIBAMAQS",
            playNum: 1114,
            playRate: 0.2602803738317757,
            winRate: 0.5359066427289049,
          },
          {
            code: "CICQCAQBAIAQGBQIAECAMCQBAUDACCACAYFRIIBBEIWTUPABAEBAMJQBAIBAMAQS",
            playNum: 200,
            playRate: 0.2602803738317757,
            winRate: 0.759066427289049,
          }],
        },
        {
          id: "faction_Demacia_Name faction_MtTargon_Name Pantheon Taric",
          code: "CQBQCAQGFYBAKBQCAUDAKCQEAUNCQMJSAIBAKCUXAG6ACAQFAYBQWAYBAIDCUAIFBIFAGBIGAQDAU",
          playNum: 500,
          playRate: 0.05443029677334776,
          winRate: 0.52,
          decks: [{
            code: "CQBQCAQGFYBAKBQCAUDAKCQEAUNCQMJSAIBAKCUXAG6ACAQFAYBQWAYBAIDCUAIFBIFAGBIGAQDAU",
            playNum: 200,
            playRate: 0.2602803738317757,
            winRate: 0.6,
          }],
        }
      ]

        commit('setMetaGroups', newMetaGroups)
      })

      // return fetch(API).then((response) => response.json()).then((data) => {
      //   console.log(Array.isArray(data))
      // }).catch((err) => console.log(err))
    }

    // fetchMetaGroups({ commit, state, rootGetters, dispatch }) {
    //   commit('setLastRequestTime', Date.now())
    //   commit('setIsLoading', true)

    //   if (state.request) dispatch('cancelRequest');
    //   const axiosSource = axios.CancelToken.source();
    //   state.request = { cancel: axiosSource.cancel, msg: "Loading..." };

    //   var api_link = `${rootGetters.apiBase}/meta`;

    //   axios
    //     .get(api_link, { cancelToken: axiosSource.token })
    //     .then((res) => {
    //       // this.rawPlayers = res.data;
    //       commit('setIsLoading', false)
    //       var newMetaGroups = [
    //         {
    //           id: "faction_Demacia_Name faction_MtTargon_Name Pantheon Taric",
    //           code: "CICQCAQBAIAQGBQIAECAMCQBAUDACCACAYFRIIBBEIWTUPABAEBAMJQBAIBAMAQS",
    //           playNum: 6643,
    //           playRate: 0.05443029677334776,
    //           winRate: 0.5355580754900373,
    //           decks: [{
    //             code: "CICQCAQBAIAQGBQIAECAMCQBAUDACCACAYFRIIBBEIWTUPABAEBAMJQBAIBAMAQS",
    //             playNum: 1114,
    //             playRate: 0.2602803738317757,
    //             winRate: 0.5359066427289049,
    //           },
    //           {
    //             code: "CICQCAQBAIAQGBQIAECAMCQBAUDACCACAYFRIIBBEIWTUPABAEBAMJQBAIBAMAQS",
    //             playNum: 200,
    //             playRate: 0.2602803738317757,
    //             winRate: 0.759066427289049,
    //           }],
    //         },
    //         {
    //           id: "faction_Demacia_Name faction_MtTargon_Name Pantheon Taric",
    //           code: "CQBQCAQGFYBAKBQCAUDAKCQEAUNCQMJSAIBAKCUXAG6ACAQFAYBQWAYBAIDCUAIFBIFAGBIGAQDAU",
    //           playNum: 500,
    //           playRate: 0.05443029677334776,
    //           winRate: 0.52,
    //           decks: [{
    //             code: "CQBQCAQGFYBAKBQCAUDAKCQEAUNCQMJSAIBAKCUXAG6ACAQFAYBQWAYBAIDCUAIFBIFAGBIGAQDAU",
    //             playNum: 200,
    //             playRate: 0.2602803738317757,
    //             winRate: 0.6,
    //           }],
    //         }
    //       ]
    //       commit('setMetaGroups', newMetaGroups)
    //     })
    //     .catch((e) => {
    //       if (axios.isCancel(e)) {
    //         console.log("Request cancelled");
    //       } else {
    //         console.log("error", e);
    //         var elapsedTime = Date.now() - state.lastRequestTime; // ms
    //         if (elapsedTime > requestWaitTime) {
    //           setTimeout(() => {
    //             dispatch('fetchMetaGroups')
    //           }, 100);
    //         } else {
    //           setTimeout(() => {
    //             dispatch('fetchMetaGroups')
    //           }, requestWaitTime - elapsedTime)
    //         }
    //       }
    //     });
    // },
  }
}