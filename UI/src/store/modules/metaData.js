const API = 'https://lormaster.herokuapp.com/meta'

export default {
  namespaced: true,
  state () {
    return {
      metaGroups: null
    }
  },
  getters: {
  },
  mutations: {
    setMetaGroups (state, newMetaGroups) {
      state.metaGroups = newMetaGroups
    }
  },
  actions: {
    fetchMetaGroups ( { commit } ) {

      console.log("Start fetching meta group info")

      var promise = new Promise(resolve => setTimeout(resolve, 1000))
      
      return promise.then((e) => {
        console.log("Retrieved meta data")
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
  }
}