<template>
  <div class="py-2">
    <div class="relative whitespace-nowrap justify-center md:justify-start flex gap-2 items-center">
      <!-- Summary -->
      <div class="flex flex-col gap-0 items-start">
        <p class="text-sm text-gray-200">
          <span v-if="isSummary">
            {{ $t("matches.meta", { num: (playRate * 100).toFixed(2) }) }}
          </span>
          <span v-if="!isSummary">
            {{ $t("matches.build", { num: (playRate * 100).toFixed(2) }) }}
          </span>
        </p>
        <p class="text-base">{{ $t("matches.games", { num: playNum }) }}</p>
        <p
          class="text-xl"
          :style="{
            color: closestColor(winRate),
          }"
        >
          {{ (winRate * 100).toFixed(2) }}% <span class="text-base"> | ± {{ (winRateBounds.gap * 100).toFixed(2) }}</span>
        </p>
      </div>

      <div class="flex flex-col items-start">
      <div v-if="isSummary" class="text-sm text-gray-200 pl-2">
        <span v-if="isFeature">Recommended (Current):</span>
        <span v-if="!isFeature">Recommended:</span>
      </div>
      <div v-if="!isSummary && isFeature" class="text-sm text-gray-200 pl-2">
        Current:
      </div>
      <div v-if="!isSummary && !isFeature" class="text-sm text-gray-200 h-4 w-full">
      </div>
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
      <div class="hidden sm:block sm:flex-1 sm:w-0 relative">
        <div class="w-full h-1 bg-gray-400 rounded-full my-2 relative">
          <!-- Range   -->
          <div
            class="h-2 absolute -translate-y-1/2 top-1/2 rounded-full"
            :style="{
              background: winRateBounds.gap < 0.05 ? closestColor(winRateBounds.lower) : closestColor(winRate),
              width: Math.max(winRateBounds.gap * 100, 1) + '%',
              left: winRateBounds.lower * 100 + '%',
              backgroundSize: (1 / winRateBounds.gap) * 100 + '%',
              backgroundPosition: winRate * 100 + '%',
            }"
          ></div>

          <!-- Player Dots -->
          <div v-for="player in players" :key="player._id">
            <div
              class="h-2 w-2 absolute -translate-y-1/2 top-1/2 rounded-full group hover:z-10"
              v-if="player.win_rate > winRateBounds.upper"
              :style="{
                backgroundColor: closestColor(player.win_rate),
                left: player.win_rate * 100 + '%',
              }"
            >
              <div class="hidden group-hover:block absolute right-0 top-2 min-w-[10rem] w-fit pointer-events-none text-left ml-2 pl-2 pr-2 py-2 bg-gray-700">
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
          class="block text-left w-fit mr-auto"
          :style="{
            color: closestColor(winRate),
            marginLeft: `${winRateBounds.lower * 100}%`,
          }"
        >
          <div class="text-sm">
            <span
              :style="{
                color: closestColor(winRateBounds.lower),
              }"
              >{{ (winRateBounds.lower * 100).toFixed(2) }}%</span
            >
            -
            <span
              :style="{
                color: closestColor(winRateBounds.upper),
              }"
              >{{ (winRateBounds.upper * 100).toFixed(2) }}%
            </span>
          </div>
        </div>
      </div>

      <button class="p-2 text-white/50 hover:text-white hover:bg-gray-500 rounded-md" v-if="linkDetail" @click="openURL(detailLink)">
        <span>{{ $t("str.detail") }}</span>
        <i class="pl-1 fas fa-external-link-alt"></i>
      </button>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"

const Z = 1.96 // 95% confidence

import { winRateToColor, winrateGradient } from "../../modules/utils/colorUtils"

const gradientString =
  "linear-gradient(90deg, " +
  winrateGradient
    .map((e) => {
      return `#${e[0]} ${e[1] * 100}%`
    })
    .join(", ") +
  ")"

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
      return {
        lower: this.winRate - interval,
        upper: this.winRate + interval,
        gap: interval * 2,
      }
    },
    detailLink() {
      return "/code?code=" + this.code
      // return "https://lor.mobalytics.gg/decks/code/" + this.baseDeck
    },
  },
  data() {
    return {
      gradientString: gradientString,
    }
  },
  methods: {
    showDeck() {
      this.$emitter.emit("showDeck", this.code)
    },
    openURL(url) {
      if (this.IS_ELECTRON) {
        this.$emitter.emit("showDeckDetail", this.code)
      } else {
        window.open(url, "_blank")
      }
    },
    closestColor: winRateToColor,
  },
}
</script>
