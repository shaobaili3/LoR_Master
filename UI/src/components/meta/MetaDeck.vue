<template>
  <div class="group py-2">
    <div class="relative flex items-center justify-center gap-2 md:justify-start">
      <div
        v-if="index || index == '0'"
        class="mr-4 rounded-md border-2 border-gray-600 py-0.5 px-2 text-sm text-gray-200"
      >
        {{ index + 1 }}
      </div>
      <!-- Summary -->
      <div class="flex w-32 flex-col items-start gap-0 whitespace-nowrap">
        <p class="w-full overflow-x-hidden text-ellipsis text-left text-sm text-gray-200">
          <span v-if="isSummary">
            {{ $t("matches.meta", { num: (playRate * 100).toFixed(2) }) }}
          </span>
          <span v-if="!isSummary">
            {{ $t("matches.build", { num: (playRate * 100).toFixed(2) }) }}
          </span>
        </p>
        <p
          class="text-sm text-white"
          :class="{
            ' sm:text-sm': sortRuleID == 1,
            ' sm:text-xl': sortRuleID == 0,
          }"
        >
          {{ $t("matches.games", { num: playNum }) }}
        </p>
        <p
          class="text-lg"
          :class="{
            'sm:text-2xl': sortRuleID == 1,
            'text-base': sortRuleID == 0,
          }"
          :style="{
            color: closestColor(winRateBounds.centerAdjusted),
          }"
        >
          {{ (winRate * 100).toFixed(1) }}%
          <span class="block text-sm sm:inline sm:text-sm">
            | ± {{ (winRateBounds.gap * 50).toFixed(1) }}</span
          >
        </p>
      </div>

      <!-- Deck Preview -->
      <div class="z-[1] flex w-fit flex-col items-start">
        <div v-if="isSummary" class="pl-2 text-sm text-gray-200">
          <span v-if="isFeature">{{ $t("matches.recommendedCurrent") }}</span>
          <span v-if="!isFeature">{{ $t("matches.recommended") }}</span>
        </div>
        <div v-if="!isSummary && isFeature" class="pl-2 text-sm text-gray-200">
          {{ $t("matches.current") }}
        </div>
        <div v-if="!isSummary && !isFeature" class="h-4 w-full text-sm text-gray-200"></div>
        <deck-preview
          v-if="code"
          class="mt-0.5 gap-1 px-1.5 py-2 text-base transition-colors hover:bg-gray-600 sm:gap-1.5 sm:px-2"
          :class="{
            ' pointer-events-none': isFeature,
          }"
          :deck="code"
          @click.stop
        ></deck-preview>
      </div>

      <!-- Bar -->
      <div class="relative hidden sm:block sm:w-0 sm:flex-1">
        <div class="relative my-2 h-1 w-full rounded-full bg-gray-400">
          <!-- Range   -->
          <div
            class="absolute top-1/2 h-2 -translate-y-1/2 rounded-full"
            :style="{
              background: closestColor(winRateBounds.centerAdjusted),
              width: `max(0.5rem, min(${(winRateBounds.upper - winRateBounds.lower) * 100}%, ${
                winRateBounds.gap * 100
              }%))`,
              left: winRateBounds.lower * 100 + '%',
            }"
          ></div>

          <!-- Player Dots -->
          <div v-for="player in players" :key="player._id">
            <meta-bar-player-dot :player="player"></meta-bar-player-dot>
          </div>
        </div>

        <!-- Winrate Text -->
        <div
          class="block w-full text-center"
          :style="{
            color: closestColor(winRate),
            transform: `translateX(calc(${(winRate - 0.5) * 100}% + 2px))`,
          }"
        >
          <div class="text-sm">
            <span
              class="inline-block w-12 text-right"
              :style="{
                color: closestColor(winRateBounds.lower),
              }"
              >{{ (winRateBounds.lower * 100).toFixed(1) }}%</span
            >
            <span v-if="winRateBounds.lower != winRateBounds.upper">
              -
              <span
                class="inline-block w-12 text-left"
                :style="{
                  color: closestColor(winRateBounds.upper),
                }"
                >{{ (winRateBounds.upper * 100).toFixed(1) }}%
              </span></span
            >
          </div>
        </div>
      </div>

      <button
        class="z-[1] whitespace-nowrap rounded-md p-2 text-white/50 transition-colors hover:bg-gray-500 group-hover:text-gold-300 group-hover:hover:text-white"
        v-if="linkDetail"
        @click="openURL(detailLink)"
      >
        <i class="fas fa-analytics pr-2"></i><span>{{ $t("str.detail") }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"

const Z = 1.96 // 95% confidence

import { winRateToColor, winrateGradient, winRateToMonoColor } from "../../modules/utils/colorUtils"

import { regionNameToShorts } from "../panels/PanelLeaderboard.vue"
import MetaBarPlayerDot from "./MetaBarPlayerDot.vue"

// const gradientString =
//   "linear-gradient(90deg, " +
//   winrateGradient
//     .map((e) => {
//       return `#${e[0]} ${e[1] * 100}%`
//     })
//     .join(", ") +
//   ")"

export default {
  components: { DeckPreview, MetaBarPlayerDot },
  mounted() {},
  props: {
    code: String,
    playNum: Number,
    playRate: Number,
    winRate: Number,
    players: Array,
    isFeature: Boolean,
    linkDetail: Boolean,
    isSummary: {
      type: Boolean,
      default: false,
    },
    index: Number,
    sortRuleID: Number,
  },
  computed: {
    winRateBounds() {
      var interval = Z * Math.sqrt((this.winRate * (1 - this.winRate)) / this.playNum)
      var lower = Math.max(0, this.winRate - interval)
      var upper = Math.min(1, this.winRate + interval)
      var gap = interval * 2
      return {
        lower: lower,
        upper: upper,
        gap: gap,
        centerAdjusted: lower + (upper - lower) * Math.min(1, Math.max(0.2, 0.5 - gap)),
      }
    },
    detailLink() {
      return "/code?code=" + this.code
      // return "https://lor.mobalytics.gg/decks/code/" + this.baseDeck
    },
  },
  data() {
    return {
      // gradientString: gradientString,
    }
  },
  methods: {
    showDeck() {
      this.$emitter.emit("showDeck", this.code)
    },
    openURL(url) {
      // if (this.IS_ELECTRON) {
      //   this.$emitter.emit("showDeckDetail", this.code)
      // } else {
      // window.open(url, "_blank")
      this.$router.push(url)
      // }
    },
    closestColor: winRateToColor,
  },
}
</script>
