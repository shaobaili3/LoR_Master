import DeckEncoder from "../../modules/runeterra/DeckEncoder"

export default {
  namespaced: true,
  state: () => {
    return {
      decks: [],
      loaded: false,
      pasteBuffer: null,
      error: null,
    }
  },
  mutations: {
    setLoaded(state, loaded) {
      state.loaded = loaded
    },
    setDecks(state, newDecks) {
      state.decks = newDecks
    },
    addToFront(state, newItem) {
      state.decks.unshift(newItem)
    },
    removeAtIndex(state, index) {
      state.decks.splice(index, 1)
    },
    setError(state, newErr) {
      state.error = newErr
    },
  },
  actions: {
    initStore({ commit, state, rootState, dispatch }) {
      console.log("Init Store")
      if (window.ipcRenderer) {
        if (state.loaded) return;
        commit("setLoaded", true)
        return new Promise((resolve) => {
          window.ipcRenderer.send("request-store", "deck-lib")

          window.ipcRenderer.on("reply-store", (event, key, val) => {
            console.log("Got Store:", key)

            if (key == "deck-lib" && val) {
              console.log("Load Deck Lib")
              commit("setDecks", JSON.parse(val))
            } else if (key == "deck-lib") {
              // commit("setLoaded", true)
            }
            resolve('resolved');
          })
        })
      } else {
        // Sample data
        var decks = [
          {
            title: "Bandle Nox",
            date: Date.now() - 10,
            code: "CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ",
          },
          {
            title: "Draven Sion",
            date: Date.now() - 30000,
            code: "CECACAIDCQAQIBAQAMCQGAIJBUCACBBGE4WTIAYBAEBS4AIBAQAQCAYDB4CACAQDBEAQGBASAICQGBAGAMAQGCZDGM",
          },
          {
            title: "Thresh Asol",
            date: Date.now() - 12394123,
            code: "CQBQCBIKV4AQEAIFFA2AKAYJC5KFMXDAAQAQCBIZAECASDIBAUCQ6AQDBFEVOAYBAQCTQAQDBERTGAYBAUAQ6HI",
          },
        ]

        commit("setDecks", decks)
      }
    },
    updateStore({ commit, state, rootState, dispatch }) {
      if (window.ipcRenderer) {
        window.ipcRenderer.send("save-store", "deck-lib", JSON.stringify(state.decks, null, "\t"))
      }
    },
    processPaste({ commit, state, rootState, dispatch }, deckCode) {
      console.log("Process Paste")

      try {
        let deck = DeckEncoder.decode(deckCode)
        let champNames = deck.reduce((names, card) => {
          let info = rootState.sets.find((info) => info.cardCode == card.code)
          if (info.rarityRef === "Champion") {
            names.push(info.name)
          }
          return names
        }, [])
        let i = 0
        let newTitle = champNames.join(" ")
        while (state.decks.findIndex((item) => item.title == newTitle) != -1 && i < 1000) {
          i += 1
          newTitle = `#${i} ` + champNames.join(" ")
          console.log(newTitle)
        }
        commit("addToFront", {
          title: newTitle,
          date: new Date(),
          code: deckCode,
        })
        dispatch("updateStore")
      } catch (error) {
        // console.log(error)
        commit("setError", error)
        setTimeout(() => {
          commit("setError", null)
        }, 2000)
      }
    },
    async deckLibPaste({ commit, state, rootState, dispatch }, deckCode) {
      if (!state.loaded) {
        await dispatch("initStore")
      }
      dispatch("processPaste", deckCode)
    },
    handleDelete({ commit, state, rootState, dispatch }, id) {
      commit("removeAtIndex", id)
      dispatch("updateStore")
    },
  },
}
