<template>
  <div class="flex h-full justify-center gap-6">
    <div class="hidden max-w-[350px] flex-1 flex-col lg:flex">
      <!-- Bookmarked Players -->
      <div class="pb-3 text-center text-lg">
        {{ $t("search.bookmarks").toUpperCase() }}
      </div>
      <div
        class="mb-4 flex max-h-[25%] min-h-[40px] flex-shrink flex-col gap-1 overflow-y-auto rounded-lg bg-gray-800"
      >
        <i18n-t
          keypath="search.noBookmarks"
          tag="div"
          class="py-2 text-gray-200"
          v-if="!bookmarks || bookmarks.length <= 0"
        >
          <i class="fas fa-bookmark px-1"></i>
        </i18n-t>
        <div v-if="bookmarks && bookmarks.length > 0">
          <draggable
            v-model="bookmarks"
            group="people"
            @start="bookmarkDragStart"
            @end="bookmarkDragEnd"
            item-key="id"
          >
            <template #item="{ element, index }">
              <search-bookmark :bookmark="element" :index="index"></search-bookmark>
            </template>
          </draggable>
          <!-- <div v-for="(bookmark, index) in bookmarks" :key="bookmark.name + bookmark.id">
            <search-bookmark :bookmark="bookmark" :index="index"></search-bookmark>
          </div> -->
        </div>
      </div>
      <!-- Filters -->
      <div
        v-if="playerName && matches.length > 0"
        class="flex flex-shrink-[2] flex-col overflow-y-auto"
      >
        <div class="pb-2 text-center text-lg">
          {{ $t("str.filter").toUpperCase() }}
        </div>
        <!-- Game Types -->
        <div class="pb-2 pl-1 text-left text-sm text-gray-300">
          <i class="fas fa-chess pr-1"></i>
          {{ $t("str.gameType") }}
        </div>
        <div class="flex flex-wrap gap-2 pb-4">
          <div
            v-for="(value, key) in uniqueBadges"
            :key="value"
            @click="setFilterBadge(key)"
            class="cursor-pointer whitespace-nowrap rounded-full px-2 py-1 text-sm transition-colors hover:bg-gray-600 hover:text-white"
            :class="{
              'bg-gray-700 text-gray-100': this.filterBadge == key,
              'bg-gray-800 text-gray-200': this.filterBadge != key,
            }"
          >
            {{ $t(getBadgeTranslateKey(key)) }} <span class="rounded-full px-1">{{ value }}</span>
          </div>
        </div>
        <!-- Archetypes -->
        <div class="pb-2 pl-1 text-left text-sm text-gray-300">
          <i class="fas fa-book-alt pr-1"></i>
          {{ $t("str.archetypes") }}
        </div>
        <div class="mb-4 flex flex-shrink flex-col gap-1 overflow-y-auto rounded-lg bg-gray-800">
          <div
            class="rounded transition-colors hover:bg-gray-600"
            v-for="obj in uniqueArchetypes"
            :key="obj.id"
            :class="{ 'bg-gray-700': filterDeckID == obj.id }"
          >
            <div class="flex items-center">
              <div>
                <deck-preview
                  class="mx-2 gap-1 py-1.5 px-2 text-xs transition-colors hover:bg-gray-800"
                  :deck="obj.decks[0]"
                ></deck-preview>
              </div>
              <!-- Archetype Filters (Button) -->
              <div
                class="group flex w-0 flex-1 cursor-pointer py-1.5 pl-1"
                @click="setFilterArchetype(obj.id)"
              >
                <div class="w-0 flex-1 text-left">
                  <div class="text-sm text-gray-300 group-hover:text-gray-150">
                    {{ $t("matches.games", { num: obj.freq }) }}
                  </div>
                  <div
                    class="overflow-hidden text-ellipsis whitespace-nowrap"
                    :style="{
                      color: winRateToColor(obj.win / obj.freq),
                    }"
                  >
                    {{
                      $t("matches.winRate", {
                        num: Math.floor((obj.win / obj.freq) * 1000) / 10,
                      })
                    }}
                  </div>
                </div>
                <div
                  class="flex cursor-pointer items-center px-2 pr-4 text-gray-200 transition-opacity group-hover:opacity-100"
                  :class="{
                    'opacity-0': filterDeckID != obj.id,
                    'text-gray-50': filterDeckID == obj.id,
                  }"
                >
                  <i class="fas fa-filter"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="min-h-[72px]"></div>
    </div>
    <div class="w-0 max-w-2xl flex-1">
      <div class="flex h-full flex-col px-2 sm:px-0">
        <!-- Search Input -->
        <div class="z-[5]">
          <div class="region-tabs">
            <div
              class="region-option"
              :class="{ selected: selectedRegion == null }"
              @click="selectRegion(null)"
            >
              ALL
            </div>
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
          <div class="width-full relative mt-4 flex flex-nowrap">
            <div class="search-bar-input-container">
              <button
                class="search-btn inside left"
                :class="{ active: searchText != '' }"
                @click="searchHistory"
              >
                <span v-if="isLoading || isUpdating"
                  ><i class="fas fa-redo-alt fa-spin-fast"></i
                ></span>
                <span v-else-if="searchText != playerName || !playerName"
                  ><i class="fas fa-search"></i
                ></span>
                <span v-else-if="!isUpdated || isError"><i class="fas fa-redo-alt"></i></span>
                <span v-else><i class="fas fa-check"></i></span>
              </button>

              <input
                spellcheck="false"
                autocomplete="off"
                class="search-bar h-12 w-full rounded-3xl border-none bg-gray-800 pl-12 pr-5 text-base text-white placeholder-gray-300 outline-none transition-colors focus:bg-gray-700"
                :class="{
                  'rounded-b-none rounded-t-[25px]': showAutoCompleteBar,
                }"
                @keyup="onKeyUp"
                @keyup.enter="searchHistory"
                @keyup.up="autoCompleteIndexMinus"
                @keyup.down="autoCompleteIndexPlus"
                @keydown="onKeyDown"
                @focus="onInputFocus"
                @blur="onInputBlur"
                v-model="searchText"
                :placeholder="$t('search.player.placeholder')"
              />
              <button class="search-btn inside right" @click="clearSearch" v-if="searchText != ''">
                <span><i class="fas fa-times"></i></span>
              </button>
            </div>
            <!-- Auto Complete -->
            <div
              v-if="showAutoCompleteBar"
              class="absolute top-12 z-10 w-full rounded-b-[25px] bg-gray-800 pb-3 text-left"
            >
              <div class="max-h-[calc(80vh-140px)] overflow-y-auto" v-if="hasNameAutoComplete">
                <div
                  class="cursor-pointer py-2 pr-2 pl-12 hover:bg-gray-600"
                  v-for="(player, index) in filteredInputNameList"
                  :key="index"
                  :class="{ 'bg-gray-700': autoCompleteIndex == index }"
                  @mousedown="searchHistoryAutoComplete(index)"
                  :ref="setAutoCompleteRefs"
                >
                  <search-auto-complete-item
                    :selectedRegion="selectedRegion"
                    :player="player"
                  ></search-auto-complete-item>
                </div>
              </div>
              <div class="pl-12 pt-2 text-gray-200">
                <span v-if="autoCompleteLoading">{{ $t("str.loading") }}</span>
                <span
                  v-else-if="
                    !hasNameAutoComplete && searchText.length > 3 && !(searchText == playerName)
                  "
                >
                  {{ $t("search.noSuggestion") }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="playerName && matches.length > 0" class="h-0 flex-1">
          <!-- Player Info -->
          <player-matches
            v-if="playerName && matches.length > 0"
            :playerName="playerName"
            :playerRegion="playerRegion"
            :playerTag="playerTag"
            :matches="filteredMatches"
          >
          </player-matches>
        </div>

        <div class="my-4 text-2xl" v-if="isLoading || isUpdating || isError || matches.length <= 0">
          <span v-if="!(isLoading || isUpdating) && !isError && matches.length <= 0">
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
          <span v-if="isError && !isUpdating">
            <!-- <i class="fas fa-circle-notch fa-spin"></i> -->
            {{ errorText }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const requestHistoryWaitTime = 100 //ms

let cancelToken, localCancleToken
var lastStatusRequestTime
var requestHistoryTimeout, prevHistoryRequest

import { regionNames, regionRefID } from "./PanelDeckCode.vue"

import { REGION_ID, REGION_SHORTS, REGION_NAMES, regionNameToShorts } from "./PanelLeaderboard.vue"

import DeckEncoder from "../../modules/runeterra/DeckEncoder"
import { championCards } from "../../assets/data/champion"

import PlayerMatches from "../match/PlayerMatches.vue"
import axios from "axios"
import DeckPreview from "../deck/DeckPreview.vue"

import { winRateToColor } from "../../modules/utils/colorUtils"

import { mapState, mapActions, mapWritableState } from "pinia"
import { useBookmarkStore } from "../../store/StoreBookmark"
import SearchBookmark from "../search/SearchBookmark.vue"
import SearchAutoCompleteItem from "../search/SearchAutoCompleteItem.vue"

import draggable from "vuedraggable"

import { getDeckID } from "./PanelMeta.vue"
import { filterBadges, getBadgeTranslateKey } from "../match/MatchHistory.vue"

export const processSearchRequestRawData = (raw) => {
  // playerServer is region shorts

  var matches = []
  if (!raw) return matches

  let data = raw.matches

  if (!data || data.length <= 0) return matches

  let puuid = raw.player._id

  // Processing for normal Data
  for (var match of data) {
    // var match = data[key]
    var info = match.info
    var playersInfo = match.player_info

    if (
      !match ||
      !playersInfo ||
      !playersInfo[0] ||
      !playersInfo[0].name ||
      !info.players ||
      !info.players[0] ||
      !info.players[0].puuid
    )
      continue // Skip if null history

    // var isFirstPlayer = playersInfo[0].name.toLowerCase() == playerName.toLowerCase()
    var isFirstPlayer = info.players[0].puuid == puuid
    var player, playerGame, opponent, opponentGame

    var details = null

    // Process local info
    if (match.local && match.local.deck_tracker) {
      details = {
        openHand: match.local.deck_tracker.openHand,
        replacedHand: match.local.deck_tracker.replacedHand,
        timeline: match.local.deck_tracker.timeline,
        startTime: match.local.startTime,
        endTime: match.local.endTime,
      }
    }

    // Because the info orders are not confirmed
    if (isFirstPlayer) {
      playerGame = info.players[0] // Players Game Information
      opponentGame = info.players[1] // Opponents Game Information
      player = playersInfo[0]
      opponent = playersInfo[1]
    } else {
      playerGame = info.players[1]
      opponentGame = info.players[0]
      player = playersInfo[1]
      opponent = playersInfo[0]
    }

    // Skip if info not complete
    if (!playerGame || !opponentGame || !player || !opponent) continue

    var badges = []
    if (info.game_mode)
      badges.push(
        info.game_mode
          .replace(/([A-Z])/g, "$1")
          .trim()
          .replace("Lobby", "")
      )
    if (info.game_type)
      badges.push(
        info.game_type
          .replace(/([A-Z])/g, "$1")
          .trim()
          .replace("Lobby", "")
      )

    //"game_version": "live_3_01_12",
    var version = info.game_version.replace("live_", "").replace("_0", ".").replace("_", ".")

    matches.push({
      opponentName: opponent.name,
      opponentTag: opponent.tag,
      opponentDeck: opponentGame.deck_code,
      deck: playerGame.deck_code,
      rounds: info.total_turn_count,
      win: playerGame.game_outcome == "win",
      time: info.game_start_time_utc,
      badges: badges,
      details: details,
      order: playerGame.order_of_play,
      version: version,
    })
  }

  return matches
}

/** Returns "americas", etc */
export const extraRegionData = (data) => {
  if (data && data.player && data.player.server) {
    return data.player.server
  }
  return null
}

export default {
  components: {
    PlayerMatches,
    DeckPreview,
    SearchBookmark,
    SearchAutoCompleteItem,
    draggable,
  },
  props: {
    player: String,
    region: String,
    tag: String,
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
      autoCompleteIndex: 0,
      isInputFocused: false,
      autoCompleteRefs: [],
      autoCompleteRequestController: null,
      autoCompleteLoading: false,

      regions: REGION_SHORTS,
      selectedRegion: null,

      // Options
      autoLaunch: null,
      debugInfos: "",

      filterDeckID: null,
      filterBadge: null,

      drag: false,
    }
  },
  computed: {
    ...mapWritableState(useBookmarkStore, ["bookmarks"]),
    showAutoCompleteBar() {
      return (
        (this.autoCompleteLoading ||
          this.hasNameAutoComplete ||
          (this.searchText.length > 3 && !(this.searchText == this.playerName))) &&
        this.isInputFocused
      )
    },
    hasNameAutoComplete() {
      return this.filteredInputNameList && this.filteredInputNameList.length > 0
    },

    filteredMatches() {
      if (!this.matches) return null
      var filtered = this.matches
      if (this.filterDeckID) {
        filtered = filtered.filter((val) => {
          return getDeckID(val.deck) == this.filterDeckID
        })
      }

      if (this.filterBadge) {
        filtered = filtered.filter((val) => {
          return val.badges.includes(this.filterBadge)
        })
      }

      return filtered
    },
    hasSearchInfo() {
      return this.player && this.tag
    },
    uniqueBadges() {
      if (!this.matches) return null

      const badgesCount = {}

      for (const match of this.matches) {
        var filtered = filterBadges(match.badges)
        for (const badge of filtered) {
          badgesCount[badge] = badgesCount[badge] ? badgesCount[badge] + 1 : 1
        }
      }

      return Object.keys(badgesCount)
        .sort()
        .reduce(function (result, key) {
          result[key] = badgesCount[key]
          return result
        }, {})
    },
    uniqueArchetypes() {
      if (!this.matches) return null
      var decks = this.matches.map((x) => ({
        code: x.deck,
        id: getDeckID(x.deck),
        win: x.win,
      }))
      var decks_freq = decks.reduce((a, x) => {
        var v = x.id
        if (v && a[v]) {
          a[v].freq = a[v].freq + 1
          a[v].win += x.win ? 1 : 0
          if (!a[v].decks.includes(x.code)) {
            a[v].decks.push(x.code)
          }
        } else {
          var decks = []
          decks.push(x.code)
          a[v] = {
            freq: 1,
            decks: decks,
            win: x.win ? 1 : 0,
          }
        }
        return a
      }, {})
      var decks_freq_array = []
      Object.keys(decks_freq).map(function (key, index) {
        var item = decks_freq[key]
        decks_freq_array[index] = {
          id: key,
          decks: item.decks,
          freq: item.freq,
          win: item.win,
        }
      })

      decks_freq_array.sort((a, b) => (b.win / b.freq > a.win / a.freq ? 1 : -1))
      // Large num in front

      return decks_freq_array
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
    errorText() {
      var error = this.errorType
      if (error == 0 || error == 3) {
        return this.$t("str.error.playerNotFound")
      } else if (error == 1 || error == 2) {
        return this.$t("str.error.playerNoHistory")
      } else if (error == 4) {
        return this.$t("str.error.internalServiceError")
      } else {
        return this.$t("str.error.unkown")
      }
    },
    isUpdatedVersion() {
      return this.version == this.remoteVersion
    },
    filteredInputNameList() {
      // return this.inputNameList.map((i) => i.split("#")[0])
      return this.inputNameList
    },
    hasLocalInfo() {
      return this.localMatches && this.localMatches.length > 0
    },
    versionText() {
      if (this.updateDownloaded) {
        return "Restart"
      }
      return this.version
    },
    versionTooltip() {
      if (this.isUpdatedVersion) {
        return "Updated"
      } else if (this.updateDownloaded) {
        return "Update on next start"
      } else if (this.updateProcess > 0) {
        return `Downloading... ${this.updateProcess}%`
      } else if (this.remoteVersion) {
        return `Latest: ${this.remoteVersion}`
      }
      return this.$t("str.loading")
    },
  },
  mounted() {
    if (this.hasSearchInfo) {
      this.searchPlayer({
        name: this.player,
        region: this.region,
        tag: this.tag,
      })
    } else if (this.player) {
      this.searchText = this.player
      this.searchName()
      this.focusSearchBar()
    } else {
      this.focusSearchBar()
    }
    this.initStore()
  },
  methods: {
    ...mapActions(useBookmarkStore, ["initStore", "updateStore"]),

    bookmarkDragStart() {
      this.drag = true
    },

    bookmarkDragEnd() {
      this.drag = true
      this.updateStore()
    },

    getBadgeTranslateKey,
    winRateToColor,
    focusSearchBar() {
      var searchBar = document.querySelector(".search-bar")
      if (searchBar) searchBar.focus()
    },
    blurSearchBar() {
      var searchBar = document.querySelector(".search-bar")
      if (searchBar) searchBar.blur()
    },
    showDeck(code) {
      this.$emitter.emit("showDeck", code)
    },
    setFilterBadge(badge) {
      if (this.filterBadge == badge) {
        this.filterBadge = null
      } else {
        this.filterBadge = badge
      }
    },
    setFilterArchetype(deckID) {
      if (this.filterDeckID == deckID) {
        this.filterDeckID = null
      } else {
        this.filterDeckID = deckID
      }
    },
    selectRegion(region) {
      // region is region short
      this.sendUserEvent({
        category: "Main Window Search",
        action: "Select Region",
        label: REGION_NAMES[REGION_ID[region]],
        value: null,
      })

      this.selectedRegion = region
      this.focusSearchBar()

      this.searchName()
    },
    searchPlayer(data) {
      // data.region is region short
      this.searchText = data.name
      this.selectedRegion = data.region
      this.resetInputFocus()

      this.playerName = data.name
      this.playerTag = data.tag
      this.requestHistoryData()
    },
    // Search bar
    clearSearch() {
      this.searchText = ""
      this.resetAutoComplete()
      document.querySelector(".search-bar").focus()
    },
    onInputFocus() {
      this.isInputFocused = true
    },
    onInputBlur() {
      this.isInputFocused = false
    },
    searchName() {
      if (this.searchText.length > 0 && !this.searchText.includes("#")) {
        this.requestAutoComplete()
      } else {
        this.resetAutoComplete()
      }
    },
    resetAutoComplete() {
      this.inputNameList = []
      this.autoCompleteIndex = 0
    },
    resetInputFocus() {
      var searchBar = document.querySelector(".search-bar")
      if (searchBar) searchBar.blur()
      this.resetAutoComplete()
    },
    // Search bar Auto Complete
    setAutoCompleteRefs(el) {
      if (el) {
        this.autoCompleteRefs.push(el)
      }
    },
    autoCompleteIndexPlus() {
      this.autoCompleteIndex += 1
      if (this.autoCompleteIndex > this.inputNameList.length - 1) {
        this.autoCompleteIndex = 0
      }
      this.autoCompleteRefs[this.autoCompleteIndex].scrollIntoViewIfNeeded({
        behavior: "smooth",
      })
    },
    autoCompleteIndexMinus() {
      this.autoCompleteIndex -= 1
      if (this.autoCompleteIndex < 0) {
        this.autoCompleteIndex = this.inputNameList.length - 1
      }
      this.autoCompleteRefs[this.autoCompleteIndex].scrollIntoViewIfNeeded({
        behavior: "smooth",
      })
    },
    onKeyUp(e) {
      if (e.key != "ArrowUp" && e.key != "ArrowDown") {
        this.searchName()
      }
    },
    onKeyDown(e) {
      if (e.key == "ArrowUp" || e.key == "ArrowDown") {
        e.preventDefault()
      }
    },
    searchHistoryAutoComplete(index) {
      // console.log("searchHistoryAutoComplete")
      this.autoCompleteIndex = index
      this.searchHistory()
    },
    searchHistory() {
      var splited
      if (this.inputNameList.length > 0 && this.inputNameList[this.autoCompleteIndex]) {
        // Use auto complete to fill the search
        // Sets player info for search

        var item = this.inputNameList[this.autoCompleteIndex]

        var region = regionNameToShorts(item.server)

        if (
          this.playerName == item.name &&
          this.playerTag == item.tag &&
          this.playerRegion == region
        ) {
          this.searchText = item.name
          this.blurSearchBar()
        } else {
          this.$router.push({
            name: "search",
            query: { name: item.name, tag: item.tag, region: region },
          })
        }
      } else {
        // Use user input
        splited = this.searchText.split("#")
        if (splited.length == 2 && splited[0].length > 0 && splited[1].length > 0) {
          // Check if format is correct
          // Sets player info for search
          // this.playerName = splited[0]
          // this.playerTag = splited[1]

          this.$router.push({
            name: "search",
            query: { name: splited[0], tag: splited[1], region: this.selectedRegion },
          })
        } else if (splited.length == 1 && splited[0] == this.playerName && this.playerTag) {
          // When trying to search the same people, do a refresh (update only)

          if (this.isError) {
            // Unless it is error, in this case do a full refresh
            console.log("Refresh when error")
            this.requestHistoryData()
            this.resetInputFocus()
            return
          }

          console.log("Refresh & update only")
          this.requestHistoryUpdate()
          this.resetInputFocus()

          this.sendUserEvent({
            category: "Main Window Search",
            action: "User Input [Refresh]",
            label: `${this.searchText}`,
            value: null,
          })
        } else {
          // Alert the player needed info

          this.sendUserEvent({
            category: "Main Window Search",
            action: "User Input [Error]",
            label: `${this.searchText}`,
            value: null,
          })
        }
      }
    },
    clearInfo() {
      // this.playerName = "";
      // this.playerTag = "";
      this.playerRank = null
      this.playerLP = null
      this.playerRegion = null
      this.matches = []
    },
    errorHistory(error) {
      if (!this.isUpdating) {
        this.clearInfo()
      }
      this.isError = true
      this.errorType = error
      // this.playerName = "No history found"
    },
    openURL(url) {
      if (window.openExternal) {
        window.openExternal(url)
      } else {
        window.open(url)
      }
    },
    requestAutoComplete() {
      // Abort not completed requests
      if (this.autoCompleteRequestController) this.autoCompleteRequestController.abort()

      const api = this.selectedRegion
        ? `${this.API_WEB}/names/${REGION_NAMES[REGION_ID[this.selectedRegion]]}/${this.searchText}`
        : `${this.API_WEB}/names/${this.searchText}`
      const controller = new AbortController()
      this.autoCompleteRequestController = controller
      this.autoCompleteLoading = true

      axios
        .get(api, { signal: controller.signal })
        .then((response) => {
          this.autoCompleteLoading = false
          // console.log(response.data)
          if (document.querySelector(".search-bar") == document.activeElement && this.searchText) {
            // If the search bar is still in focus
            this.inputNameList = response.data
          } else {
            this.resetAutoComplete()
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            this.autoCompleteLoading = false
            console.log("error", e)
          }
        })
    },
    requestHistoryUpdate() {
      // Second request to makesure that the data is updated
      this.isUpdating = true
      this.isUpdated = false
      this.isError = false

      var newRequest = `${this.API_WEB}/match/${REGION_NAMES[REGION_ID[this.selectedRegion]]}/${
        this.playerName
      }/${this.playerTag}`

      // To record this activity
      this.sendUserEvent({
        category: "Main Window Requests",
        action: "Update Search",
        label: "URL: " + newRequest,
        value: null,
      })

      const requestUpdateHistoryStartTime = Date.now()

      cancelToken = axios.CancelToken.source()
      axios
        .get(newRequest, {
          headers: {
            is_update: 1,
          },
          cancelToken: cancelToken.token,
        })
        .then((response) => {
          this.isUpdating = false
          this.isUpdated = true

          this.sendUserEvent({
            category: "Main Window Requests",
            action: "Updated Search Result [Success]",
            label: "URL: " + newRequest,
            value: Date.now() - requestUpdateHistoryStartTime,
          })

          this.matches = processSearchRequestRawData(response.data)
          this.selectedRegion = regionNameToShorts(extraRegionData(response.data))
          this.playerRegion = REGION_SHORTS[REGION_ID[this.selectedRegion]]
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request (update) cancelled")
          } else {
            console.log(e)

            if (e.response) {
              if (e.response.data && e.response.data.status) console.log(e.response.data.status)

              if (e.response.status == 500) {
                this.errorHistory(4) // Internal server error
              } else {
                var data = e.response.data
                var errorCode = data.status && data.status.error
                if (errorCode == null) {
                  errorCode = 11 // give a 11 so that there is a fallback
                }
                this.errorHistory(errorCode) //
              }
            } else {
              this.errorHistory(11) // Unkown Error
            }
            this.isUpdating = false

            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Updated Search Result [Fail]",
              label: "Type: " + this.errorType + " | URL: " + newRequest,
              value: Date.now() - requestUpdateHistoryStartTime,
            })
          }
        })
    },
    requestHistoryData() {
      var newRequest = this.selectedRegion
        ? `${this.API_WEB}/match/${REGION_NAMES[REGION_ID[this.selectedRegion]]}/${
            this.playerName
          }/${this.playerTag}`
        : `${this.API_WEB}/match/${this.playerName}/${this.playerTag}`

      if (prevHistoryRequest == newRequest && this.isLoading) {
        // Don't refresh if the request is the same and ongoing
        return
      }

      //Check if there are any previous pending requests
      if (typeof cancelToken != typeof undefined) {
        cancelToken.cancel("Operation canceled due to new request.")
      }

      //Save the cancel token for the current request
      cancelToken = axios.CancelToken.source()

      this.isLoading = true
      this.isError = false
      this.isUpdated = false
      this.isUpdating = false
      this.playerRegion = REGION_SHORTS[REGION_ID[this.selectedRegion]]

      prevHistoryRequest = newRequest

      this.sendUserEvent({
        category: "Main Window Requests",
        action: "Request Search",
        label: "URL: " + newRequest,
        value: null,
      })

      const requestHistoryStartTime = Date.now()

      axios
        .get(newRequest, {
          cancelToken: cancelToken.token,
        }) // Pass the cancel token
        .then((response) => {
          this.isLoading = false

          this.sendUserEvent({
            category: "Main Window Requests",
            action: "Got Search Result [Success]",
            label: "URL: " + newRequest,
            value: Date.now() - requestHistoryStartTime,
          })

          // console.log(response.data)

          this.matches = processSearchRequestRawData(response.data)

          this.selectedRegion = regionNameToShorts(extraRegionData(response.data))
          this.playerRegion = REGION_SHORTS[REGION_ID[this.selectedRegion]]

          this.requestHistoryUpdate()
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)

            if (e.response) {
              if (e.response.data && e.response.data.status) console.log(e.response.data.status)
              if (e.response.status == 500) {
                this.errorHistory(4) // Internal server error
              } else {
                var data = e.response.data
                this.errorHistory((data.status && data.status.error) || 3) // give a 3 so that there is a fallback
              }
            } else {
              this.errorHistory(3) // Unkown Error
            }
            this.isLoading = false

            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Got Search Result [Fail]",
              label: "Type: " + this.errorType + " | URL: " + newRequest,
              value: Date.now() - requestHistoryStartTime,
            })

            this.requestHistoryUpdate() // Attempt to update in case of 404 or something else
          }
        })
    },
    getDeckID: getDeckID,
  },
}

// // Demo Data
// {
//   info: {
//     game_mode: "SeasonalTournamentLobby",
//     game_start_time_utc: "Sun, 06 Feb 2022 02:01:07 GMT",
//     game_type: "",
//     game_version: "live_3_01_12",
//     players: [
//       {
//         archetype: "faction_BandleCity_Name faction_ShadowIsles_Name Senna Veigar",
//         deck_code: "CQBQCAIFFABAKBIIBEDAKCRRHFOV4YVGAEBAEAIFAEOQEBIKAHIQCAQBAQCTQBABAUHRGFBO",
//         deck_id: "d67464e8-7b58-491e-83d3-0a764ed3a174_live_tour_deck_1",
//         factions: ["faction_BandleCity_Name", "faction_ShadowIsles_Name"],
//         game_outcome: "win",
//         order_of_play: 1,
//         puuid: "irldRzmkWeat7CWIAw5c_v-xwst8IV__BM5HEC6PvfMZxhX3cOR96Yvm1mTlWLPkvnR9WRDfQSgY5A",
//       },
//       {
//         archetype: "faction_Demacia_Name faction_MtTargon_Name Pantheon Shyvana",
//         deck_code: "CICQCAYJLQAQIAAOAIAQACI2AIBQACYOAICQSAYGAMAQEAABAECAAAQDAMEQGIZTAMAQGCKVAIAQADIPAMBQAAICAY",
//         deck_id: "d67464e8-7b58-491e-83d3-0a764ed3a174_live_tour_deck_2",
//         factions: ["faction_Demacia_Name", "faction_MtTargon_Name"],
//         game_outcome: "loss",
//         order_of_play: 0,
//         puuid: "aL1HBeYrs2AC3Axu83sUGTDfj0Khd_u5RbK7YMl_kmxk8U0ZCxj4iyQWXpjVfAQk5mPtBX0Neqz_Qg",
//       },
//     ],
//     total_turn_count: 60,
//   },
//   player_info: [
//     {
//       name: "nobody",
//       tag: "5547",
//     },
//     {
//       name: "Kevor24",
//       tag: "NA1",
//     },
//   ],
//   server: "americas",
// }
</script>
