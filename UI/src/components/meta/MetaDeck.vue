<template>
  <div class="py-2">
    <div class="relative flex-wrap justify-center md:justify-start flex gap-2 items-center">
      <deck-preview
        v-if="code"
        class="max-w-[220px] md:mr-2"
        :class="{
          ' pointer-events-none bg-gray-200/40': isFeature,
        }"
        :fixedWidth="true"
        :deck="code"
        @click.stop
      ></deck-preview>
      <div class="flex flex-row sm:flex-col gap-3 sm:gap-0 items-start">
        <!-- Summary -->
        <p class="text-sm text-gray-200">
          {{ $t("matches.usage", { num: (playRate * 100).toFixed(2) }) }}
        </p>
        <p class="text-lg">{{ $t("matches.games", { num: playNum }) }}</p>
      </div>
      <button class="p-2 text-white/50 hover:text-white hover:bg-gray-500 rounded-md absolute right-0" v-if="linkDetail" @click="openURL(detailLink)">
        <span>{{ $t("str.detail") }}</span>
        <i class="pl-1 fas fa-external-link-alt"></i>
      </button>
    </div>
    <div class="w-full h-1 bg-gray-400 rounded-full my-2 relative">
      <!-- <div class="h-2 bg-gold-400 absolute -translate-y-1/2 top-1/2 rounded-l-full"
      :style="{
        width: winRateBounds.gap * 50 + '%',
        left: winRateBounds.lower * 100 + '%',
      }"
      ></div>
      <div class="h-2 bg-gold-200 absolute -translate-y-1/2 top-1/2 rounded-r-full"
      :style="{
        width: winRateBounds.gap * 50 + '%',
        left: winRate * 100 + '%',
      }"
      ></div>-->
      <div
        class="h-2 absolute -translate-y-1/2 top-1/2 rounded-full"
        :style="{
          background: gradientString,
          width: winRateBounds.gap * 100 + '%',
          left: winRateBounds.lower * 100 + '%',
          backgroundSize: (1 / winRateBounds.gap) * 100 + '%',
          backgroundPosition: winRate * 100 + '%',
        }"
      ></div>
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
            <p :style="{
              color: closestColor(player.win_rate),
            }">
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
    <p
      class="block w-full text-left"
      :style="{
        color: closestColor(winRate),
        paddingLeft: `${winRateBounds.lower * 100}%`,
      }"
    >
      {{ (winRate * 100).toFixed(2) }}%
      <span class="text-sm text-gray-300 hover:text-gray-100 pl-1 hover:pl-2 transition-spacing">
        {{ (winRateBounds.lower * 100).toFixed(2) }}% - {{ (winRateBounds.upper * 100).toFixed(2) }}%
      </span>
    </p>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"

const Z = 1.96 // 95% confidence

const winrateGradient = [
  ["dc2626", 0.0],
  ["f59e0b", 0.4],
  ["f59e0b", 0.42],
  ["fbbf24", 0.44],
  ["facc15", 0.46],
  ["fde047", 0.48],
  ["fef08a", 0.5],
  ["ecfccb", 0.52],
  ["d9f99d", 0.54],
  ["bef264", 0.56],
  ["a3e635", 0.58],
  ["84cc16", 0.6],
  ["34d399", 0.7],
  ["2dd4bf", 0.8],
  ["38bdf8", 1.0],
]

const gradientString =
  "linear-gradient(90deg, " +
  winrateGradient
    .map((e) => {
      return `#${e[0]} ${e[1] * 100}%`
    })
    .join(", ") +
  ")"

const mix = function (color_1, color_2, weight) {
  function d2h(d) {
    return d.toString(16)
  } // convert a decimal value to hex
  function h2d(h) {
    return parseInt(h, 16)
  } // convert a hex value to decimal

  weight = typeof weight !== "undefined" ? weight : 50 // set the weight to 50%, if that argument is omitted

  var color = "#"

  for (var i = 0; i <= 5; i += 2) {
    // loop through each of the 3 hex pairs—red, green, and blue
    var v1 = h2d(color_1.substr(i, 2)), // extract the current pairs
      v2 = h2d(color_2.substr(i, 2)),
      // combine the current pairs from each source color, according to the specified weight
      val = d2h(Math.floor(v2 + (v1 - v2) * (weight / 100.0)))

    while (val.length < 2) {
      val = "0" + val
    } // prepend a '0' if val results in a single digit

    color += val // concatenate val to our new color string
  }

  return color // PROFIT!
}

export default {
  components: { DeckPreview },
  mounted() {
  },
  props: ["code", "playNum", "playRate", "winRate", "players", "isFeature", "linkDetail"],
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
      return "/?code=" + this.code
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
    closestColor(ratio) {
      for (let index in winrateGradient) {
        var gradient = winrateGradient[index]
        if (ratio < gradient[1]) {
          var last = winrateGradient[index - 1]
          var percent = ((ratio - last[1]) / (gradient[1] - last[1])) * 100
          return mix(gradient[0], last[0], percent)
        }
      }
      return winrateGradient[0][0]
    },
  },
}
</script>
