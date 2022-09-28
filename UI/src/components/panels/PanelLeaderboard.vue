<template>
  <div class="flex h-full justify-center gap-6 px-2 sm:px-4">
    <!-- Left -->
    <div class="hidden w-[30%] min-w-[350px] max-w-[425px] flex-shrink justify-center lg:flex">
      <div class="flex h-full w-full max-w-md flex-col text-left">
        <LadderHighlight
          :activeRegionID="activeRegionID"
          @searchPlayer="searchPlayer"
        ></LadderHighlight>
      </div>
    </div>
    <!-- Center -->
    <div class="w-0 max-w-3xl flex-[2]">
      <div class="flex h-full flex-col px-2 sm:px-0">
        <h1 class="title flex w-full items-end text-left sm:block sm:text-white">
          <!-- Title -->
          <h1
            v-if="!IS_ELECTRON"
            class="hidden text-ellipsis sm:block sm:w-auto sm:flex-initial sm:pb-4 sm:text-3xl"
          >
            <span class="pt-1 sm:pt-0">{{ $t("str.leaderboard") }}</span>
            <h2 class="hidden text-base text-gray-300 sm:inline sm:pl-4">
              {{ $t("leaderboard.desc") }}
            </h2>
          </h1>

          <!-- Buttons -->
          <div class="flex h-[32px] w-fit justify-end gap-2">
            <button
              class="w-[60px] border-b-2 text-base"
              :class="{
                ' border-gold-400  text-white': activeRegionID == 0,
                'border-transparent text-gold-400': activeRegionID != 0,
              }"
              @click="switchRegion(regions.AM)"
            >
              {{ REGION_SHORTS[regions.AM] }}
            </button>
            <button
              class="w-[60px] border-b-2 text-base"
              :class="{
                ' border-gold-400  text-white': activeRegionID == 1,
                'border-transparent text-gold-400': activeRegionID != 1,
              }"
              @click="switchRegion(regions.EU)"
            >
              {{ REGION_SHORTS[regions.EU] }}
            </button>
            <button
              class="w-[60px] border-b-2 text-base"
              :class="{
                ' border-gold-400  text-white': activeRegionID == 2,
                'border-transparent text-gold-400': activeRegionID != 2,
              }"
              @click="switchRegion(regions.APAC)"
            >
              {{ REGION_SHORTS[regions.APAC] }}
            </button>
            <!-- <button id="btn-as" class="btn" :class="{active: activeRegionID == 2}" @click="switchRegion(regions.AS)">AS</button> -->
            <!-- <button id="btn-sea" class="btn" :class="{active: activeRegionID == 3}" @click="switchRegion(regions.SEA)">SEA</button> -->
          </div>
        </h1>

        <!-- Search bar -->
        <div class="">
          <div class="relative mt-4 h-12">
            <div
              class="search-icon left"
              v-if="!isLoading[this.activeRegionID]"
              @click="
                () => {
                  this.fetchLeaderboard(this.activeRegionID)
                }
              "
            >
              <i class="fa fa-trophy"></i>
            </div>
            <div class="search-icon left loading" v-if="isLoading[this.activeRegionID]">
              <i class="fa fa-circle-notch fa-spin"></i>
            </div>
            <input
              id="search-input"
              class="rounded-3xl bg-gray-800 placeholder-gray-300 transition-colors focus:bg-gray-700"
              spellcheck="false"
              autocomplete="off"
              v-model="searchText"
              @keyup="onKeyUp"
              @focus="onInputFocus"
              @blur="onInputBlur"
              type="text"
              :placeholder="isLoading[this.activeRegionID] ? $t('str.loading') : searchPlaceHolder"
              :disabled="isLoading[this.activeRegionID]"
              ref="leaderboardInput"
            />
            <div
              v-if="updateTime && updateTime[activeRegionID]"
              class="absolute top-[16px] right-12 pb-2 text-right text-xs text-gray-300 transition-colors hover:text-gray-100"
            >
              {{ $t("str.lastUpdated") }}
              {{
                formatDistanceStrict(new Date(updateTime[activeRegionID]), new Date(), {
                  addSuffix: true,
                  locale: dateFNSLocales[$i18n.locale],
                })
              }}
            </div>
            <div class="search-icon right" @click="clearSearch" v-if="searchText != ''">
              <span><i class="fas fa-times"></i></span>
            </div>
          </div>
        </div>

        <!-- Headers -->
        <div
          class="sticky top-0 z-[2] grid h-12 grid-cols-12 items-center whitespace-nowrap bg-gray-900 pt-1 text-sm"
        >
          <div class="bg-gray-900 sm:px-2">{{ $t("leaderboard.rank") }}</div>
          <div class="col-span-5 bg-gray-900 px-2 sm:col-span-3">
            {{ $t("leaderboard.name") }}
          </div>
          <div class="col-span-2 sm:col-span-1 sm:px-2">
            {{ $t("leaderboard.points") }}
          </div>
          <div class="hidden px-2 sm:col-span-2 sm:block">
            {{ $t("leaderboard.lastRank") }}
          </div>
          <!-- "$t('leaderboard.lastRankTip')" -->

          <div
            class="hidden px-2 sm:col-span-2 sm:block"
            v-tooltip="{ content: $t('leaderboard.lastRankTip') }"
          >
            {{ $t("leaderboard.lastX", { num: 20 }) }}
          </div>

          <div class="col-span-4 px-2 sm:col-span-3">
            {{ $t("leaderboard.recent") }}
          </div>
        </div>

        <RecycleScroller
          v-if="filteredPlayers"
          class="block h-0 w-full flex-1 overflow-y-auto rounded-md"
          :items="filteredPlayers"
          :item-size="64"
          key-field="rank"
          ref="scroller"
        >
          <template v-slot="{ item, index }"
            ><leaderboard-player
              @click="searchPlayer(item)"
              :rank="(item.rank + 1).toString()"
              :name="item.name"
              :lp="item.lp"
              :deck="item.deck_code"
              :winRate="item.game_latest_rank_win_rate"
              :lastRankTime="item.game_latest_rank_time"
              :selected="inputFocused && index == selectedIndex"
              :isSearch="searchText != '' && index == filteredPlayers.length - 1"
            >
            </leaderboard-player
          ></template>
        </RecycleScroller>
        <div v-else class="block h-0 w-full flex-1 rounded-md bg-gray-800"></div>
      </div>
    </div>
    <!-- Right -->
    <!-- <div class="hidden w-0 max-w-3xl flex-1 2xl:flex"></div> -->
  </div>
</template>

<script>
// const axios = require('axios')
// import axios from "axios"
import LeaderboardPlayer from "../leaderboard/LeaderboardPlayer.vue"
import { formatDistanceStrict } from "date-fns"
import { dateFNSLocales } from "../../assets/data/messages"

export const REGION_ID = {
  AM: 0,
  EU: 1,
  APAC: 2,
}
export const REGION_SHORTS = ["AM", "EU", "APAC"]
export const REGION_NAMES = ["americas", "europe", "apac"]

/**
 * Converts "amaricas" -> "AM", etc
 **/
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

import LadderHighlight from "../leaderboard/LadderHighlight.vue"

export default {
  components: { LeaderboardPlayer, LadderHighlight },
  mounted() {
    // this.getLeaderboard(this.activeRegionID)
    // console.log("Mounted Leaderboard")
    let oldRegion = window.localStorage.getItem(leaderboardStorageID)
    if (oldRegion) {
      this.activeRegionID = oldRegion
    }
    this.fetchLeaderboard(this.activeRegionID)

    setTimeout(() => {
      this.$refs.leaderboardInput.focus()
    }, 25)
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
      selectedIndex: 0,

      REGION_SHORTS,
      dateFNSLocales,

      inputFocused: false,
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
    ...mapState(useLeaderboardStore, {
      leaderboard: "leaderboard",
      isLoading: "leaderboardLoading",
      updateTime: "leaderboardUpdateTime",
    }),
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

        filteredPlayers.push({
          name: searchText,
          rank: "",
          lp: 0,
          deck: null,
          winRate: 0,
          lastRankTime: "",
        })

        return filteredPlayers // TODO implement better way to improve this performence
      }
      return this.leaderboard[this.activeRegionID]
    },

    searchPlaceHolder() {
      if (this.leaderboard && this.leaderboard[this.activeRegionID]) {
        return this.$t("search.leaderboard.numPlayer", {
          num: this.leaderboard[this.activeRegionID].length,
        })
      } else {
        return this.$t("search.leaderboard.base")
      }
    },
  },
  methods: {
    ...mapActions(useLeaderboardStore, ["fetchLeaderboard"]),
    formatDistanceStrict,
    selectTopItem() {
      const scroller = this.$refs.scroller
      const el = scroller.$el
      let currentTopItem = Math.ceil(el.scrollTop / 64)
      this.selectedIndex = currentTopItem
    },
    onInputFocus() {
      this.inputFocused = true
      this.selectTopItem()
    },
    onInputBlur() {
      this.inputFocused = false
    },
    setLeaderBoardPlayerRefs(el) {
      if (el) {
        // this.leaderboardPlayerRefs.push(el)
        console.log(el)
      }
    },
    onKeyUp(e) {
      const scroller = this.$refs.scroller
      const el = scroller.$el
      if (e.key == "ArrowDown") {
        this.selectedIndex += 1
        if (this.selectedIndex > this.filteredPlayers.length - 1) {
          this.selectedIndex = 0
          scroller.scrollToItem(0)
        } else {
          let minScrollTop = this.selectedIndex * 64 - el.getBoundingClientRect().height + 64 //min scrollTop to be visible
          if (el.scrollTop < minScrollTop) {
            this.$refs.scroller.scrollToPosition(minScrollTop)
          }
        }
      } else if (e.key == "ArrowUp") {
        this.selectedIndex -= 1
        if (this.selectedIndex < 0) {
          this.selectedIndex = this.filteredPlayers.length - 1
          this.$refs.scroller.scrollToItem(this.selectedIndex)
        } else {
          let maxScrollTop = this.selectedIndex * 64 //max scrollTop to be visible
          if (el.scrollTop > maxScrollTop) {
            this.$refs.scroller.scrollToItem(this.selectedIndex)
          }
        }
      } else if (e.key == "Enter") {
        let player = this.filteredPlayers[this.selectedIndex]
        this.searchPlayer(player)
      } else {
        if (this.filteredPlayers.length > 5) {
          this.selectTopItem()
        } else {
          this.selectedIndex = this.filteredPlayers.length - 1
        }
      }
    },
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
          query: {
            name: player.name,
            tag: player.tag,
            region: REGION_SHORTS[this.activeRegionID],
          },
        })
      } else {
        this.$router.push({
          name: "search",
          query: {
            name: player.name,
          },
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
