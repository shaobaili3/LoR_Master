<template>
  <div>
    <div class="mb-1.5 flex w-full flex-col rounded-md bg-gray-800 px-2 py-1 2xs:mb-2">
      <!-- WinRate -->
      <div
        class="flex items-baseline gap-1.5 text-sm 2xs:gap-2 2xs:text-base"
        :style="{ color: winRateColor }"
      >
        <!-- {{matches}} / {{total}} -->
        <div>{{ $t("matches.winRate", { num: (winRate * 100).toFixed(0) }) }}</div>

        <!-- History Tooltip -->
        <tooltip :placement="'bottom'" :allowedPlacements="['bottom']">
          <div class="text-gray-200"><i class="fas fa-grip-horizontal"></i></div>
          <template #float="props">
            <div
              class="pointer-events-none z-10 w-full px-2 transition-opacity"
              :class="{
                'opacity-0': !props.visible,
                'opacity-100': props.visible,
              }"
            >
              <div class="bg-gray-800">
                <!-- Title -->
                <div class="2cs:text-sm pt-1 pl-1 text-xs text-gray-200">
                  <i class="fas fa-history pr-1"></i>{{ $t("str.history") }}
                </div>
                <div class="flex flex-wrap gap-x-1 gap-y-1.5 px-1 pb-2 pt-2">
                  <div v-for="(char, index) in history.split('')" :key="index">
                    <div
                      class="h-2 w-2 rounded 2xs:h-3 2xs:w-3"
                      :class="{
                        'bg-gray-500': char == 'E',
                        'bg-red-500': char == 'L',
                        'bg-sky-400': char == 'W',
                      }"
                      :style="{
                        opacity: 1 - (0.7 * index) / total,
                      }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </tooltip>
      </div>

      <!-- History -->
      <div class="flex flex-wrap gap-x-1 gap-y-1.5 px-1 pb-2 pt-2">
        <div v-for="(char, index) in history.split('').slice(0, 10)" :key="index">
          <div
            class="h-2 w-2 rounded 2xs:h-3 2xs:w-3"
            :class="{
              'bg-gray-500': char == 'E',
              'bg-red-500': char == 'L',
              'bg-sky-400': char == 'W',
            }"
            :style="{
              opacity: 1 - (0.7 * index) / 10, //total
            }"
          ></div>
        </div>
      </div>

      <!-- Number of Games -->
      <div
        class="flex items-baseline gap-x-1.5 whitespace-nowrap pb-1 text-xs text-gray-200 2xs:text-sm"
      >
        <div class="">{{ gamesString }}</div>
        <div class="">{{ timeString }}</div>
        <!-- <div class="">{{ wonNum }} W - {{ lostNum }} L</div> -->
      </div>

      <!-- Preview Button -->
      <div class="w-full">
        <deck-preview
          @click="showDeck"
          :clickToShow="false"
          class="w-full gap-0.5 py-1 text-xs hover:bg-white/10 2xs:gap-1 2xs:py-1.5 2xs:text-sm"
          :deck="deck"
        ></deck-preview>
        <!-- <div class="text-vs">VS</div> -->
        <!-- <deck-preview @click="showDeck" :deck="deck"></deck-preview> -->
      </div>
    </div>

    <transition name="height">
      <deck-detail v-if="expanded" :baseDeck="deck" :hideNum="true"></deck-detail>
    </transition>
  </div>
</template>

<script>
import DeckDetail from "../deck/DeckDetail.vue"
import DeckPreview from "../deck/DeckPreview.vue"

import { winRateToColor } from "../../modules/utils/colorUtils"
import Tooltip from "../base/Tooltip.vue"

export default {
  components: {
    DeckDetail,
    DeckPreview,
    Tooltip,
  },
  mounted() {
    this.subscribeData()
  },
  data() {
    return {
      visibleDeck: 0,
    }
  },
  props: {
    opponentName: String,
    rounds: Number,
    deck: String,
    opponentDeck: String,
    time: String,
    startTime: String,
    matches: Number,
    badges: Array,
    total: Number,
    history: String,
    expanded: Boolean,
  },
  computed: {
    timeString() {
      var date = new Date(this.startTime)
      var time

      var milliElapsed = Date.now() - date
      var secondsElapsed = milliElapsed / 1000
      var minElapse = secondsElapsed / 60
      var hoursElapse = minElapse / 60
      var daysElapsed = hoursElapse / 24

      if (secondsElapsed < 60) {
        time = this.$t("str.times.sec", { t: Math.floor(secondsElapsed) })
      } else if (minElapse < 60) {
        time = this.$t("str.times.min", { t: Math.floor(minElapse) })
      } else if (hoursElapse < 24) {
        if (Math.floor(hoursElapse) == 1) {
          time = this.$t("str.times.hour", { t: Math.floor(hoursElapse) })
        } else {
          time = this.$t("str.times.hours", { t: Math.floor(hoursElapse) })
        }
      } else if (daysElapsed < 7) {
        if (Math.floor(daysElapsed) == 1) {
          time = this.$t("str.times.day", { t: Math.floor(daysElapsed) })
        } else {
          time = this.$t("str.times.days", { t: Math.floor(daysElapsed) })
        }
      } else {
        time = date.toLocaleDateString()
      }

      return time
    },

    opponentLink() {
      return "/profile/" + this.opponentName
    },
    won() {
      return true
    },
    useRate() {
      return Math.floor((this.matches / this.total) * 100)
    },
    winRateColor() {
      return winRateToColor(this.winRate)
    },
    winRate() {
      return this.wonNum / this.matches
    },
    wonNum() {
      return (this.history.match(/W/g) || []).length
    },
    lostNum() {
      return (this.history.match(/L/g) || []).length
    },
    gamesString() {
      return this.matches > 1
        ? this.$t("matches.games", { num: this.matches })
        : this.$t("matches.game", { num: this.matches })
    },
  },
  emits: ["open"],
  methods: {
    showDeck() {
      // if (this.visibleDeck == 1) this.visibleDeck = 0
      // else this.visibleDeck = 1
      this.$emit("open")
    },
    showOpponentDeck() {
      // console.log("Show Oppo Deck")
      if (this.visibleDeck == 2) this.visibleDeck = 0
      else this.visibleDeck = 2
    },
    subscribeData() {
      // console.log(window)
    },
    isWonGame(index) {
      var i = index - 1
      // console.log(this.history)
      if (i >= this.history.length) return false
      return this.history[i] == "W"
    },
    isPlayedGame(index) {
      var i = index - 1
      // console.log(this.history)
      if (i >= this.history.length) return false
      return this.history[i] == "W" || this.history[i] == "L"
    },
  },
}
</script>
