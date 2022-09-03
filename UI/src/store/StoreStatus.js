import { defineStore } from "pinia"
import { useBaseStore } from "./StoreBase"

const requestStatusWaitTime = 1000 //ms
import axios from "axios"
export const useStatusStore = defineStore("status", {
  state: () => {
    return {
      lastStatusRequestTime: 0,

      lorRunning: false,
      localApiEnabled: false,
      localServer: null,
      localPlayerID: null,

      backendRunning: true,
    }
  },
  actions: {
    initAnalytics(uid) {
      if (window.ipcRenderer) {
        window.ipcRenderer.send("user-init", uid)
      }
    },
    processStatusInfo(data) {
      const baseStore = useBaseStore()

      this.backendRunning = true

      // if (data.language) {
      //   // Card language
      //   var newLocale = data.language.replace("-", "_").toLowerCase()
      //   if (baseStore.locale != newLocale) {
      //     console.log("Switch Card Locale", this.locale, newLocale)
      //     baseStore.changeLocale(newLocale)
      //   }
      // }

      this.lorRunning = data.lorRunning
      if (!data.lorRunning) {
        this.localApiEnabled = null
        this.localServer = null
        this.localPlayerID = null
      } else {
        this.localApiEnabled = data.isLocalApiEnable
        this.localServer = data.server

        if (data.playerId && data.playerId != "" && this.localPlayerID != data.playerId) {
          // there is a new valid player ID
          this.initAnalytics(data.playerId)
        }
        this.localPlayerID = data.playerId
      }
    },
    requestStatusInfo() {
      // Keeps requesting status
      const baseStore = useBaseStore()

      if (!baseStore.IS_ELECTRON) {
        // Skip for Web app
        return
      }

      this.lastStatusRequestTime = Date.now()
      axios
        .get(`${baseStore.apiBase}/status`)
        .then((response) => {
          this.processStatusInfo(response.data)
          var elapsedTime = Date.now() - this.lastStatusRequestTime // ms
          if (requestStatusWaitTime > elapsedTime) {
            setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime)
          } else {
            setTimeout(this.requestStatusInfo, 100)
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            this.backendRunning = false
            this.lorRunning = null
            console.log("error", e)
            var elapsedTime = Date.now() - this.lastStatusRequestTime // ms
            if (elapsedTime > requestStatusWaitTime) {
              setTimeout(this.requestStatusInfo, 100)
            } else {
              setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime)
            }
          }
        })
    },
    restartBackend() {
      if (window.ipcRenderer && !this.backendRunning) {
        window.ipcRenderer.send("backend-restart")
      }
    },
  },
})
