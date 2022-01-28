import { defineStore } from 'pinia'

export const useDeckLib = defineStore('decklib', {
  state: () => {
    return {
      decks: [],
      loaded: false,
      pasteBuffer: null,
    }
  },
  actions: {
    initStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send('request-store', 'deck-lib')

        window.ipcRenderer.on('reply-store', (event, key, val) => {
          console.log("Got Store:", key)

          if (key == 'deck-lib' && val) {
            console.log("Load Deck Lib")
            this.decks = JSON.parse(val)
            this.loaded = true
          } else if (key == 'deck-lib') {
            this.loaded = true
          }
        })
      } else {
        
        // Sample data
        this.decks = [
          {
            title: "Bandle Nox",
            date: Date.now() - 10,
            code: 'CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ'
          },
          {
            title: "Draven Sion",
            date: Date.now() - 30000,
            code: 'CECACAIDCQAQIBAQAMCQGAIJBUCACBBGE4WTIAYBAEBS4AIBAQAQCAYDB4CACAQDBEAQGBASAICQGBAGAMAQGCZDGM'
          },
          {
            title: "Thresh Asol",
            date: Date.now() - 12394123,
            code: 'CQBQCBIKV4AQEAIFFA2AKAYJC5KFMXDAAQAQCBIZAECASDIBAUCQ6AQDBFEVOAYBAQCTQAQDBERTGAYBAUAQ6HI'
          }
        ]

        this.loaded = true
      }
    },
    addDeckLibPaste( deckCode ) {
      this.pasteBuffer = deckCode
    }
  },
})