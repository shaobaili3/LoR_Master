<template>
  <div>
    <div class="sticky-top search">
      <div class="region-tabs">
        <div
          class="region-option"
          v-for="(region, index) in regions"
          :class="{ selected: selectedRegion == region }"
          :key="index"
          @click="selectRegion(region)"
        >
          {{ region }}
        </div>
      </div>
      <div class="search-bar-container">
        <div class="search-bar-input-container">
          <button
            class="search-btn inside left"
            :class="{ active: searchText != '' }"
            @click="searchHistory"
          >
            <span v-if="isLoading || isUpdating"
              ><i class="fas fa-redo-alt fa-spin-fast"></i
            ></span>
            <span v-if="!(isLoading || isUpdating) && !isSameSearch"
              ><i class="fas fa-search"></i
            ></span>
            <span
              v-if="!(isLoading || isUpdating) && isSameSearch && !isUpdated"
              ><i class="fas fa-redo-alt"></i
            ></span>
            <span v-if="!(isLoading || isUpdating) && isSameSearch && isUpdated"
              ><i class="fas fa-check"></i
            ></span>
          </button>

          <input
            spellcheck="false"
            autocomplete="off"
            class="search-bar"
            @keyup="searchName"
            @keyup.enter="searchHistory"
            @keyup.up="autoCompleteIndexMinus"
            @keyup.down="autoCompleteIndexPlus"
            @focus="searchName"
            v-model="searchText"
            :placeholder="$t('search.player.placeholder')"
          />
          <button
            class="search-btn inside right"
            @click="clearSearch"
            v-if="searchText != ''"
          >
            <span><i class="fas fa-times"></i></span>
          </button>
        </div>
        <div class="search-bar-auto-complete">
          <div
            class="auto-complete-item"
            v-for="(name, index) in filteredInputNameList"
            :key="index"
            :class="{ selected: autoCompleteIndex == index }"
            @click="searchHistoryAutoComplete(index)"
          >
            {{ name }}
          </div>
        </div>
      </div>
    </div>
    <!-- Player Info -->
    <player-matches
      v-if="playerName && matches.length > 0"
      @search="searchPlayer($event)"
      :playerName="playerName"
      :playerRegion="playerRegion"
      :playerRank="playerRank"
      :playerLP="playerLP"
      :playerTag="playerTag"
      :matches="matches"
      ref="searchPlayerMatch"
    >
    </player-matches>

    <div class="status-text">
      <span
        v-if="!(isLoading || isUpdating) && !isError && matches.length <= 0"
      >
        {{ $t("search.prompt") }}
      </span>
      <span v-if="isLoading">
        <i class="fas fa-circle-notch fa-spin"></i>
        {{ $t("str.loading") }}
      </span>
      <span v-if="isUpdating">
        <i class="fas fa-circle-notch fa-spin"></i>
        {{ $t("str.updating") }}
      </span>
      <span v-if="isError">
        <!-- <i class="fas fa-circle-notch fa-spin"></i> -->
        {{ errorText }}
      </span>
    </div>
  </div>
</template>

<script>
const requestDataWaitTime = 400; //ms
const requestHistoryWaitTime = 100; //ms
const requestStatusWaitTime = 1000; //ms
const inputNameListLength = 10;

const requestRefreshDelay = 5000; //ms

let cancelToken, localCancleToken;
var lastStatusRequestTime;
var requestHistoryTimeout, prevHistoryRequest;

const regionNames = {
  NA: "americas",
  EU: "europe",
  AS: "asia",
};

const regionShort = {
  americas: "NA",
  europe: "EU",
  asia: "AS",
};

import {
  REGION_ID, REGION_SHORTS, REGION_NAMES
} from "../leaderboard/Leaderboard.vue"

import PlayerMatches from "../match/PlayerMatches.vue";
import axios from "axios";

export default {
  components: {
    PlayerMatches,
  },
  props: {
  },
  data() {
    return {
      matches: [],
      playerName: "",
      playerTag: "",
      playerRank: null,
      playerLP: null,
      playerRegion: null,
      searchText: "",
      isLoading: false,
      isUpdating: false,
      isError: false,
      isUpdated: false,

      errorType: "",

      inputNameList: [],
      autoCompleteIndex: -1,

      regions: REGION_SHORTS,
      selectedRegion: "NA",

      // Options
      autoLaunch: null,
      debugInfos: "",
    };
  },
  computed: {
    errorText() {
      var error = this.errorType;
      console.log("Processing error text from type", error);
      if (error == 0) {
        return this.$t("str.error.playerNotFound");
      } else if (error == 1 || error == 2) {
        return this.$t("str.error.playerNoHistory");
      } else if (error == 4) {
        return this.$t("str.error.internalServiceError");
      } else {
        return this.$t("str.error.unkown");
      }
    },
    isUpdatedVersion() {
      return this.version == this.remoteVersion;
    },
    filteredInputNameList() {
      return this.inputNameList.map((i) => i.split("#")[0]);
    },
    isSameSearch() {
      return (
        this.searchText == this.playerName &&
        this.playerTag &&
        REGION_SHORTS[REGION_ID[this.selectedRegion]] == this.playerRegion
      );
    },
    hasLocalInfo() {
      return this.localMatches && this.localMatches.length > 0;
    },
    versionText() {
      if (this.updateDownloaded) {
        return "Restart";
      }
      return this.version;
    },
    versionTooltip() {
      if (this.isUpdatedVersion) {
        return "Updated";
      } else if (this.updateDownloaded) {
        return "Update on next start";
      } else if (this.updateProcess > 0) {
        return `Downloading... ${this.updateProcess}%`;
      } else if (this.remoteVersion) {
        return `Latest: ${this.remoteVersion}`;
      }
      return this.$t("str.loading");
    },
  },
  methods: {
    selectRegion(region) {
      // region is region short
      this.sendUserEvent({
        category: "Main Window Search",
        action: "Select Region",
        label: REGION_NAMES[REGION_ID[region]],
        value: null,
      });

      this.selectedRegion = region;
      var searchBar = document.querySelector(".search-bar");
      if (searchBar) searchBar.focus();

      this.searchName();
    },
    searchPlayer(data) {
      // data.region is region short
      this.searchText = data.name;
      this.selectRegion(data.region);
      this.resetInputFocus();

      this.playerName = data.name;
      this.playerTag = data.tag;
      this.requestHistoryData();
    },
    // Search bar
    clearSearch() {
      this.searchText = "";
      this.searchName();
      document.querySelector(".search-bar").focus();
    },
    searchName() {
      if (this.searchText.length > 0) {
        this.requestNameData();
      } else {
        this.resetInputNameList();
      }
    },
    resetInputNameList() {
      this.inputNameList = [];
      this.autoCompleteIndex = -1;
    },
    resetInputFocus() {
      var searchBar = document.querySelector(".search-bar");
      if (searchBar) searchBar.blur();
      this.resetInputNameList();
    },
    // Search bar Auto Complete
    autoCompleteIndexPlus() {
      this.autoCompleteIndex += 1;
      if (this.autoCompleteIndex > inputNameListLength - 1) {
        this.autoCompleteIndex = inputNameListLength - 1;
      }
    },
    autoCompleteIndexMinus() {
      this.autoCompleteIndex -= 1;
      if (this.autoCompleteIndex < -1) {
        this.autoCompleteIndex = -1;
      }
    },
    searchHistoryAutoComplete(index) {
      // console.log("searchHistoryAutoComplete")
      this.autoCompleteIndex = index;
      this.searchHistory();
    },
    searchHistory() {

      console.log("Search History")
      var splited;
      if (
        this.inputNameList.length > 0 &&
        this.inputNameList[this.autoCompleteIndex]
      ) {
        // Use auto complete to fill the search
        // Sets player info for search
        splited = this.inputNameList[this.autoCompleteIndex].split("#");
        this.playerName = splited[0];
        this.playerTag = splited[1];

        this.searchText = this.playerName;

        this.sendUserEvent({
          category: "Main Window Search",
          action: "Auto Complete",
          label: this.playerName + "#" + this.playerTag,
          value: null,
        });

        // Perform the actual search
        this.requestHistoryData();
        this.resetInputFocus();
      } else {
        // Use user input
        splited = this.searchText.split("#");
        if (
          splited.length == 2 &&
          splited[0].length > 0 &&
          splited[1].length > 0
        ) {
          // Check if format is correct
          // Sets player info for search
          this.playerName = splited[0];
          this.playerTag = splited[1];

          this.sendUserEvent({
            category: "Main Window Search",
            action: "User Input [New]",
            label: `${this.searchText}`,
            value: null,
          });

          // Perform the actual search
          this.requestHistoryData();
          this.resetInputFocus();
        } else if (
          splited.length == 1 &&
          splited[0] == this.playerName &&
          this.playerTag
        ) {
          // When trying to search the same people, do a refresh (update only)

          if (this.isError) {
            // Unless it is error, in this case do a full refresh
            console.log("Refresh when error")
            this.requestHistoryData()
            this.resetInputFocus();
            return
          }

          console.log("Refresh & update only")
          this.requestHistoryUpdate();
          this.resetInputFocus();

          this.sendUserEvent({
            category: "Main Window Search",
            action: "User Input [Refresh]",
            label: `${this.searchText}`,
            value: null,
          });
        } else {
          // Alert the player needed info

          this.sendUserEvent({
            category: "Main Window Search",
            action: "User Input [Error]",
            label: `${this.searchText}`,
            value: null,
          });
        }
      }
    },
    clearInfo() {
      // this.playerName = "";
      // this.playerTag = "";
      this.playerRank = null;
      this.playerLP = null;
      this.playerRegion = null;
      this.matches = [];
    },
    errorHistory(error) {
      if (!this.isUpdating) {
        this.clearInfo();
      }
      this.isError = true;
      this.errorType = error;
      // this.playerName = "No history found"
    },
    openURL(url) {
      if (window.openExternal) {
        window.openExternal(url);
      } else {
        window.open(url);
      }
    },
    requestNameData() {
      axios
        .get(
          `${this.API_WEB}/name/${REGION_NAMES[REGION_ID[this.selectedRegion]]}/${
            this.searchText
          }`
        )
        .then((response) => {
          if (response.data == "Error") {
            // Error
          } else {
            // console.log(response.data)
            if (
              document.querySelector(".search-bar") == document.activeElement
            ) {
              // If the search bar is still in focus
              this.inputNameList = response.data.slice(0, inputNameListLength);
            } else {
              this.resetInputNameList();
            }
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else {
            console.log("error", e);
          }
        });
    },
    requestHistoryUpdate() {
      // Second request to makesure that the data is updated
      this.isUpdating = true;
      this.isUpdated = false;

      var newRequest = `${this.API_WEB}/search/${
        REGION_NAMES[REGION_ID[this.selectedRegion]]
      }/${this.playerName}/${this.playerTag}`;

      this.sendUserEvent({
        category: "Main Window Requests",
        action: "Update Search",
        label: "URL: " + newRequest,
        value: null,
      });

      const requestUpdateHistoryStartTime = Date.now();

      cancelToken = axios.CancelToken.source();
      axios
        .get(newRequest, {
          headers: {
            is_update: 1,
          },
          cancelToken: cancelToken.token,
        })
        .then((response) => {
          this.isUpdating = false;
          this.isUpdated = true;

          this.sendUserEvent({
            category: "Main Window Requests",
            action: "Updated Search Result [Success]",
            label: "URL: " + newRequest,
            value: Date.now() - requestUpdateHistoryStartTime,
          });

          this.processSearchHistory(response.data);
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request (update) cancelled");
          } else {
            console.log("error", e);

            if (e.response) {
              if (e.response.status == 500) {
                this.errorHistory(4); // Internal sercive error
              } else {
                var data = e.response.data;
                this.errorHistory((data.status && data.status.error) || 3); // give a 3 so that there is a fallback
              }
            } else {
              this.errorHistory(3); // Unkown Error
            }
            this.isUpdating = false;

            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Updated Search Result [Fail]",
              label: "Type: " + this.errorType + " | URL: " + newRequest,
              value: Date.now() - requestUpdateHistoryStartTime,
            });
          }
        });
    },
    requestHistoryData() {
      if (this.localHistoryLoading) {
        // Before start, wait until old local search resolves
        if (requestHistoryTimeout) clearTimeout(requestHistoryTimeout);
        requestHistoryTimeout = setTimeout(
          this.requestHistoryData,
          requestHistoryWaitTime
        );
        return;
      }

      var newRequest = `${this.API_WEB}/search/${
        REGION_NAMES[REGION_ID[this.selectedRegion]]
      }/${this.playerName}/${this.playerTag}`;
      if (prevHistoryRequest == newRequest && this.isLoading) {
        // Don't refresh if the request is the same and ongoing
        return;
      }

      //Check if there are any previous pending requests
      if (typeof cancelToken != typeof undefined) {
        cancelToken.cancel("Operation canceled due to new request.");
      }

      //Save the cancel token for the current request
      cancelToken = axios.CancelToken.source();

      this.isLoading = true;
      this.isError = false;
      this.isUpdated = false;
      this.isUpdating = false;
      this.playerRegion = REGION_SHORTS[REGION_ID[this.selectedRegion]];

      prevHistoryRequest = newRequest;

      this.sendUserEvent({
        category: "Main Window Requests",
        action: "Request Search",
        label: "URL: " + newRequest,
        value: null,
      });

      const requestHistoryStartTime = Date.now();

      axios
        .get(newRequest, {
          headers: {
            is_update: 0,
          },
          cancelToken: cancelToken.token,
        }) // Pass the cancel token
        .then((response) => {
          this.isLoading = false;

          this.sendUserEvent({
            category: "Main Window Requests",
            action: "Got Search Result [Success]",
            label: "URL: " + newRequest,
            value: Date.now() - requestHistoryStartTime,
          });

          this.processSearchHistory(response.data);

          this.requestHistoryUpdate()
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else {
            console.log("error", e);

            if (e.response) {
              if (e.response.status == 500) {
                this.errorHistory(4); // Internal sercive error
              } else {
                var data = e.response.data;
                this.errorHistory((data.status && data.status.error) || 3); // give a 3 so that there is a fallback
              }
            } else {
              this.errorHistory(3); // Unkown Error
            }
            this.isLoading = false;

            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Got Search Result [Fail]",
              label: "Type: " + this.errorType + " | URL: " + newRequest,
              value: Date.now() - requestHistoryStartTime,
            });
          }
        });
    },
    processHistory(data, playerName, playerServer) {
      // playerServer is region shorts
      console.log("Process History!", playerName, playerServer);
      // console.log(data);

      var matchInfo = {
        matches: [],
        rank: null,
        lp: null,
      };

      // Set selected filter to null
      if (
        this.$refs.searchPlayerMatch &&
        this.$refs.searchPlayerMatch.setFilterDeckCode
      ) {
        this.$refs.searchPlayerMatch.setFilterDeckCode(null);
      }

      if (!data) return matchInfo;

      // if (playerServer == "sea") {
      //   // sea players only have local data
      //   for (let match of data) {
      //     let opponentName,
      //       opponentRank,
      //       opponentLp,
      //       opponentTag,
      //       opponentDeck,
      //       deck,
      //       rounds,
      //       win,
      //       time,
      //       order;

      //     matchInfo.rank = match.playerRank; // Currently no value
      //     matchInfo.lp = match.playerLp; // Currently no value

      //     opponentName = match.opponentName;
      //     opponentTag = null; // Cannot get
      //     opponentRank = match.opponentRank; // Currently no value
      //     opponentLp = match.opponentLp; // Currently no value
      //     opponentDeck = match.deck_tracker.opGraveyardCode;
      //     deck = match.deck_tracker.deckCode;
      //     rounds = null; // Cannot get
      //     win = match.localPlayerWon;
      //     time = match.startTime;
      //     order = null; // Cannot get

      //     let badges = []; // Currently no value

      //     let details = {
      //       openHand: match.deck_tracker.openHand,
      //       replacedHand: match.deck_tracker.replacedHand,
      //       timeline: match.deck_tracker.timeline,
      //       startTime: match.startTime,
      //       endTime: match.endTime,
      //     };

      //     matchInfo.matches.push({
      //       opponentName: opponentName,
      //       deck: deck,
      //       region: regionShort[this.localPlayerInfo.server],
      //       opponentDeck: opponentDeck,
      //       opponentRank: opponentRank,
      //       opponentLp: opponentLp,
      //       opponentTag: opponentTag,
      //       rounds: rounds,
      //       win: win,
      //       time: time,
      //       badges: badges,
      //       details: details,
      //     });
      //   }
      // } else 
      {
        // Processing for normal Data
        for (var key in data) {
          var match = data[key];
          if (
            !match ||
            !match.player_info ||
            !match.player_info[0] ||
            !match.player_info[0].name
          )
            continue; // Skip if null history

          var isFirstPlayer =
            match.player_info[0].name.toLowerCase() == playerName.toLowerCase();
          var player, playerGame, opponent, opponentGame;
          var info = match.info;
          var details = null;

          if (match.local && match.local.deck_tracker) {
            details = {
              openHand: match.local.deck_tracker.openHand,
              replacedHand: match.local.deck_tracker.replacedHand,
              timeline: match.local.deck_tracker.timeline,
              startTime: match.local.startTime,
              endTime: match.local.endTime,
            };
          }

          var opponentName,
            opponentRank,
            opponentLp,
            opponentTag,
            opponentDeck,
            deck,
            rounds,
            win,
            time,
            order;

          if (isFirstPlayer) {
            playerGame = info.players[0];
            opponentGame = info.players[1];

            player = match.player_info[0];
            opponent = match.player_info[1];
          } else {
            playerGame = info.players[1];
            opponentGame = info.players[0];

            player = match.player_info[1];
            opponent = match.player_info[0];
          }

          if (!playerGame || !opponentGame || !player || !opponent) continue;

          opponentName = opponent.name;

          if (opponent.rank !== "") {
            opponentRank = opponent.rank + 1; // rank starts from 0
          } else {
            opponentRank = ""; // ranks can be empty
          }

          opponentLp = opponent.lp;
          opponentTag = opponent.tag;

          if (!matchInfo.rank && player.rank !== "") {
            matchInfo.rank = player.rank + 1; // player.rank starts from 0
          }

          if (!matchInfo.lp) matchInfo.lp = player.lp;

          deck = playerGame.deck_code;
          opponentDeck = opponentGame.deck_code;
          order = playerGame.order_of_play;
          win = playerGame.game_outcome == "win";
          rounds = info.total_turn_count;
          var badges = [];
          if (info.game_mode)
            badges.push(
              info.game_mode
                .replace(/([A-Z])/g, " $1")
                .trim()
                .replace("Lobby", "")
            );
          if (info.game_type)
            badges.push(
              info.game_type
                .replace(/([A-Z])/g, " $1")
                .trim()
                .replace("Lobby", "")
            );

          time = info.game_start_time_utc;

          matchInfo.matches.push({
            opponentName: opponentName,
            deck: deck,
            region: playerServer, // region short passed in, essentially this.playerRegion
            opponentDeck: opponentDeck,
            opponentRank: opponentRank,
            opponentLp: opponentLp,
            opponentTag: opponentTag,
            rounds: rounds,
            win: win,
            time: time,
            badges: badges,
            details: details,
          });
        }
      }

      return matchInfo;
    },
    processSearchHistory(data) {
      var Info = this.processHistory(data, this.playerName, this.playerRegion);
      this.matches = Info.matches;
      this.playerRank = Info.rank;
      this.playerLP = Info.lp;
    },
  },
};
</script>