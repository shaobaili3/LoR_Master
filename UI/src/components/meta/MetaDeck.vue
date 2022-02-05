<template>
  <div class="py-2">
    <div class="relative flex items-center justify-center gap-2 md:justify-start">
      <!-- Summary -->
      <div class="flex flex-col items-start w-32 gap-0 whitespace-nowrap">
        <p class="text-sm text-gray-200">
          <span v-if="isSummary">
            {{ $t("matches.meta", { num: (playRate * 100).toFixed(2) }) }}
          </span>
          <span v-if="!isSummary">
            {{ $t("matches.build", { num: (playRate * 100).toFixed(2) }) }}
          </span>
        </p>
        <p class="text-sm sm:text-base">{{ $t("matches.games", { num: playNum }) }}</p>
        <p
          class="text-lg sm:text-xl"
          :style="{
            color: closestColor(winRateBounds.centerAdjusted),
          }"
        >
          {{ (winRate * 100).toFixed(2) }}%
          <span class="block text-sm sm:text-base sm:inline"> | ± {{ (winRateBounds.gap * 50).toFixed(2) }}</span>
        </p>
      </div>

      <div class="flex flex-col items-start">
        <div v-if="isSummary" class="pl-2 text-sm text-gray-200">
          <span v-if="isFeature">{{ $t("matches.recommendedCurrent") }}</span>
          <span v-if="!isFeature">{{ $t("matches.recommended") }}</span>
        </div>
        <div v-if="!isSummary && isFeature" class="pl-2 text-sm text-gray-200">{{ $t("matches.current") }}</div>
        <div v-if="!isSummary && !isFeature" class="w-full h-4 text-sm text-gray-200"></div>
        <deck-preview
          v-if="code"
          class="max-w-[220px] md:mr-2"
          :class="{
            ' pointer-events-none': isFeature,
          }"
          :fixedWidth="true"
          :deck="code"
          @click.stop
        ></deck-preview>
      </div>

      <!-- Bar -->
      <div class="relative hidden sm:block sm:flex-1 sm:w-0">
        <div class="relative w-full h-1 my-2 bg-gray-400 rounded-full">
          <!-- Range   -->
          <div
            class="absolute h-2 -translate-y-1/2 rounded-full top-1/2"
            :style="{
              background: closestColor(winRateBounds.centerAdjusted),
              width: `max(0.5rem, min(${(winRateBounds.upper - winRateBounds.lower) * 100}%, ${winRateBounds.gap * 100}%))`,
              left: winRateBounds.lower * 100 + '%',
            }"
          ></div>

          <!-- Player Dots -->
          <div v-for="player in players" :key="player._id">
            <div
              class="absolute w-2 h-2 -translate-y-1/2 rounded-full top-1/2 group hover:z-10"
              v-if="player.win_rate > winRate"
              :style="{
                backgroundColor: closestColor(player.win_rate),
                left: player.win_rate * 100 + '%',
              }"
              @click="routePlayerProfile(player)"
            >
              <div
                class="
                  hidden
                  group-hover:block
                  absolute
                  right-0
                  top-2
                  min-w-[10rem]
                  w-fit
                  pointer-events-none
                  text-left
                  ml-2
                  pl-2
                  pr-2
                  py-2
                  bg-gray-700
                "
              >
                <p class="text-sm text-gray-200">
                  <span class="pre-info">
                    <i class="fas" :class="player.server === 'sea' ? 'fa-globe-asia' : 'fa-globe-' + player.server"></i>
                  </span>
                  {{ $t("str.regions." + player.server) }}
                </p>
                <p class="text-xl">{{ player.riot_id.split("#")[0] }}</p>
                <p class="text-gray-200">{{ $t("matches.games", { num: player.count }) }}</p>
                <p
                  :style="{
                    color: closestColor(player.win_rate),
                  }"
                >
                  {{
                    $t("matches.winRate", {
                      num: (player.win_rate * 100).toFixed(2),
                    })
                  }}
                </p>
              </div>
            </div>
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
              >{{ (winRateBounds.lower * 100).toFixed(2) }}%</span
            >
            <span v-if="winRateBounds.lower != winRateBounds.upper">
              -
              <span
                class="inline-block w-12 text-left"
                :style="{
                  color: closestColor(winRateBounds.upper),
                }"
                >{{ (winRateBounds.upper * 100).toFixed(2) }}%
              </span></span
            >
          </div>
        </div>
      </div>

      <button class="p-2 rounded-md text-white/50 hover:text-white hover:bg-gray-500" v-if="linkDetail" @click="openURL(detailLink)">
        <span>{{ $t("str.detail") }}</span>
        <i class="pl-1 fas fa-external-link-alt"></i>
      </button>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"

const Z = 1.96 // 95% confidence

import { winRateToColor, winrateGradient, winRateToMonoColor } from "../../modules/utils/colorUtils"

import { regionNameToShorts } from "../panels/PanelLeaderboard.vue"

// const gradientString =
//   "linear-gradient(90deg, " +
//   winrateGradient
//     .map((e) => {
//       return `#${e[0]} ${e[1] * 100}%`
//     })
//     .join(", ") +
//   ")"

export default {
  components: { DeckPreview },
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
    routePlayerProfile(player) {
      var splited = player.riot_id.split("#")
      this.$router.push({
        path: "/search",
        query: { name: splited[0], tag: splited[1], region: regionNameToShorts(player.server) },
      })
    },
    showDeck() {
      this.$emitter.emit("showDeck", this.code)
    },
    openURL(url) {
      if (this.IS_ELECTRON) {
        this.$emitter.emit("showDeckDetail", this.code)
      } else {
        // window.open(url, "_blank")
        this.$router.push(url)
      }
    },
    closestColor: winRateToColor,
  },
}
</script>
