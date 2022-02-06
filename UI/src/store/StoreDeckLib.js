import DeckEncoder from "../modules/runeterra/DeckEncoder"
import { defineStore } from "pinia"

import { useBaseStore } from "./StoreBase"

export const useDeckLibStore = defineStore("deckLib", {
  state: () => {
    return {
      decks: [],
      loaded: false,
      pasteBuffer: null,
      error: null,
    }
  },
  actions: {
    initStore() {
      console.log("Init Store")
      if (window.ipcRenderer) {
        if (this.loaded) return
        this.loaded = true // Assume that the loading will never fail?
        return new Promise((resolve) => {
          window.ipcRenderer.send("request-store", "deck-lib")

          window.ipcRenderer.on("reply-store", (event, key, val) => {
            console.log("Got Store:", key)

            if (key == "deck-lib" && val) {
              console.log("Load Deck Lib")
              this.decks = JSON.parse(val)
            } else if (key == "deck-lib") {
              // this.loaded = true
            }
            resolve("resolved")
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

        this.decks = decks
        this.loaded = true
      }
    },
    updateStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send("save-store", "deck-lib", JSON.stringify(this.decks, null, "\t"))
      }
    },
    processPaste(deckCode) {
      console.log("Process Paste")

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
          console.log(newTitle)
        }
        this.decks.unshift({
          title: newTitle,
          date: new Date(),
          code: deckCode,
        })
        this.updateStore()
      } catch (error) {
        // console.log(error)
        this.error = error
        setTimeout(() => {
          this.error = null
        }, 2000)
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
