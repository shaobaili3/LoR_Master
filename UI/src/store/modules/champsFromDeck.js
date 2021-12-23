export default {
  state () {
      return {
        _champsFromDeck: {},
      }
  },
  getters: {
      champsFromDeck: (state) => state._champsFromDeck
  },
  mutations: {
      pushChampsFromDeck (state, newChampsFromDeck) {
          state._champsFromDeck[newChampsFromDeck.deckCode] = newChampsFromDeck.champs
      }
  },
  actions: {
      addChampsFromDeck( { commit }, { champs, deckCode } ) {
          commit('pushChampsFromDeck', Object.freeze({ deckCode: deckCode, champs: champs }))
      }
  } 
}