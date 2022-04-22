<template>
  <div class="flex h-full flex-col">
    <!-- Summary -->
    <div class="grid grid-cols-5 items-end pb-4 sm:grid-cols-5">
      <!-- Left -->
      <div class="col-span-3 px-2 sm:col-span-4 sm:px-0">
        <div class="player-name">
          {{ playerName }}
          <i
            v-if="playerName && playerTag && playerRegion"
            class="fas fa-bookmark hidden cursor-pointer pl-2 text-base hover:text-white lg:inline"
            :class="{
              'text-gray-200 ': bookmarkIndex == null || bookmarkIndex == -1,
              'text-gold-200': bookmarkIndex != null && bookmarkIndex != -1,
            }"
            @click="handleBookmarkClick"
          ></i>
        </div>
        <div class="flex items-center justify-start gap-4 pt-2 text-left sm:gap-6">
          <div v-if="rank">
            <div class="text-sm text-gray-300">
              <i class="fas fa-trophy"></i> {{ $t("leaderboard.rank") }}
            </div>
            <div class="text-lg">No. {{ rank }}</div>
          </div>

          <div v-if="lp">
            <div class="text-sm text-gray-300">
              <i class="fas fa-map-marker-alt"></i>
              {{ $t("leaderboard.points") }}
            </div>
            <div class="text-lg">
              {{ lp }}
            </div>
          </div>

          <div v-if="playerRegion">
            <div class="text-sm text-gray-300">
              <i
                class="fas"
                :class="{
                  'fa-globe-asia': playerRegion === 'APAC',
                  'fa-globe-europe': playerRegion === 'EU',
                  'fa-globe-americas': playerRegion === 'NA',
                }"
              ></i>
              {{ $t("str.server") }}
            </div>
            <div class="text-lg">
              {{ playerRegionFC }}
            </div>
          </div>

          <div v-if="games24hr" class="hidden sm:block">
            <div class="text-sm text-gray-300">
              {{ $t("matches.lastNumHour", { num: 24 }) }}
            </div>
            <div class="text-lg">
              {{ $t("matches.games", { num: games24hr }) }}
            </div>
          </div>
        </div>
      </div>
      <!-- Right -->
      <div class="col-span-2 px-2 pt-2 text-left sm:col-span-1 sm:p-0" v-if="winrate">
        <div class="text-sm text-gray-300">
          {{ $t("matches.games", { num: totalMatches }) }}
        </div>
        <div
          class="whitespace-nowrap text-2xl"
          :style="{
            color: winRateToColor(winrate),
          }"
        >
          {{ winrateString }} <span class="subtext">{{ $t("dash.winRate") }}</span>
        </div>
        <div class="text-sm text-gray-300" v-if="winloss">{{ winloss }}</div>
      </div>
    </div>

    <div class="no-content" v-if="totalMatches == 0">
      {{ $t("str.error.playerNoHistory") }}
    </div>

    <DynamicScroller
      :items="filteredMatches"
      :min-item-size="50"
      key-field="time"
      class="flex-1 overflow-y-auto"
    >
      <template v-slot="{ item, index, active }">
        <DynamicScrollerItem
          :item="item"
          :active="active"
          :size-dependencies="[item.winStreak, item.isDateBreak]"
          :data-index="index"
        >
          <match-history
            @search="
              searchPlayer({
                region: playerRegion,
                name: item.opponentName,
                tag: item.opponentTag,
              })
            "
            :opponentName="item.opponentName"
            :opponentRank="item.opponentRank"
            :opponentLp="item.opponentLp"
            :deck="item.deck"
            :opponentDeck="item.opponentDeck"
            :rounds="item.rounds"
            :win="item.win"
            :time="item.time"
            :badges="item.badges"
            :details="item.details"
            :region="playerRegion"
            :winStreak="item.winStreak"
            :isDateBreak="item.isDateBreak"
            :index="index"
          ></match-history>
        </DynamicScrollerItem>
      </template>
    </DynamicScroller>
  </div>
</template>

<script>
import MatchHistory from "../match/MatchHistory.vue"

import { REGION_ID, REGION_SHORTS, REGION_NAMES } from "../panels/PanelLeaderboard.vue"

import { winRateToColor } from "../../modules/utils/colorUtils"

// Some helper math functions
function FLip(x) {
  return 1 - x
}
function Square(x) {
  return x * x
}
function EaseOut(x) {
  return FLip(Square(FLip(x)))
}
function Clamp(x, min, max) {
  return Math.min(Math.max(x, min), max)
}

function filterUnique(value, index, self) {
  return self.indexOf(value) === index
}

const frequencies = (arr) =>
  arr.reduce((a, v) => {
    a[v] = a[v] ? a[v] + 1 : 1
    return a
  }, {})

function firstCap(string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

import { useLeaderboardStore } from "../../store/StoreLeaderboard"
import { mapStores } from "pinia"

import { useBookmarkStore } from "../../store/StoreBookmark"

export const getLeaderboardFromPlayer = (regionShort, name, tag) => {
  if (!(regionShort && name && tag)) return null
  const leaderboardStore = useLeaderboardStore()
  const lead = leaderboardStore.leaderboard
  if (lead && lead[REGION_ID[regionShort]]) {
    return lead[REGION_ID[regionShort]].find((val) => {
      return val.name == name && val.tag == tag
    })
  } else {
    leaderboardStore.fetchLeaderboard(REGION_ID[regionShort])
  }
  return null
}

export default {
  components: {
    MatchHistory,
  },
  mounted() {
    if (!this.leaderboardStore && !this.leaderboardStore[REGION_ID[this.playerRegion]]) {
      this.leaderboardStore.fetchLeaderboard(REGION_ID[this.playerRegion])
    }
  },
  props: {
    playerName: String,
    playerTag: String,
    playerRegion: String, // region shorts
    matches: Array,
    filter: String,
  },
  data() {
    return {
      filterDeckCode: null,
    }
  },
  computed: {
    ...mapStores(useLeaderboardStore, useBookmarkStore),

    bookmarkIndex() {
      return this.bookmarkStore?.bookmarks?.findIndex(
        (bookmark) => this.playerName == bookmark.name && this.playerTag == bookmark.tag
      )
    },

    leaderboard() {
      return getLeaderboardFromPlayer(this.playerRegion, this.playerName, this.playerTag)
    },

    lp() {
      if (this.playerLP) {
        return this.playerLP
      } else {
        if (this.leaderboard) {
          return this.leaderboard.lp
        }
      }
      return null
    },

    rank() {
      if (this.playerRank) {
        return this.playerRank
      } else {
        if (this.leaderboard) {
          return this.leaderboard.rank + 1 // Because raw rank data starts at 0
        }
      }
      return null
    },

    playerRegionFC() {
      return this.$t("str.regions." + REGION_NAMES[REGION_ID[this.playerRegion]])
    },

    uniqueDeckCodes() {
      if (!this.matches) return null
      var decks = this.matches.map((x) => x.deck)
      var decks_freq = decks.reduce((a, v) => {
        a[v] = a[v] ? a[v] + 1 : 1
        return a
      }, {})
      var decks_freq_array = []
      Object.keys(decks_freq).map(function (key, index) {
        decks_freq_array[index] = { deck: key, num: decks_freq[key] }
      })

      decks_freq_array.sort((a, b) => b.num - a.num)
      // Large num in front

      return decks_freq_array
    },
    filteredMatches() {
      if (!this.matches) return null
      if (!this.filterDeckCode) {
        var winStreak = 0
        var days = 1
        return this.matches
          .filter((n) => n)
          .map((val, index, array) => {
            // Loading in Rank from Leaderboard
            if (
              (!val.opponentRank || val.opponentRank == "") &&
              val.opponentName &&
              val.opponentTag &&
              val.region
            ) {
              const lead = this.leaderboardStore.leaderboard
              if (lead && lead[REGION_ID[val.region]]) {
                let leadItem = lead[REGION_ID[val.region]].find((boardItem) => {
                  return boardItem.name == val.opponentName && boardItem.tag == val.opponentTag
                })
                if (leadItem) {
                  val.opponentRank = (leadItem.rank + 1).toString()
                }
              }
            }

            val.isDateBreak = false
            val.winStreak = 0

            if (val.win) {
              winStreak += 1
            } else {
              if (winStreak >= 5) array[index - winStreak].winStreak = winStreak
              winStreak = 0
            }

            var date = new Date(val.time)
            var daysElapsed = (Date.now() - date) / 1000 / 60 / 60 / 24

            if (daysElapsed >= days) {
              val.isDateBreak = true
              days = Math.ceil(daysElapsed)
            }

            return val
          }) // filters out null decks
      }
      return this.matches.filter((x) => x.deck == this.filterDeckCode && x.time) // filters according to deck code & check to make sure time is set
    },
    totalWins() {
      if (!this.filteredMatches) return null
      return this.filteredMatches.reduce((total, match) => (match.win ? total + 1 : total), 0) // adds up all the wins
    },
    games24hr() {
      if (!this.matches) return 0
      return this.matches.reduce((total, match) => {
        var date = new Date(match.time)
        var daysElapsed = (Date.now() - date) / 1000 / 60 / 60 / 24
        return daysElapsed < 1 ? total + 1 : total
      }, 0)
    },
    totalMatches() {
      return this.filteredMatches.length
    },
    winloss() {
      if (this.totalMatches == 0) return null
      var loss = this.totalMatches - this.totalWins
      return this.$t("dash.winloss", { win: this.totalWins, loss: loss })
    },
    winrate() {
      if (this.totalMatches == 0) return null
      return this.totalWins / this.totalMatches
    },
    winrateString() {
      if (this.totalMatches == 0) return null
      return (this.winrate * 100).toFixed(1) + "%"
    },
  },
  methods: {
    winRateToColor,
    handleBookmarkClick() {
      if (this.bookmarkIndex != null && this.bookmarkIndex != -1) {
        this.bookmarkStore.deleteBookmark(this.bookmarkIndex)
      } else {
        this.bookmarkStore.addBookmark({
          name: this.playerName,
          tag: this.playerTag,
          region: this.playerRegion,
        })
      }
    },
    downloadStreakScreenshot(index) {
      // html2canvas(this.$el).then(function (canvas) {
      //   document.body.appendChild(canvas)
      // })
    },
    // Helpers
    animateScroll(el, distance, duration) {
      var scrollAmount = 0
      var start, prePos

      function step(timestamp) {
        if (start === undefined) {
          start = timestamp
          prePos = 0
        }
        const elapsed = timestamp - start
        var newPos = distance * EaseOut(Clamp(elapsed / duration, 0, 1))

        el.scrollLeft += newPos - prePos
        prePos = newPos

        if (elapsed < duration) {
          // Stop the animation after 2 seconds
          window.requestAnimationFrame(step)
        }
      }

      window.requestAnimationFrame(step)
    },
    horizontalScroll(event) {
      var el = event.currentTarget

      if (event.deltaY > 0) {
        this.animateScroll(el, 100, 300)
      } else {
        this.animateScroll(el, -100, 300)
      }
    },

    // Filter related
    setFilterDeckCode(code) {
      if (this.filterDeckCode == code) {
        // If trying to set the same, clear the filter
        this.filterDeckCode = null
      } else {
        this.filterDeckCode = code
      }

      this.sendUserEvent({
        category: "Main Window Matches",
        action: this.filterDeckCode ? "Set Filter Deck Code" : "Remove Filter Deck Code",
        label: code,
        value: null,
      })
    },

    searchPlayer(data) {
      if (data.tag) {
        // Only player with tag can be clicked=
        this.$router.push({
          name: "search",
          query: { name: data.name, tag: data.tag, region: data.region },
        })
      }
    },
  },
}
</script>

<style lang="scss">
.player-name {
  font-size: 24px;
  padding-top: 15px;
  text-align: left;
}

.no-content {
  font-size: 20px;
}

.summary-container {
  padding: 5px 0px 15px 0px;
  gap: 10px;
  justify-content: space-between;
  align-items: center;
}

.match-history-container {
  /* height: calc(100vh - 325px); */
  /* overflow-y: scroll; */
  margin-bottom: 25px;
}

.player-summary {
  text-align: left;
  width: 20%;
}

.player-summary .name {
  font-size: 24px;
  margin-bottom: 5px;
}

.player-summary .detail {
  font-size: 12px;
  color: var(--col-lighter-grey);
}

.player-summary .detail .pre-info {
  display: inline-block;
  width: 20px;
  border-right: 1px solid var(--col-lighter-grey);
}

.player-summary:hover .detail {
  color: var(--col-dark-white);
}

.player-summary:hover .detail.rank {
  color: white;
}

.iconfy {
  font-size: 0.9em;
  font-weight: 900;
}

.decks-summary {
  display: block;
  overflow-x: auto;
  white-space: nowrap;
  width: 55%;
  text-align: left;

  padding-bottom: 5px;
}

.decks-summary .champion-icons {
  display: inline-flex;
  padding: 5px;
  border-radius: 50px;
  margin: 0px 2px;
  cursor: pointer;
}

.decks-summary .champion-icons:hover {
  background: var(--col-dark-grey);
}

.decks-summary .champion-icons.active {
  background: var(--col-light-grey);
}

.history-summary {
  font-size: 24px;
  /* margin-left: 20px; */
  text-align: right;
  width: 22%;
}

.history-summary .winrate {
  font-size: 24px;
  color: white;
  /* color: var(--col-lighter-grey); */
}

.history-summary .winrate .subtext {
  font-size: 0.75em;
  color: white;
}

.history-summary .winloss {
  font-size: 18px;
  color: var(--col-lighter-grey);
}

.history-summary:hover .winloss {
  color: var(--col-dark-white);
}

.sticky-top {
  position: sticky;
  top: 0;
  background: var(--col-background);
  z-index: 1;
}

.main-content-container.search .sticky-top {
  position: sticky;
  top: 102px;
  background: var(--col-background);

  &.search {
    top: 0px;
    padding-bottom: 5px;
    z-index: 3;
  }
}
</style>
