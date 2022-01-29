<template>
  <!-- <div id="content"> -->

  <!-- <h1 id="title">LoR Master Leaderboard</h1> -->

  <div class="sticky-top leaderboard-sticky-top">
    <div id="btn-group-regions" class="flex">
      <button id="btn-na" class="btn" :class="{ active: activeRegionID == 0 }" @click="switchRegion(regions.NA)">NA</button>
      <button id="btn-eu" class="btn" :class="{ active: activeRegionID == 1 }" @click="switchRegion(regions.EU)">EU</button>
      <button id="btn-sea" class="btn" :class="{ active: activeRegionID == 2 }" @click="switchRegion(regions.APAC)">APAC</button>
      <!-- <button id="btn-as" class="btn" :class="{active: activeRegionID == 2}" @click="switchRegion(regions.AS)">AS</button> -->
      <!-- <button id="btn-sea" class="btn" :class="{active: activeRegionID == 3}" @click="switchRegion(regions.SEA)">SEA</button> -->
    </div>

    <div id="search-container">
      <div class="search-icon left" v-if="!isLoading"><i class="fa fa-search"></i></div>
      <div class="search-icon left loading" v-if="isLoading"><i class="fa fa-circle-notch fa-spin"></i></div>
      <input spellcheck="false" autocomplete="off" v-model="searchText" id="search-input" type="text" :placeholder="isLoading ? $t('str.loading') : searchPlaceHolder" :disabled="isLoading" />
      <div class="search-icon right" @click="clearSearch" v-if="searchText != ''">
        <span><i class="fas fa-times"></i></span>
      </div>
    </div>

    <div class="flex info-help h-10">
      <div class="info-rank">{{ $t("leaderboard.rank") }}</div>
      <div class="info-name">{{ $t("leaderboard.name") }}</div>
      <div class="info-lp">{{ $t("leaderboard.points") }}</div>
    </div>
  </div>

  <div id="ladder">
    <leaderboard-player
      v-for="(player, index) in filteredPlayers"
      @click="searchPlayer(player)"
      :key="index"
      :rank="player.rank + 1"
      :name="player.name"
      :lp="player.lp"
      :deck="player.deck_code"
      :winRate="player.game_latest_rank_win_rate"
      :lastRankTime="player.game_latest_rank_time"
    >
    </leaderboard-player>
  </div>

  <!-- </div> -->
</template>

<script>
// const axios = require('axios')
import axios from "axios"
import LeaderboardPlayer from "./LeaderboardPlayer.vue"

export const REGION_ID = {
  NA: 0,
  EU: 1,
  APAC: 2,
}
export const REGION_SHORTS = ["NA", "EU", "APAC"]
export const REGION_NAMES = ["americas", "europe", "apac"]

const requestLeaderboardWaitTime = 1000 //ms
var lastLeaderboardRequestTime

import { useLeaderboardStore } from "../../store/StoreLeaderboard"
import { mapState, mapActions } from "pinia"

export default {
  mounted() {
    // this.getLeaderboard(this.activeRegionID)
    // console.log("Mounted Leaderboard")
    this.fetchLeaderboard(this.activeRegionID)
  },
  data() {
    return {
      rawPlayers: [],
      activeRegionID: 0,
      regions: REGION_ID,
      request: null,
      searchText: "",
      signedIn: false,
      dataStartTime: 0,
    }
  },
  emits: {
    search: ({ region, name, tag }) => {
      if (region && name && tag) {
        return true
      } else {
        console.warn("Invalid submit event payload!")
        return false
      }
    },
  },
  computed: {
    ...mapState(useLeaderboardStore, { leaderboard: "leaderboard", isLoading: "isLeaderboardLoading" }),
    filteredPlayers() {
      if (!this.leaderboard || !this.leaderboard[this.activeRegionID]) {
        return null
      }
      if (this.searchText) {
        var searchText = this.searchText
        var filteredPlayers = []
        var prefilteredPlayer = this.leaderboard[this.activeRegionID]
        for (var i = 0; i < prefilteredPlayer.length; i++) {
          if (prefilteredPlayer[i].name.toLowerCase().indexOf(searchText.toLowerCase()) !== -1) {
            filteredPlayers.push(prefilteredPlayer[i])
          }
        }
        // return this.players[this.activeRegionID].filter(function(player) {
        //     return player.name.toLowerCase().indexOf(searchText.toLowerCase()) !== -1
        // })

        return filteredPlayers.slice(0, 100) // TODO implement better way to improve this performence
      }
      return this.leaderboard[this.activeRegionID].slice(0, 100)
    },
    searchPlaceHolder() {
      if (this.leaderboard && this.leaderboard[this.activeRegionID]) {
        return this.$t("search.leaderboard.numPlayer", { num: this.leaderboard[this.activeRegionID].length })
      } else {
        return this.$t("search.leaderboard.base")
      }
    },
  },
  components: { LeaderboardPlayer },
  methods: {
    ...mapActions(useLeaderboardStore, ["fetchLeaderboard"]),
    clearSearch() {
      this.searchText = ""
      document.querySelector("#search-input").focus()
    },
    switchRegion(regionID) {
      this.sendUserEvent({
        category: "Main Window Leaderboard",
        action: "Select Region",
        label: REGION_NAMES[regionID],
        value: null,
      })

      if (this.activeRegionID != regionID) {
        this.fetchLeaderboard(regionID)
        this.activeRegionID = regionID
      }
    },

    searchPlayer(player) {
      // console.log("In leaderboard", player)
      if (player.tag) {
        // Only player with tag can be clicked=
        this.$router.push({
          name: 'search',
          query: { name: player.name, tag: player.tag , region: REGION_SHORTS[this.activeRegionID]}
        })
      }
    },
  },
}
</script>

<style lang="scss">
.info-help {
  color: white;
  background-color: var(--col-light-grey);
  width: 100%;
  padding: 5px 0px;
  margin: 20px 0px 0px 0px;
  align-items: center;
  justify-content: space-around;
  border-radius: 5px;

  white-space: nowrap;
}

.info-rank {
  width: 9.6%;
  text-align: center;
}

.info-name {
  width: 53.8%;
  text-align: left;
}

.info-lp {
  width: 9.6%;
  text-align: center;
}

/* Search */

.sticky-top {
  position: sticky;
  top: 0;
  background: var(--col-background);
}

.leaderboard-sticky-top {
  padding-bottom: 5px;
}

#search-container {
  position: relative;
  margin-top: 15px;
  /* width: 420px; */
  height: 50px;
}

#search-input {
  color: white;

  font-size: 16px;

  width: 100%;
  height: 100%;

  border: none;
  background-color: var(--col-darker-grey);
  padding: 20px 20px 20px 50px;
  border-radius: 40px;
  box-sizing: border-box;
}

#search-input:focus {
  outline: none;
  background-color: var(--col-dark-grey);
  /* box-shadow: 0px 0px 10px 2px var(--col-gold); */
}

.search-icon {
  position: absolute;
  width: 36px;
  height: 50px;
  line-height: 50px;
  vertical-align: middle;

  top: 0px;

  color: var(--col-dark-white);

  &.left {
    left: 10px;
  }

  &.right {
    right: 10px;
    cursor: pointer;
  }
}

#btn-menu {
  /* display: block; */
  display: none;
  position: relative;
  top: 0px;
  left: 0px;
}

#container {
  color: white;
}

#content {
  display: flex;
  flex-direction: column;

  width: 100%;

  align-items: center;
}

#title {
  margin-top: 0px;
  margin-bottom: 40px;
}

#btn-group-regions {
  border-radius: 5px;
}

#btn-group-regions .btn {
  background-color: transparent;
  color: var(--col-gold);

  width: 60px;
  height: 32px;

  font-size: 16px;

  cursor: pointer;

  border: 0px;
  border-bottom: 2px transparent solid;
}

#btn-group-regions .btn:hover {
  border-bottom: 2px var(--col-gold) solid;
}

#btn-group-regions .btn:focus {
  outline: 0px;
}

#btn-group-regions .btn.active {
  color: white;
  border-bottom: 2px var(--col-gold) solid;
}

/* Ladder  */
#ladder {
  margin-bottom: 25px;
  /* color: white; */
  display: flex;
  flex-direction: column;
  /* width: 520px; */
  gap: 5px;
}

/* @media only screen and (max-width: 768px) {
        #ladder {
            width: 400px;
        }
    } */
</style>
