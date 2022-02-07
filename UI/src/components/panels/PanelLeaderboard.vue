<template>
  <div class="flex justify-center h-full px-2 sm:px-4">
    <div class="flex-1 w-0 max-w-3xl">
      <div class="flex flex-col h-full px-2 sm:px-0">
        <h1 class="flex items-end w-full text-left sm:block sm:text-white title">
          <!-- Title -->
          <div v-if="!IS_ELECTRON" class="hidden sm:block sm:text-3xl sm:flex-initial sm:pb-4 sm:w-auto text-ellipsis">
            {{ $t("str.leaderboard") }}
            <h2 class="hidden text-base text-gray-300 sm:pl-4 sm:inline">{{ $t("leaderboard.desc") }}</h2>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 w-fit h-[32px]">
            <button
              class="text-base border-b-2 w-[60px]"
              :class="{ ' text-white  border-gold-400': activeRegionID == 0, 'text-gold-400 border-transparent': activeRegionID != 0 }"
              @click="switchRegion(regions.NA)"
            >
              NA
            </button>
            <button
              class="text-base border-b-2 w-[60px]"
              :class="{ ' text-white  border-gold-400': activeRegionID == 1, 'text-gold-400 border-transparent': activeRegionID != 1 }"
              @click="switchRegion(regions.EU)"
            >
              EU
            </button>
            <button
              class="text-base border-b-2 w-[60px]"
              :class="{ ' text-white  border-gold-400': activeRegionID == 2, 'text-gold-400 border-transparent': activeRegionID != 2 }"
              @click="switchRegion(regions.APAC)"
            >
              APAC
            </button>
            <!-- <button id="btn-as" class="btn" :class="{active: activeRegionID == 2}" @click="switchRegion(regions.AS)">AS</button> -->
            <!-- <button id="btn-sea" class="btn" :class="{active: activeRegionID == 3}" @click="switchRegion(regions.SEA)">SEA</button> -->
          </div>
        </h1>

        <!-- Search bar -->
        <div class="">
          <div class="mt-2 relative h-[50px]">
            <div class="search-icon left" v-if="!isLoading"><i class="fa fa-search"></i></div>
            <div class="search-icon left loading" v-if="isLoading"><i class="fa fa-circle-notch fa-spin"></i></div>
            <input
              id="search-input"
              class="rounded-[25px] focus:bg-gray-700 bg-gray-800 transition-rounded"
              :class="{ 'rounded-tl-md': activeRegionID == 0 }"
              spellcheck="false"
              autocomplete="off"
              v-model="searchText"
              type="text"
              :placeholder="isLoading ? $t('str.loading') : searchPlaceHolder"
              :disabled="isLoading"
            />
            <div class="search-icon right" @click="clearSearch" v-if="searchText != ''">
              <span><i class="fas fa-times"></i></span>
            </div>
          </div>
        </div>

        <!-- Headers -->
        <div class="grid grid-cols-12 h-12 pt-1 sticky top-0 z-[2] bg-gray-900 items-center text-sm whitespace-nowrap">
          <div class="bg-gray-900 sm:px-2">{{ $t("leaderboard.rank") }}</div>
          <div class="col-span-5 px-2 bg-gray-900 sm:col-span-3">{{ $t("leaderboard.name") }}</div>
          <div class="col-span-2 sm:px-2 sm:col-span-1">{{ $t("leaderboard.points") }}</div>
          <div class="hidden px-2 sm:block sm:col-span-2">{{ $t("leaderboard.lastRank") }}</div>
          <div class="hidden px-2 sm:block sm:col-span-2">{{ $t("leaderboard.lastX", { num: 20 }) }}</div>
          <div class="col-span-4 px-2 sm:col-span-3">{{ $t("leaderboard.recent") }}</div>
        </div>

        <RecycleScroller
          v-if="filteredPlayers"
          class="flex-1 block w-full h-0 overflow-y-auto rounded-md"
          :items="filteredPlayers"
          :item-size="64"
          key-field="rank"
        >
          <template v-slot="{ item }"
            ><leaderboard-player
              @click="searchPlayer(item)"
              :rank="(item.rank + 1).toString()"
              :name="item.name"
              :lp="item.lp"
              :deck="item.deck_code"
              :winRate="item.game_latest_rank_win_rate"
              :lastRankTime="item.game_latest_rank_time"
            >
            </leaderboard-player
          ></template>
        </RecycleScroller>
      </div>
    </div>
  </div>
</template>

<script>
// const axios = require('axios')
// import axios from "axios"
import LeaderboardPlayer from "../leaderboard/LeaderboardPlayer.vue"

export const REGION_ID = {
  NA: 0,
  EU: 1,
  APAC: 2,
}
export const REGION_SHORTS = ["NA", "EU", "APAC"]
export const REGION_NAMES = ["americas", "europe", "apac"]

export const regionNameToShorts = (name) => {
  if (name == "sea" || name == "asia") {
    return "APAC"
  } else {
    let nameIndex = REGION_NAMES.indexOf(name)
    if (nameIndex != -1) return REGION_SHORTS[nameIndex]
  }
  return null
}

const requestLeaderboardWaitTime = 1000 //ms
var lastLeaderboardRequestTime

const leaderboardStorageID = "lmt-settings-leaderboard-region"

import { useLeaderboardStore } from "../../store/StoreLeaderboard"
import { mapState, mapActions } from "pinia"

export default {
  components: { LeaderboardPlayer },
  mounted() {
    // this.getLeaderboard(this.activeRegionID)
    // console.log("Mounted Leaderboard")
    let oldRegion = window.localStorage.getItem(leaderboardStorageID)
    if (oldRegion) {
      this.activeRegionID = oldRegion
    }

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

        return filteredPlayers // TODO implement better way to improve this performence
      }
      return this.leaderboard[this.activeRegionID]
    },
    searchPlaceHolder() {
      if (this.leaderboard && this.leaderboard[this.activeRegionID]) {
        return this.$t("search.leaderboard.numPlayer", { num: this.leaderboard[this.activeRegionID].length })
      } else {
        return this.$t("search.leaderboard.base")
      }
    },
  },
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
        window.localStorage.setItem(leaderboardStorageID, regionID)
      }
    },

    searchPlayer(player) {
      if (player.tag) {
        // Only player with tag can be clicked=
        this.$router.push({
          name: "search",
          query: { name: player.name, tag: player.tag, region: REGION_SHORTS[this.activeRegionID] },
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

// #search-container {
//   position: relative;
//   /* width: 420px; */
//   height: 50px;
// }

#search-input {
  color: white;

  font-size: 16px;

  width: 100%;
  height: 100%;

  border: none;
  // background-color: var(--col-darker-grey);
  padding: 20px 20px 20px 50px;
  box-sizing: border-box;
}

#search-input:focus {
  outline: none;
  // background-color: var(--col-dark-grey);
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
