
import { defineStore } from "pinia"

const storeid = "player-info"

// Player object should contain, name, tag, and preferrably region

export const usePlayerInfoStore = defineStore(storeid, {
  state: () => {
    return {
      playerInfo: null,
      loaded: false,
    }
  },
  actions: {
    initStore() {
      if (this.loaded) return
      console.log(`Init '${storeid}' Store`)
      if (window.ipcRenderer) {
        // Electron
        return new Promise((resolve) => {
          window.ipcRenderer.send("request-store", storeid) // bookmark
          window.ipcRenderer.on(`reply-store-${storeid}`, (_event, val) => {
            if (val) {
              console.log("Loaded Bookmarks")

              this.playerInfo = JSON.parse(val)
              if (this.playerInfo == null) this.playerInfo = null
              this.loaded = true
            }

            resolve("resolved")
          })
        })
      } else {
        // Browser
        this.playerInfo = JSON.parse(window.localStorage.getItem(`lmt-settings-${storeid}`))
        if (this.playerInfo == null) this.playerInfo = null
        this.loaded = true
      }
    },
    updateStore() {
      console.log("Update Player Store")
      if (window.ipcRenderer) {
        // Electron
        window.ipcRenderer.send("save-store", storeid, JSON.stringify(this.playerInfo, null, "\t"))
      } else {
        // Browser
        window.localStorage.setItem(`lmt-settings-${storeid}`, JSON.stringify(this.playerInfo))
      }
    },
    async changePlayerInfo(newPlayerInfo) {
      console.log("Change Player Info")
      if (!this.loaded) {
        await this.initStore()
      }
      this.playerInfo = newPlayerInfo
      this.updateStore()
    },
    async deletePlayerInfo() {
      console.log("Delete Player Info")
      if (!this.loaded) {
        await this.initStore()
      }
      this.playerInfo = null
      this.updateStore()
    },
  },
})
