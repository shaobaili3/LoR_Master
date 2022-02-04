import { defineStore } from "pinia"

import { REGION_ID, REGION_SHORTS, REGION_NAMES } from "../components/panels/PanelLeaderboard.vue"

const requestLeaderboardWaitTime = 1000 // ms

import { useBaseStore } from "./StoreBase"
import axios from "axios"

export const useLeaderboardStore = defineStore("leaderboard", {
  state: () => {
    return {
      request: null,
      leaderboard: [],
      lastLeaderboardRequestTime: null,
      isLeaderboardLoading: false,
    }
  },
  actions: {
    cancelLeaderboard() {
      if (this.request) this.request.cancel()
    },
    fetchLeaderboard(regionID) {
      const baseStore = useBaseStore()

      this.lastLeaderboardRequestTime = Date.now()
      this.isLeaderboardLoading = true

      var region = REGION_NAMES[regionID]

      if (!region) return // if region is undefined

      if (this.request) this.cancelLeaderboard()
      const axiosSource = axios.CancelToken.source()
      this.request = { cancel: axiosSource.cancel, msg: "Loading..." }

      var api_link = `${baseStore.API_WEB}/leaderboard/${region}`

      axios
        .get(api_link, { cancelToken: axiosSource.token })
        .then((res) => {
          // this.rawPlayers = res.data;
          this.isLeaderboardLoading = false
          this.leaderboard[regionID] = res.data
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)
            var elapsedTime = Date.now() - this.lastLeaderboardRequestTime // ms
            if (elapsedTime > requestLeaderboardWaitTime) {
              setTimeout(() => {
                this.fetchLeaderboard(regionID)
              }, 100)
            } else {
              setTimeout(() => {
                this.fetchLeaderboard(regionID)
              }, requestLeaderboardWaitTime - elapsedTime)
            }
          }
        })
    },
  },
})
