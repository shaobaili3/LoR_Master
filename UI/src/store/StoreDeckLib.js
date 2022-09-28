import DeckEncoder from "../modules/runeterra/DeckEncoder"
import { defineStore } from "pinia"

import { useBaseStore } from "./StoreBase"

const storeid = "deckLib"

export const useDeckLibStore = defineStore(storeid, {
  state: () => {
    return {
      decks: [],
      loaded: false,
      error: null,
    }
  },
  actions: {
    initStore() {
      if (this.loaded) {
        return
      }
      if (window.ipcRenderer) {
        this.loaded = true // Assume that the loading will never fail?
        return new Promise((resolve) => {
          window.ipcRenderer.on("reply-store-deck-lib", (_event, val) => {
            if (val) {
              this.decks = JSON.parse(val)
            }
            resolve("resolved")
          })
          window.ipcRenderer.send("request-store", "deck-lib")
        })
      } else {
        // Sample data
        this.decks = JSON.parse(window.localStorage.getItem(`lmt-settings-${storeid}`))
        if (this.decks == null) this.decks = []
        this.loaded = true
      }
    },
    setErrorFading(error) {
      this.error = error
      setTimeout(() => {
        this.error = null
      }, 2000)
    },
    updateStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send("save-store", "deck-lib", JSON.stringify(this.decks, null, "\t"))
      } else {
        window.localStorage.setItem(`lmt-settings-${storeid}`, JSON.stringify(this.decks))
      }
    },
    processPaste(deckCode) {
      console.log("Process Paste")

      console.log(this.decks)
      console.log(this.decks.findIndex((item) => item.code == deckCode))

      if (this.decks.findIndex((item) => item.code == deckCode) != -1) {
        this.setErrorFading("Exact Deck Already Exists")
        return
      }

      try {
        let deck = DeckEncoder.decode(deckCode)
        let champNames = deck.reduce((names, card) => {
          const baseStore = useBaseStore()
          let info = baseStore.sets.find((info) => info.cardCode == card.code)
          if (info.rarityRef === "Champion") {
            names.push(info.name)
          }
          return names
        }, [])
        let i = 0
        let newTitle = champNames.join(" ")
        while (this.decks.findIndex((item) => item.title == newTitle) != -1 && i < 1000) {
          i += 1
          newTitle = `#${i} ` + champNames.join(" ")
        }
        this.decks.unshift({
          title: newTitle,
          date: new Date(),
          code: deckCode,
        })
        this.updateStore()
      } catch (error) {
        // console.log(error)
        this.setErrorFading(error)
      }
    },
    async deckLibPaste(deckCode) {
      if (!this.loaded) {
        await this.initStore()
      }
      this.processPaste(deckCode)
      return true
    },
    handleDelete(id) {
      this.decks.splice(id, 1)
      this.updateStore()
    },
  },
})
