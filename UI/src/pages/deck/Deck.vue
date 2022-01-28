<template>
  <base-window-controls
    :canClose="false"
    :canShrink="true"
    :playerName="oppoName"
    :playerRank="oppoRank"
    :playerLP="oppoLp"
    :titleType="'match'"
  ></base-window-controls>

  <div id="content">
    <div class="loading" :class="{ invisible: !isLoading }">
      {{ loadingText }}
    </div>

    <div class="tabs px-0 xxs:px-1 xs:px-2" v-if="!isLoading">
      <div class="tab-title-group">
        <div
          class="tab-title text-sm xxs:text-base xs:text-lg"
          @click="switchTab(TABS.oppo)"
          :class="{ active: isShowOppo }"
        >
          <i class="fas fa-swords"></i>
        </div>
        <div
          class="tab-title text-sm xxs:text-base xs:text-lg"
          @click="switchTab(TABS.oppog)"
          :class="{ active: isShowOppoGrave }"
        >
          <i class="fas fa-tombstone-alt"></i>
        </div>
      </div>
      <div class="tab-title-group">
        <div
          class="tab-title text-sm xxs:text-base xs:text-lg"
          @click="switchTab(TABS.my)"
          :class="{ active: isShowMy }"
        >
          <i class="fas fa-user-cowboy"></i>
        </div>
        <div
          class="tab-title text-sm xxs:text-base xs:text-lg"
          @click="switchTab(TABS.myg)"
          :class="{ active: isShowMyGrave }"
        >
          <i class="fas fa-tombstone-alt"></i>
        </div>
      </div>
    </div>

    <!-- Opponent History -->
    <div id="history" class="tab-content" v-if="isShowOppo && !isLoading">
      <div
        class="loading"
        v-if="matchInfos.length <= 0"
        :class="{ zeroHeight: oppoPinnedId !== null }"
      >
        {{ loadingOppoText }}
      </div>

      <div class="w-full" v-if="matchInfos && matchInfos.length > 0">
        <match-info
          v-for="match in matchInfos"
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
        ></match-info>
      </div>
    </div>

    <div
      class="layerpanel max-w-[280px] h-10 p-2 xxs:h-11 xxs:p-1"
      :class="{ expanded: currentLayer != LAYERS.base }"
      v-if="isShowOppo"
    >
      <button
        v-if="currentLayer == LAYERS.base"
        @click="onOpenDecklib"
        class="btn btn-decklib text-sm py-1 px-2 xxs:text-base"
      >
        Open Deck Library
      </button>
      <button
        class="btn btn-back"
        v-if="currentLayer != LAYERS.base"
        @click="onLayerBack"
      >
        <span><i class="fas fa-caret-down"></i></span>
      </button>
      <tracker-layer
        v-if="currentLayer != LAYERS.base"
        @showDeck="onPinOppo"
        :pinDeckId="oppoPinnedId"
      ></tracker-layer>
    </div>

    <!-- Oppo Played -->
    <div class="tab-content" v-if="isShowOppoGrave && !isLoading">
      <div class="tab-text">{{ $t("tracker.tabs.oppoPlayed") }}</div>
      <deck-detail
        :deck="oppoGraveCode"
        :baseDeck="oppoGraveCode"
        :showCopy="false"
        :extra="oppoGraveExtraCards"
      ></deck-detail>
    </div>

    <!-- My Deck -->
    <div class="tab-content" v-if="isShowMy && !isLoading">
      <deck-regions :deck="startingDeckCode" :fixedWidth="false"></deck-regions>
      <deck-detail
        :deck="currentDeckCode"
        :baseDeck="startingDeckCode"
      ></deck-detail>
    </div>

    <!-- My Played -->
    <div class="tab-content" v-if="isShowMyGrave && !isLoading">
      <div class="tab-text">{{ $t("tracker.tabs.myPlayed") }}</div>
      <deck-detail
        :baseDeck="myPlayedCode"
        :showCopy="false"
        :extra="myPlayedExtraCards"
      ></deck-detail>
    </div>

    <div class="footer" v-if="!isLoading">
      <div class="footer-text">
        {{ $t("tracker.cardsInHand", { num: cardsInHandNum }) }}
      </div>
    </div>
  </div>
</template>


<script>
import MatchInfo from "../../components/match/MatchInfo.vue";
import axios from "axios";
import BaseWindowControls from "../../components/base/BaseWindowControls.vue";
import DeckDetail from "../../components/deck/DeckDetail.vue";
import DeckRegions from "../../components/deck/DeckRegions.vue";
import DeckEncoder from "../../modules/runeterra/DeckEncoder";
import Card from "../../modules/runeterra/Card";

import { mapActions, mapState } from "vuex";

import "../../assets/scss/tooltips.scss";
import "../../assets/scss/deck.scss";
import "../../assets/scss/transitions.scss";

const testTrackData = require("../../assets/data/testTrack");
// const testTrackData = require('../../assets/data/testTrackLab')
const testStatusData = require("../../assets/data/testStatusEN");
// const testStatusData = require('../../assets/data/testStatus')

import TrackerLayer from "../../components/tracker/TrackerLayer.vue";

const requestDataWaitTime = 100; // ms
const requestServerWaitTime = 3000; //ms
const requestStatusWaitTime = 1000; //ms

// const portNum = "26531"
// const API_BASE = `http://127.0.0.1:${portNum}`

const REGION_NAMES = ["americas", "europe", "asia", "sea"];

const TABS = {
  oppo: 0,
  my: 1,
  oppog: 2,
  myg: 3,
};

const LAYERS = {
  base: 0,
  decklib: 1,
  deckdetail: 2,
};

const api_error = "https://lormaster.herokuapp.com/error";

var lastTrackTime, lastServerRequestTime, lastStatusRequestTime;

export default {
  components: {
    BaseWindowControls,
    MatchInfo,
    DeckDetail,
    DeckRegions,
    TrackerLayer,
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

      portNum: "26531",

      currentLayer: 0,
    };
  },
  computed: {
    ...mapState('leaderboardData', {
      leaderboard: 'leaderboard',
      isLeaderboardLoading: 'isLoading'
    }),
    isLoading() {
      if (this.currentDeckCode || this.startingDeckCode) return false;
      if (this.matchInfos.length > 0) return false;
      return (
        this.oppoName == null ||
        this.oppoName == "" ||
        this.matchInfos.length == 0
      );
      // return true
    },
    oppoLeaderboard() {
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
    loadingText() {
      return this.$t("loading.readyToRock");
    },
    loadingOppoText() {
      if (this.requestOpponentHistoryError) return this.$t("loading.nohistory");
      if (this.isLoadingOpponentHistory) return this.$t("loading.history");
      return this.$t("loading.nohistory");
    },
    isShowOppo() {
      return this.currentTab == TABS.oppo;
    },
    isShowMy() {
      return this.currentTab == TABS.my;
    },
    isShowOppoGrave() {
      return this.currentTab == TABS.oppog;
    },
    isShowMyGrave() {
      return this.currentTab == TABS.myg;
    },
    isInvalidDeckCode() {
      try {
        var deck = DeckEncoder.decode(this.deckCode);
      } catch (err) {
        // console.log(err.message)
        return true;
      }
      return false;
    },
    matchTotalNum() {
      // console.log(this.matchInfos);
      return this.matchInfos.reduce((total, item) => total + item.matches, 0);
    },
  },
  mounted() {
    // console.log(JSON.stringify(this.matchInfos))
    // this.getMatchInfo()
    // this.getSubData()
    // console.log("Mounted")
    // this.requestData()
    console.log("Page Deck Mounted");
    console.log(`API BASE: ${this.apiBase}`);
    
    // this.hideWindow()
    if (this.IS_ELECTRON) {
      window.ipcRenderer.on("return-port", (event, port) => {
        console.log("New Port:", port);
        this.portNum = port;
      });

      window.ipcRenderer.send("get-port");

      this.initStore();
      this.initChangeLocale();
    }

    this.requestStatusInfo();
    this.requestTrackInfo();
    // this.requestServerInfo()
  },
  methods: {
    ...mapActions(["changeLocale", 'leaderboardData/fetchLeaderboard']),

    initStore() {
      window.ipcRenderer.send("request-store", "ui-locale");

      window.ipcRenderer.on("reply-store", (event, key, val) => {
        // console.log("Got store", key, val);

        if (key == "ui-locale" && val) {
          this.$i18n.locale = val;
          console.log("Change locale to", val);
        }
      });
    },
    // Change Locale
    initChangeLocale() {
      console.log("Initing Change Locale | current locale", this.$i18n.locale);

      window.ipcRenderer.on("to-change-locale", (event, newLocale) => {
        this.$i18n.locale = newLocale;
        console.log("Changing locale to", newLocale);
      });

      window.ipcRenderer.on("request-test-history", (event) => {
        this.requestTestOppoHistory();
      });
    },

    hideWindow() {
      if (window.hideWindow) {
        window.hideWindow();
      }
    },
    makeWindowVisible() {
      if (window.makeVisible) {
        window.makeVisible();
      }
    },
    switchTab(newTab) {
      if (this.IS_ELECTRON) {
        this.sendUserEvent({
          category: "Tracker Event",
          action: "Switch Tab",
          label: "From: " + this.currentTab + " | To: " + newTab,
          value: null,
        });
      }

      this.currentTab = newTab;
    },
    async getSubData() {
      if (window.sock)
        for await (const [topic, msg] of window.sock) {
          this.processRawData(msg);
        }
    },
    requestOpponentHistory() {
      // http://192.168.20.4:${portNum}/history/asia/J01/J01

      console.log(
        "Request Opponent History for " + this.oppoName 
      );

      this.isLoadingOpponentHistory = true;
      this.requestOpponentHistoryError = null;

      var api = `${this.API_WEB}/history/${this.server}/${this.oppoName}`;

      axios
        .get(api)
        .then((response) => {
          console.log("Opponent Data", response.data);
          this.isLoadingOpponentHistory = false;
          this.processOpponentHistory(response.data);
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else {
            console.log("error", e);
            this.requestOpponentHistoryError = e;
          }
        });
    },
    requestTestOppoHistory() {
      const stormHistoryAPI = `${this.API_WEB}/history/americas/storm`;
      axios
        .get(stormHistoryAPI)
        .then((response) => {
          console.log("Opponent Data", response.data);
          this.processOpponentHistory(response.data);
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else {
            console.log("error", e);
          }
        });
    },
    requestStatusInfo() {
      if (!this.IS_ELECTRON) {
        var data = testStatusData;
        this.server = data.server;
        var regionID = REGION_NAMES.indexOf(this.server)
        if (regionID >= 0) {
          this['leaderboardData/fetchLeaderboard'](regionID);
        }
        if (data.language) {
          var newLocale = data.language.replace("-", "_").toLowerCase();
          if (this.locale != newLocale) {
            console.log("Switch Locale", this.locale, newLocale);
            this.changeLocale(newLocale);
          }
        }

        return;
      }

      // Keeps requesting status
      lastStatusRequestTime = Date.now();
      axios
        .get(`${this.apiBase}/status`) // status
        .then((response) => {
          var elapsedTime = Date.now() - lastStatusRequestTime; // ms

          if (response && response.data) {
            var data = response.data;
            if (data.server && this.server != data.server) {
              this.server = data.server;
              var regionID = REGION_NAMES.indexOf(this.server)
              this['leaderboardData/fetchLeaderboard'](regionID);
            }
            if (data.language) {
              var newLocale = data.language.replace("-", "_").toLowerCase();
              if (this.locale != newLocale) {
                console.log("Switch Locale", this.locale, newLocale);
                this.changeLocale(newLocale);
              }
            }
          } else {
            console.log("/status parse data error");
          }

          if (requestStatusWaitTime > elapsedTime) {
            setTimeout(
              this.requestStatusInfo,
              requestStatusWaitTime - elapsedTime
            );
          } else {
            setTimeout(this.requestStatusInfo, 100);
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else {
            console.log("error", e);
            setTimeout(this.requestStatusInfo, 100);
          }
        });
    },
    requestOppoInfo() {
      // Getting opponent rank, lp and tag
      // Once per opponent change

      // if (!this.IS_ELECTRON) {
      //   this.oppoName = "Lumus11";
      // }
      this.requestOpponentHistory();
    },
    requestTrackInfo() {
      if (!this.IS_ELECTRON) {
        if (!this.startingDeckCode) {
          Math.random() > 0.2
            ? this.processTrackInfo(testTrackData)
            : this.processTrackInfo({
                positional_rectangles: null,
              });
        } else {
          this.processTrackInfo(testTrackData);
        }

        setTimeout(this.requestTrackInfo, 1000);
        return;
      }

      lastTrackTime = Date.now();
      // console.log("requestTrackInfo")
      axios
        .get(`${this.apiBase}/track`)
        .then((response) => {
          if (response && response.data) {
            this.processTrackInfo(response.data);
          } else {
            console.log("/track parse data error");
          }

          var elapsedTime = Date.now() - lastTrackTime; // ms
          if (requestDataWaitTime > elapsedTime) {
            setTimeout(
              this.requestTrackInfo,
              requestDataWaitTime - elapsedTime
            );
          } else {
            setTimeout(this.requestTrackInfo, 100);
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            // console.log("Request cancelled");
          } else {
            console.log("error", e);

            var elapsedTime = Date.now() - lastTrackTime; // ms
            if (requestDataWaitTime > elapsedTime) {
              setTimeout(
                this.requestTrackInfo,
                requestDataWaitTime - elapsedTime
              );
            } else {
              setTimeout(this.requestTrackInfo, 100);
            }
          }
        });
    },
    processTrackInfo(data) {
      if (
        data.positional_rectangles &&
        data.positional_rectangles.OpponentName
      ) {
        // Check if there is opponent
        var trackOppoName = data.positional_rectangles.OpponentName;

        if (trackOppoName.includes("_")) {
          // opponent is AI
          this.oppoName = "AI";
          this.makeWindowVisible();
        } else if (
          !this.oppoName ||
          this.oppoName.toLowerCase() != trackOppoName.toLowerCase()
        ) {
          // If there is no oppoName set or there is a change in the name
          console.log("Track Info:", trackOppoName);
          this.oppoName = trackOppoName;
          
          this.oppoRank = this.oppoLeaderboard?.rank
          this.oppoLp = this.oppoLeaderboard?.lp
          
          this.requestOppoInfo();
          this.makeWindowVisible();
        }
      } else {
        // Clear Info about opponent and matches if there is no opponent

        this.oppoName = null;
        this.oppoRank = null;
        this.oppoLp = null;
        this.matchInfos = [];
      }

      if (data.deck_tracker) {
        if (data.deck_tracker.deckCode) {
          this.makeWindowVisible();
          if (this.startingDeckCode == null) {
            // switching from not having deck code
            this.handleGameStart();
          }
        }

        let startingCards, myGraveCards, myPlayedCards, oppoGraveCards;
        try {
          startingCards = DeckEncoder.encodeCardsObj(
            data.deck_tracker.cardsInDeck
          );
          myGraveCards = DeckEncoder.encodeCardsObj(
            data.deck_tracker.myGraveyard
          );
          myPlayedCards = DeckEncoder.encodeCardsObj(
            data.deck_tracker.myPlayedCards
          );
          oppoGraveCards = DeckEncoder.encodeCardsObj(
            data.deck_tracker.oppoGraveCards
          );
          // Handles cards that are not encodable
          this.startingExtraCards = startingCards.extra;
          this.myGraveExtraCards = myGraveCards.extra;
          this.myPlayedExtraCards = myPlayedCards.extra;
          this.oppoGraveExtraCards = oppoGraveCards.extra;

          this.startingDeckCode =
            data.deck_tracker.deckCode || startingCards.code;
          this.currentDeckCode =
            data.deck_tracker.currentDeckCode || startingCards.code;
          this.oppoGraveCode =
            data.deck_tracker.opGraveyardCode || oppoGraveCards.code;
          this.myPlayedCode =
            data.deck_tracker.myPlayedCardsCode || myPlayedCards.code;
          this.cardsInHandNum = data.deck_tracker.cardsInHandNum;
        } catch (error) {
          console.log(error);
        }
      } else {
        if (this.startingDeckCode != null) {
          // switching from having deck code
          console.log("Handle Game End");
          this.handleGameEnd();
        }
        this.startingDeckCode = null;
        this.currentDeckCode = null;
        this.myPlayedCode = null;
        this.oppoGraveCode = null;
        this.cardsInHandNum = null;

        this.startingExtraCards = null;
        this.myGraveExtraCards = null;
        this.myPlayedExtraCards = null;
        this.oppoGraveExtraCards = null;

        this.hideWindow();
      }
    },
    processOpponentHistory(data) {
      // Process New Data
      console.log("Process Json Data");

      // if ((data.type == "deckCode" && data.deckCode != "" && data.deckCode != this.deckCode)) {
      // Changes Deck Code
      // Make window appear to display deck code
      // window.showWindow()
      // Switches to code tab
      // this.showCode()
      // } else
      if (JSON.stringify(this.matchInfos) != JSON.stringify(data)) {
        // Changes Match Info
        console.log("New Match Info");

        if (window.showWindow) window.showWindow();
        this.switchTab(TABS.oppo);
      }

      this.matchInfos = data;
      // console.log(this.matchTotalNum)
    },
    handleGameEnd() {
      if (this.IS_ELECTRON) {
        window.ipcRenderer.send("game-end-trigger");
      }
    },
    handleGameStart() {
      if (this.IS_ELECTRON) {
        window.ipcRenderer.send("game-start-trigger");
      }
    },

    onOpenDecklib() {
      this.currentLayer = LAYERS.decklib;
    },
    setLayer(newLayer) {
      this.currentLayer = newLayer;
    },
    onLayerBack() {
      this.currentLayer -= 1;
    },
    onPinOppo(code, id) {
      console.log("Pinning", code, id);
      // this.oppoPinnedCode = code
      this.oppoPinnedId = id;
    },
  },
};
</script>