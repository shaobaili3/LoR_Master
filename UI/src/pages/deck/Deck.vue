<template>
  <div class="flex h-full max-w-[290px] flex-col pt-[45px] text-white">
    <base-window-controls
      :canClose="false"
      :canShrink="true"
      :playerName="oppoName"
      :playerRank="oppoInfo.rank"
      :playerLP="oppoInfo.lp"
      :titleType="'match'"
    ></base-window-controls>

    <div class="flex h-full flex-col">
      <!-- Loading -->
      <div class="flex w-full justify-center pt-2" v-if="isLoading">
        {{ $t("loading.readyToRock") }}
      </div>

      <!-- Title Tabs -->
      <div class="flex w-full justify-around gap-1 px-1 text-gray-200" v-if="!isLoading">
        <div
          class="flex-1 cursor-pointer rounded-lg bg-gray-700 py-0.5 text-center text-sm hover:bg-gray-500 hover:text-white 2xs:text-base"
          @click="switchTab(TABS.oppo)"
          :class="{ 'bg-gray-500 text-gray-100': this.currentTab == TABS.oppo }"
        >
          <i class="fas fa-telescope"></i>
        </div>
        <div
          class="flex-1 cursor-pointer rounded-lg bg-gray-700 py-0.5 text-center text-sm hover:bg-gray-500 hover:text-white 2xs:text-base"
          @click="switchTab(TABS.my)"
          :class="{ 'bg-gray-500 text-gray-100': this.currentTab == TABS.my }"
        >
          <i class="fas fa-user-cowboy"></i>
        </div>
        <div
          class="flex-1 cursor-pointer rounded-lg bg-gray-700 py-0.5 text-center text-sm hover:bg-gray-500 hover:text-white 2xs:text-base"
          @click="switchTab(TABS.grave)"
          :class="{ 'bg-gray-500 text-gray-100': this.currentTab == TABS.grave }"
        >
          <i class="fas fa-tombstone"></i>
        </div>
      </div>

      <div class="mt-1 h-0 flex-1 overflow-y-auto" ref="scrollContainer">
        <!-- Opponent History -->
        <!-- <div class="px-1 pt-1" v-if="this.currentTab == TABS.oppo && !isLoading">
          <div class="pt-1.5 pb-2 text-center" v-if="matchInfos.length <= 0">
            {{ loadingOppoText }}
          </div>

          <div class="" v-if="matchInfos && matchInfos.length > 0">
            <match-oppo-info
              v-for="(match, index) in matchInfos"
              :key="match.opponentName"
              :opponentName="match.opponentName"
              :rounds="match.rounds"
              :time="match.time"
              :startTime="match.startTime"
              :matches="match.matches"
              :winrate="match.winrate"
              :badges="match.badge"
              :opponentDeck="match.opponentDeck"
              :deck="match.deckCode"
              :total="matchTotalNum"
              :history="match.history"
              :expanded="match.expanded"
              @open="onMatchOppoOpen(index)"
            ></match-oppo-info>
          </div>
        </div> -->

        <!-- Deck Library (Also TABS.oppo) -->
        <div v-if="this.currentTab == TABS.oppo && !isLoading">
          <tracker-deck-lib></tracker-deck-lib>
        </div>

        <!-- Oppo Played -->
        <div v-if="this.currentTab == TABS.grave && !isLoading">
          <div
            class="sticky top-0 z-10 bg-gray-900 py-2 px-2 text-left text-xs text-gray-200 2xs:text-sm"
          >
            <i class="fas fa-axe-battle px-1"></i>
            {{ $t("tracker.tabs.oppoPlayed") }}
          </div>
          <deck-detail
            :deck="oppoGraveCode"
            :baseDeck="oppoGraveCode"
            :showCopy="false"
            :extra="oppoGraveExtraCards"
          ></deck-detail>
        </div>

        <!-- My Played -->
        <div v-if="this.currentTab == TABS.grave && !isLoading">
          <div
            class="sticky top-0 z-10 bg-gray-900 py-2 px-2 pt-4 text-left text-xs text-gray-200 2xs:text-sm"
          >
            <i class="fas fa-sword px-1"></i>
            {{ $t("tracker.tabs.myPlayed") }}
          </div>
          <deck-detail
            :baseDeck="myPlayedCode"
            :showCopy="false"
            :extra="myPlayedExtraCards"
          ></deck-detail>
        </div>

        <!-- My Deck -->
        <div v-if="this.currentTab == TABS.my && !isLoading">
          <!-- <div class="flex h-9 justify-center gap-1 pt-1">
            <deck-regions :deck="startingDeckCode" :fixedWidth="false"></deck-regions>
          </div> -->

          <deck-detail
            :deck="currentDeckCode"
            :baseDeck="startingDeckCode"
            :showCopy="false"
            @card="onCardHover"
          ></deck-detail>
        </div>
      </div>

      <!-- Footer Tabs -->
      <div class=""></div>

      <div class="flex h-8 w-full flex-col justify-center text-base 2xs:h-10" v-if="!isLoading">
        <div class="flex w-full items-center gap-2">
          <div class="w-0 flex-1">
            <div
              class="flex items-center justify-center transition-opacity"
              :class="{ 'opacity-100': showCardProb, 'opacity-0': !showCardProb }"
            >
              <i class="fas fa-dice pr-1.5 text-gray-200"></i>
              <div class="w-5">{{ cardProb }}%</div>
            </div>
          </div>
          <!-- Card Num -->
          <div class="flex w-0 flex-1 items-baseline justify-center text-gray-200">
            <!-- <i class="fas fa-layer-group"></i> -->
            <!-- <i class="fas fa-send-backward"></i> -->
            <!-- <i class="fas fa-archive"></i> -->
            <i class="fas fa-scroll-old"></i>
            <!-- <i class="fas fa-hand-paper"></i> -->
            <!-- <i class="fas fa-copy"></i> -->
            <!-- <div class="relative inline-block h-4 w-6 scale-90">
              <i class="fas fa-rectangle-portrait absolute top-0 left-0"></i>
              <i class="fas fa-rectangle-portrait absolute top-0.5 left-0.5 text-gray-900"></i>
              <i class="far fa-rectangle-portrait absolute top-1 left-1"></i>
            </div> -->
            <span class="pl-2 text-white">{{ cardsInHandNum }}</span
            ><span class="pr-2 text-sm">/10</span>
          </div>
        </div>
        <!-- <div class="footer-text">
          {{ $t("tracker.cardsInHand", { num: cardsInHandNum }) }}
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import BaseWindowControls from "../../components/base/BaseWindowControls.vue"
import DeckDetail from "../../components/deck/DeckDetail.vue"
import DeckEncoder from "../../modules/runeterra/DeckEncoder"
import MatchOppoInfo from "../../components/match/MatchOppoInfo.vue"
import DeckRegions from "../../components/deck/DeckRegions.vue"
import Card from "../../modules/runeterra/Card"

import { useStore, mapActions, mapState } from "pinia"

import "../../assets/scss/tooltips.scss"
import "../../assets/scss/deck.scss"
import "../../assets/scss/transitions.scss"

const testTrackData = require("../../assets/data/testTrack")
// const testTrackData = require('../../assets/data/testTrackLab')
const testStatusData = require("../../assets/data/testStatusEN")
// const testStatusData = require('../../assets/data/testStatus')

import TrackerLayer from "../../components/tracker/TrackerLayer.vue"
import { useLeaderboardStore } from "../../store/StoreLeaderboard"
import { useBaseStore } from "../../store/StoreBase"
import TrackerDeckLib from "../../components/tracker/TrackerDeckLib.vue"

const requestDataWaitTime = 100 // ms
const requestServerWaitTime = 3000 //ms
const requestStatusWaitTime = 1000 //ms

// const portNum = "26531"
// const API_BASE = `http://127.0.0.1:${portNum}`

const REGION_NAMES = ["americas", "europe", "asia", "sea"]

const TABS = {
  oppo: 0,
  my: 1,
  grave: 3,
  decklib: 4,
}

const LAYERS = {
  base: 0,
  decklib: 1,
  deckdetail: 2,
}

const api_error = `${useBaseStore.API_WEB}/error`

var lastTrackTime, lastServerRequestTime, lastStatusRequestTime

export default {
  components: {
    BaseWindowControls,
    // MatchOppoInfo,
    DeckDetail,
    TrackerDeckLib,
  },
  data() {
    return {
      rawDataString: null,
      matchInfos: [],
      request: null,

      deckCode: null,
      titleType: null,
      currentTab: TABS.my,

      LAYERS: LAYERS,
      TABS: TABS,

      tabScrollTops: [],

      cardsInHandNum: null,

      currentDeckCode: null,
      startingDeckCode: null,
      oppoGraveCode: null,
      myPlayedCode: null,
      oppoPinnedId: null,

      startingExtraCards: null,
      myGraveExtraCards: null,
      myPlayedExtraCards: null,
      oppoGraveExtraCards: null,

      oppoName: null,
      oppoRank: null,
      oppoLp: null,

      requestOpponentHistoryError: null,
      isLoadingOpponentHistory: false,

      lorRunning: false,

      currentLayer: 0,

      showCardProb: false,
      cardProb: null,
    }
  },
  computed: {
    ...mapState(useLeaderboardStore, ["leaderboard", "leaderboardLoading"]),
    oppoInfo() {
      if (!this.oppoLeaderboard) {
        return {
          rank: null,
          lp: null,
        }
      }

      return {
        rank: this.oppoLeaderboard.rank,
        lp: this.oppoLeaderboard.lp,
      }
    },
    isLoading() {
      if (this.currentDeckCode || this.startingDeckCode) return false
      if (this.matchInfos.length > 0) return false
      return this.oppoName == null || this.oppoName == "" || this.matchInfos.length == 0
      // return true
    },
    oppoLeaderboard() {
      if (!this.oppoName) return null
      var regionID = REGION_NAMES.indexOf(this.server)
      if (regionID >= 0) {
        console.log("Leaderboard access from deck tracker")
        var lead = this.leaderboard
        // console.log(lead)
        if (lead && lead[regionID]) {
          return lead[regionID].find((val) => {
            return val.name == this.oppoName
          })
        }
      }
      return null
    },
    loadingOppoText() {
      if (this.requestOpponentHistoryError) return this.$t("loading.nohistory")
      if (this.isLoadingOpponentHistory) return this.$t("loading.history")
      return this.$t("loading.nohistory")
    },
    matchTotalNum() {
      // console.log(this.matchInfos);
      return this.matchInfos.reduce((total, item) => total + item.matches, 0)
    },
  },
  mounted() {
    // console.log(JSON.stringify(this.matchInfos))
    // this.getMatchInfo()
    // console.log("Mounted")
    // this.requestData()
    console.log("Page Deck Mounted")
    // console.log(`API BASE: ${this.apiBase}`)

    // this.hideWindow()
    if (this.IS_ELECTRON) {
      this.initPortNum()
      this.initUILocale()

      // The keyboard shortcut test
      window.ipcRenderer.on("request-test-history", (event) => {
        this.requestTestOppoHistory()
      })
    }

    this.requestStatusInfo()
    this.requestTrackInfo()
    // this.requestServerInfo()
  },
  methods: {
    ...mapActions(useBaseStore, ["changeLocale", "initPortNum"]),
    ...mapActions(useLeaderboardStore, ["fetchLeaderboard"]),

    onMatchOppoOpen(index) {
      this.matchInfos[index].expanded = !this.matchInfos[index].expanded
    },

    initUILocale() {
      window.ipcRenderer.send("request-store", "ui-locale")

      window.ipcRenderer.on("reply-store-ui-locale", (_event, val) => {
        // console.log("Got store", key, val);
        if (val && this.$i18n && this.$i18n.locale) {
          this.$i18n.locale = val
          console.log("Change locale to", val)
        }
      })

      // Allow change locale message to be synced across windows
      window.ipcRenderer.on("to-change-locale", (event, newLocale) => {
        this.$i18n.locale = newLocale
        console.log("Changing locale to", newLocale)
      })

      window.ipcRenderer.on("to-change-card-locale", (event, newLocale) => {
        console.log("Changing card locale to", newLocale)
        this.changeLocale(newLocale)
      })
    },
    hideWindow() {
      if (window.hideWindow) {
        window.hideWindow()
      }
    },
    makeWindowVisible() {
      if (window.makeVisible) {
        window.makeVisible()
      }
    },
    switchTab(newTab) {
      if (this.currentTab == newTab) return

      if (this.IS_ELECTRON) {
        this.sendUserEvent({
          category: "Tracker Event",
          action: "Switch Tab",
          label: "From: " + this.currentTab + " | To: " + newTab,
          value: null,
        })
      }

      // Record current scrolltop
      this.tabScrollTops[this.currentTab] = this.$refs.scrollContainer.scrollTop

      this.currentTab = newTab

      setTimeout(() => {
        // this.current tab should be the new tab
        this.$refs.scrollContainer.scrollTo({
          top: this.tabScrollTops[this.currentTab],
          left: 0,
          behavior: "smooth",
        })
      }, 10)
    },
    requestOpponentHistory() {
      // http://192.168.20.4:${portNum}/history/asia/J01/J01

      this.isLoadingOpponentHistory = true
      this.requestOpponentHistoryError = null

      var api = `${this.API_WEB}/history/${this.server}/${this.oppoName}`
      console.log("Request Opponent History, api:", api)

      axios
        .get(api)
        .then((response) => {
          console.log("Opponent Data", response.data)
          this.isLoadingOpponentHistory = false
          this.processOpponentHistory(response.data)
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)
            this.requestOpponentHistoryError = e
          }
        })
    },
    requestTestOppoHistory() {
      const stormHistoryAPI = `${this.API_WEB}/history/americas/storm`
      axios
        .get(stormHistoryAPI)
        .then((response) => {
          console.log("Opponent Data", response.data)
          this.processOpponentHistory(response.data)
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)
          }
        })
    },
    requestStatusInfo() {
      if (!this.IS_ELECTRON) {
        var data = testStatusData
        this.server = data.server
        var regionID = REGION_NAMES.indexOf(this.server)
        if (regionID >= 0) {
          this.fetchLeaderboard(regionID)
        }
        // if (data.language) {
        //   var newLocale = data.language.replace("-", "_").toLowerCase()
        //   if (this.locale != newLocale) {
        //     console.log("Switch Locale", this.locale, newLocale)
        //     this.changeLocale(newLocale)
        //   }
        // }

        return
      }

      // Keeps requesting status
      lastStatusRequestTime = Date.now()
      axios
        .get(`${this.apiBase}/status`) // status
        .then((response) => {
          var elapsedTime = Date.now() - lastStatusRequestTime // ms

          if (response && response.data) {
            var data = response.data
            if (data.server && this.server != data.server) {
              this.server = data.server
              var regionID = REGION_NAMES.indexOf(this.server)
              this.fetchLeaderboard(regionID)
            }
            // if (data.language) {
            //   var newLocale = data.language.replace("-", "_").toLowerCase()
            //   if (this.locale != newLocale) {
            //     console.log("Switch Locale", this.locale, newLocale)
            //     this.changeLocale(newLocale)
            //   }
            // }
          } else {
            console.log("/status parse data error")
          }

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
            console.log("error", e)
            setTimeout(this.requestStatusInfo, 100)
          }
        })
    },
    requestOppoInfo() {
      // Getting opponent rank, lp and tag
      // Once per opponent change

      // if (!this.IS_ELECTRON) {
      //   this.oppoName = "Lumus11";
      // }
      this.requestOpponentHistory()
    },
    requestTrackInfo() {
      if (!this.IS_ELECTRON) {
        setTimeout(this.processTrackInfo(testTrackData), 1500)
        return
      }

      lastTrackTime = Date.now()
      // console.log("requestTrackInfo")
      axios
        .get(`${this.apiBase}/track`)
        .then((response) => {
          if (response && response.data) {
            this.processTrackInfo(response.data)
          } else {
            console.log("/track parse data error")
          }

          var elapsedTime = Date.now() - lastTrackTime // ms
          if (requestDataWaitTime > elapsedTime) {
            setTimeout(this.requestTrackInfo, requestDataWaitTime - elapsedTime)
          } else {
            setTimeout(this.requestTrackInfo, 100)
          }
        })
        .catch((e) => {
          console.log("error", e)

          var elapsedTime = Date.now() - lastTrackTime // ms
          if (requestDataWaitTime > elapsedTime) {
            setTimeout(this.requestTrackInfo, requestDataWaitTime - elapsedTime)
          } else {
            setTimeout(this.requestTrackInfo, 100)
          }
        })
    },
    processTrackInfo(data) {
      if (data.positional_rectangles && data.positional_rectangles.OpponentName) {
        // Check if there is opponent
        var trackOppoName = data.positional_rectangles.OpponentName

        if (trackOppoName.includes("_")) {
          // opponent is AI
          this.oppoName = "AI"
          this.makeWindowVisible()
        } else if (!this.oppoName || this.oppoName.toLowerCase() != trackOppoName.toLowerCase()) {
          // If there is no oppoName set or there is a change in the name
          console.log("Track Info:", trackOppoName)
          this.oppoName = trackOppoName

          // this.requestOppoInfo()
          this.makeWindowVisible()
        }
      } else {
        // Clear Info about opponent and matches if there is no opponent

        this.oppoName = null
        this.oppoRank = null
        this.oppoLp = null
        this.matchInfos = []
      }

      if (data.deck_tracker) {
        if (data.deck_tracker.deckCode) {
          this.makeWindowVisible()
          if (this.startingDeckCode == null) {
            // switching from not having deck code
            this.handleGameStart()
          }
        }

        let startingCards, myGraveCards, myPlayedCards, oppoGraveCards
        try {
          startingCards = DeckEncoder.encodeCardsObj(data.deck_tracker.cardsInDeck)
          myGraveCards = DeckEncoder.encodeCardsObj(data.deck_tracker.myGraveyard)
          myPlayedCards = DeckEncoder.encodeCardsObj(data.deck_tracker.myPlayedCards)
          oppoGraveCards = DeckEncoder.encodeCardsObj(data.deck_tracker.oppoGraveCards)
          // Handles cards that are not encodable
          this.startingExtraCards = startingCards.extra
          this.myGraveExtraCards = myGraveCards.extra
          this.myPlayedExtraCards = myPlayedCards.extra
          this.oppoGraveExtraCards = oppoGraveCards.extra

          this.startingDeckCode = data.deck_tracker.deckCode || startingCards.code
          this.currentDeckCode = data.deck_tracker.currentDeckCode || startingCards.code
          this.oppoGraveCode = data.deck_tracker.opGraveyardCode || oppoGraveCards.code
          this.myPlayedCode = data.deck_tracker.myPlayedCardsCode || myPlayedCards.code
          this.cardsInHandNum = data.deck_tracker.cardsInHandNum
        } catch (error) {
          console.log(error)
        }
      } else {
        if (this.startingDeckCode != null) {
          // switching from having deck code
          console.log("Handle Game End")
          this.handleGameEnd()
        }
        this.startingDeckCode = null
        this.currentDeckCode = null
        this.myPlayedCode = null
        this.oppoGraveCode = null
        this.cardsInHandNum = null

        this.startingExtraCards = null
        this.myGraveExtraCards = null
        this.myPlayedExtraCards = null
        this.oppoGraveExtraCards = null

        this.hideWindow()
      }
    },
    processOpponentHistory(data) {
      // Process New Data
      console.log("Process Json Data")

      // if ((data.type == "deckCode" && data.deckCode != "" && data.deckCode != this.deckCode)) {
      // Changes Deck Code
      // Make window appear to display deck code
      // window.showWindow()
      // Switches to code tab
      // this.showCode()
      // } else
      if (JSON.stringify(this.matchInfos) != JSON.stringify(data)) {
        // Changes Match Info
        console.log("New Match Info")

        if (window.showWindow) window.showWindow()
        this.switchTab(TABS.oppo)
      }

      this.matchInfos = data
      // console.log(this.matchTotalNum)
    },
    handleGameEnd() {
      if (this.IS_ELECTRON) {
        window.ipcRenderer.send("game-end-trigger")
      }
    },
    handleGameStart() {
      if (this.IS_ELECTRON) {
        window.ipcRenderer.send("game-start-trigger")
      }
    },

    onCardHover(card) {
      if (!card) {
        this.showCardProb = false
        return
      } else {
        this.showCardProb = true
        this.cardProb = ((card.count / card.all) * 100).toFixed(1)
      }
    },

    onOpenDecklib() {
      this.currentLayer = LAYERS.decklib
    },
    setLayer(newLayer) {
      this.currentLayer = newLayer
    },
    onLayerBack() {
      this.currentLayer -= 1
    },
  },
}
</script>

<style>
html,
body,
#app {
  height: 100%;
}
</style>
