<template>
  <player-matches
    @search="searchPlayer($event)"
    :playerName="localPlayerInfo.name"
    :playerRegion="localPlayerInfo.server"
    :playerRank="localPlayerInfo.rank"
    :playerLP="localPlayerInfo.lp"
    :playerTag="localPlayerInfo.tag"
    :matches="localMatches"
  >
  </player-matches>
</template>

<script>
export default {
  data() {
    return {
      localMatches: [],
      localPlayerInfo: {}, // playerId, server, language, rank, lp
      localHistoryLoading: false,
      localHistoryWaiting: false,
    }
  },
  methods: {
    searchPlayer() {
      console.log("Should now search player")
    },
    requestLocalHistory() {
      console.log("Request Local History")

      if (this.localHistoryLoading) {
        // Don't do anything if there is already a local search request
        return
      }

      //Check if there are any previous pending requests
      if (typeof localCancleToken != typeof undefined) {
        localCancleToken.cancel("Operation canceled due to new request.")
      }

      //Save the cancel token for the current request
      localCancleToken = axios.CancelToken.source()

      var { server, name, tag } = this.localPlayerInfo

      if (!(server && name && tag)) {
        // Checks to see if there is all the information
        // Don't do anything if not enough data
        return
      }

      let apiLink
      if (server === "sea") {
        apiLink = `${this.apiBase}/local`
      } else {
        apiLink = `${this.API_WEB}/search/${server}/${name}/${tag}`
      }

      console.log("Request Local History", apiLink)
      this.localHistoryLoading = true

      this.sendUserEvent({
        category: "Main Window Requests",
        action: "Request Local History",
        label: "URL: " + apiLink,
        value: null,
      })

      const requestLocalHistoryStartTime = Date.now()

      axios
        .get(apiLink, { cancelToken: localCancleToken.token }) // Pass the cancel token
        .then((response) => {
          this.localHistoryLoading = false

          if (response.data == "Error") {
            console.log("Local History Search Error")
          } else {
            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Got Local History Result [Success]",
              label: "URL: " + apiLink,
              value: Date.now() - requestLocalHistoryStartTime,
            })

            if (server === "sea") {
              let key = (name + "#" + tag).toLowerCase()
              // console.log('Current key', key)
              this.processLocalHistory(response.data[key])
            } else {
              this.processLocalHistory(response.data)
            }
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)
            this.localHistoryLoading = false
            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Got Local History Result [Fail]",
              label: "URL: " + apiLink,
              value: Date.now() - requestLocalHistoryStartTime,
            })
          }
        })
    },
  },
}
</script>
