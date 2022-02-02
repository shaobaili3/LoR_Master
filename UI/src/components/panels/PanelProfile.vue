<template>
  <div class="flex justify-center h-full">
    <div class="max-w-xl flex-1 w-0">
      <div class="flex flex-col h-full px-2 sm:px-0">
        <div class="text-3xl" v-if="localHistoryLoading">{{ $t("str.loading") }}</div>
        <PlayerMatches v-if="!localHistoryLoading" :playerName="name" :playerRegion="server" :playerTag="tag" :matches="playerMatches"></PlayerMatches>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useBaseStore } from "../../store/StoreBase"
import { useStatusStore } from "../../store/StoreStatus"
import PlayerMatches from "../match/PlayerMatches.vue"

import axios from "axios"

import { ref, onMounted } from "vue"

const store = useStatusStore()
const baseStore = useBaseStore()

const regionShort = {
  americas: "NA",
  europe: "EU",
  asia: "APAC",
  sea: "APAC",
}

let localCancleToken,
  localHistoryLoading = ref(false)

let server = regionShort[store.localServer]
let name = null,
  tag = null
if (store.localPlayerID) {
  let nameTag = store.localPlayerID.split("#")
  if (nameTag.length == 2) {
    name = nameTag[0]
    tag = nameTag[1]
  }
}

let playerMatches = ref([]),
  rank = ref(0),
  lp = ref(0)

onMounted(() => {
  requestLocalHistory()
})

function requestLocalHistory() {
  // console.log("Request Local History")

  if (localHistoryLoading.value) {
    // Don't do anything if there is already a local search request
    return
  }

  // Now ready for a new request
  //Check if there are any previous pending requests
  if (typeof localCancleToken != typeof undefined) {
    localCancleToken.cancel("Operation canceled due to new request.")
  }

  //Save the cancel token for the current request
  localCancleToken = axios.CancelToken.source()

  var server = store.localServer
  var name = null,
    tag = null
  if (store.localPlayerID) {
    let nameTag = store.localPlayerID.split("#")
    if (nameTag.length == 2) {
      name = nameTag[0]
      tag = nameTag[1]
    }
  }

  if (!(server && name && tag)) {
    // Checks to see if there is all the information
    // Don't do anything if not enough data
    return
  }

  // server = "americas"
  // name = "FlyingFish"
  // tag = "1111"

  let apiLink = `${baseStore.API_WEB}/search/${server}/${name}/${tag}`

  console.log("Request Local History", apiLink)
  localHistoryLoading.value = true

  sendUserEvent({
    category: "Main Window Requests",
    action: "Request Local History",
    label: "URL: " + apiLink,
    value: null,
  })

  const requestLocalHistoryStartTime = Date.now()

  axios
    .get(apiLink, { cancelToken: localCancleToken.token }) // Pass the cancel token
    .then((response) => {
      localHistoryLoading.value = false

      if (response.data == "Error") {
        console.log("Local History Search Error")
      } else {
        sendUserEvent({
          category: "Main Window Requests",
          action: "Got Local History Result [Success]",
          label: "URL: " + apiLink,
          value: Date.now() - requestLocalHistoryStartTime,
        })

        processLocalHistory(response.data)

      }
    })
    .catch((e) => {
      if (axios.isCancel(e)) {
        console.log("Request cancelled")
      } else {
        console.log("error", e)
        localHistoryLoading.value = false
        sendUserEvent({
          category: "Main Window Requests",
          action: "Got Local History Result [Fail]",
          label: "URL: " + apiLink,
          value: Date.now() - requestLocalHistoryStartTime,
        })
      }
    })
}
function processHistory(data, playerName, playerServer) {
  // console.log(data)

  var matchInfo = {
    matches: [],
    rank: null,
    lp: null,
  }

  if (!data) return matchInfo

  // Processing for normal Data
  for (var key in data) {
    var match = data[key]
    if (!match) continue // Skip if null history

    var isFirstPlayer = match.player_info[0].name.toLowerCase() == playerName.toLowerCase()
    var player, playerGame, opponent, opponentGame
    var info = match.info
    var details = null

    if (match.local && match.local.deck_tracker) {
      details = {
        openHand: match.local.deck_tracker.openHand,
        replacedHand: match.local.deck_tracker.replacedHand,
        timeline: match.local.deck_tracker.timeline,
        startTime: match.local.startTime,
        endTime: match.local.endTime,
      }
    }

    var opponentName, opponentRank, opponentLp, opponentTag, opponentDeck, deck, rounds, win, time, order

    if (isFirstPlayer) {
      playerGame = info.players[0]
      opponentGame = info.players[1]

      player = match.player_info[0]
      opponent = match.player_info[1]
    } else {
      playerGame = info.players[1]
      opponentGame = info.players[0]

      player = match.player_info[1]
      opponent = match.player_info[0]
    }

    if (!playerGame || !opponentGame || !player || !opponent) continue

    opponentName = opponent.name

    if (opponent.rank && opponent.rank !== "") {
      opponentRank = (opponent.rank + 1).toString() // rank starts from 0
    } else {
      opponentRank = "" // ranks can be empty
    }

    opponentLp = opponent.lp
    opponentTag = opponent.tag

    if (!matchInfo.rank && player.rank !== "") {
      matchInfo.rank = player.rank + 1 // player.rank starts from 0
    }

    if (!matchInfo.lp) matchInfo.lp = player.lp

    deck = playerGame.deck_code
    opponentDeck = opponentGame.deck_code
    order = playerGame.order_of_play
    win = playerGame.game_outcome == "win"
    rounds = info.total_turn_count
    var badges = []
    if (info.game_mode)
      badges.push(
        info.game_mode
          .replace(/([A-Z])/g, " $1")
          .trim()
          .replace("Lobby", "")
      )
    if (info.game_type)
      badges.push(
        info.game_type
          .replace(/([A-Z])/g, " $1")
          .trim()
          .replace("Lobby", "")
      )

    time = info.game_start_time_utc

    matchInfo.matches.push({
      opponentName: opponentName,
      deck: deck,
      region: regionShort[playerServer],
      opponentDeck: opponentDeck,
      opponentRank: opponentRank,
      opponentLp: opponentLp,
      opponentTag: opponentTag,
      rounds: rounds,
      win: win,
      time: time,
      badges: badges,
      details: details,
    })
  }

  return matchInfo
}
function processLocalHistory(data) {
  var info = processHistory(data, name, server)
  playerMatches.value = info.matches
  rank.value = info.rank
  lp.value = info.lp
}

function sendUserEvent(eventInfo) {
  if (window.ipcRenderer) {
    window.ipcRenderer.send("user-event", eventInfo)
  }
}
</script>
