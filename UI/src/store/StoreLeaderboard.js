import { defineStore } from "pinia"

import { REGION_ID, REGION_SHORTS, REGION_NAMES } from "../components/panels/PanelLeaderboard.vue"

const requestLeaderboardWaitTime = 1000 // ms

import { useBaseStore } from "./StoreBase"
import axios from "axios"

export const useLeaderboardStore = defineStore("leaderboard", {
  state: () => {
    return {
      request: [],
      leaderboard: [],
      leaderboardUpdateTime: [],
      lastLeaderboardRequestTime: [],
      leaderboardLoading: [],
    }
  },
  actions: {
    fetchLeaderboard(regionID) {
      const baseStore = useBaseStore()

      var region = REGION_NAMES[regionID]

      if (!region) return // if region is undefined

      if (this.leaderboardLoading[regionID]) return // if leaderboard is already loading

      if (this.request[regionID]) this.request[regionID].cancel()

      this.lastLeaderboardRequestTime[regionID] = Date.now()
      this.leaderboardLoading[regionID] = true

      const axiosSource = axios.CancelToken.source()
      this.request = { cancel: axiosSource.cancel, msg: "Loading..." }

      var api_link = `${baseStore.API_WEB}/rank/${region}`

      axios
        .get(api_link, { cancelToken: axiosSource.token })
        .then((res) => {
          // this.rawPlayers = res.data;
          this.leaderboardLoading[regionID] = false
          this.leaderboard[regionID] = res.data.players
          this.leaderboardUpdateTime[regionID] = res.data.time
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)

            this.leaderboardLoading[regionID] = false

            // var elapsedTime = Date.now() - this.lastLeaderboardRequestTime // ms
            // if (elapsedTime > requestLeaderboardWaitTime) {
            //   setTimeout(() => {
            //     this.fetchLeaderboard(regionID)
            //   }, 100)
            // } else {
            //   setTimeout(() => {
            //     this.fetchLeaderboard(regionID)
            //   }, requestLeaderboardWaitTime - elapsedTime)
            // }
          }
        })
    },
  },
})
