import DeckEncoder from "../modules/runeterra/DeckEncoder"
import { defineStore } from "pinia"

const storeid = "bookmark"

// Player object should contain, name, tag, and preferrably region

export const useBookmarkStore = defineStore(storeid, {
  state: () => {
    return {
      bookmarks: [],
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

              this.bookmarks = JSON.parse(val)
              if (this.bookmarks == null) this.bookmarks = []
              this.loaded = true
            }

            resolve("resolved")
          })
        })
      } else {
        // Browser
        this.bookmarks = JSON.parse(window.localStorage.getItem(`lmt-settings-${storeid}`))
        if (this.bookmarks == null) this.bookmarks = []
        this.loaded = true
      }
    },
    updateStore() {
      if (window.ipcRenderer) {
        // Electron
        window.ipcRenderer.send("save-store", storeid, JSON.stringify(this.bookmarks, null, "\t"))
      } else {
        // Browser
        window.localStorage.setItem(`lmt-settings-${storeid}`, JSON.stringify(this.bookmarks))
      }
    },
    async addBookmark(newBookmark) {
      if (!this.loaded) {
        await this.initStore()
      }
      this.bookmarks.push(newBookmark)
      this.updateStore()
    },
    async deleteBookmark(id) {
      if (!this.loaded) {
        await this.initStore()
      }
      this.bookmarks.splice(id, 1)
      this.updateStore()
    },
    async clearBookmarks() {
      if (!this.loaded) {
        await this.initStore()
      }
      this.bookmarks.splice(0, this.bookmarks.length)
      this.updateStore()
    },
  },
})
