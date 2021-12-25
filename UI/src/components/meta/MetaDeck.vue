<template>
  <div class="py-2">
    <div class="relative flex-wrap justify-center md:justify-start flex gap-2 items-center">
      <deck-preview v-if="code" class="max-w-[220px] md:mr-2"
        :class="{
          ' pointer-events-none bg-gray-200/40': isFeature
        }"
      :fixedWidth="true" :deck="code" @click.stop></deck-preview>
      <div class=" flex flex-row sm:flex-col gap-3 sm:gap-0 items-start">
        <!-- Summary -->
        <p class="text-sm text-gray-200">{{$t('matches.usage', {num: (playRate*100).toFixed(2)})}}</p>
        <p class="text-lg">{{$t("matches.games", {num: playNum})}}</p>
      </div>
      <button class="p-2 text-white/50 hover:text-white hover:bg-gray-500 rounded-md absolute right-0" v-if="linkDetail" @click="openURL(detailLink)">
        <span>{{$t('str.detail')}}</span><i class="pl-1 fas fa-external-link-alt"></i>
      </button>
    </div>
    <div class="w-full h-1 bg-gray-200 rounded-full my-2 relative">
      
      <div class="h-2 bg-gold-400 absolute -translate-y-1/2 top-1/2 rounded-l-full"
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
      ></div>
      <div v-for="player in players" :key="player._id">
        <div class="h-2 w-2 bg-sky-300 absolute -translate-y-1/2 top-1/2 rounded-full group hover:z-10"
          v-if="player.win_rate > winRateBounds.upper"
          :style="{
            left: player.win_rate * 100 + '%',
          }"
        >
          <div class="hidden group-hover:block absolute right-0 top-2 min-w-[10rem] w-fit pointer-events-none text-left ml-2 pl-2 pr-2 py-2 bg-gray-700">
            <p class="text-sm text-gray-200">
              <span class="pre-info"><i class="fas" :class="player.server === 'sea' ? 'fa-globe-asia' : 'fa-globe-'+player.server"></i></span>
              {{$t('str.regions.'+player.server)}}
            </p>
            <p class="text-xl">{{player.riot_id.split('#')[0]}}</p>
            <p>
              {{$t("matches.games", {num: player.count})}}
            </p>
            <p>{{$t('matches.winRate', {num: (player.win_rate * 100).toFixed(2)})}}</p>
          </div>
        </div>
      </div>
    </div>
    <p 
    class=" block w-full text-left"
      :style="{
        paddingLeft: `${winRateBounds.lower*100}%`
      }"
    >{{(winRate*100).toFixed(2)}}% <span class=" text-sm text-gray-300 hover:text-gray-100 pl-1 hover:pl-2 transition-spacing">{{(winRateBounds.lower*100).toFixed(2)}}% - {{(winRateBounds.upper*100).toFixed(2)}}%</span></p>
    
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"

const Z = 1.96 // 95% confidence

export default {
  components: { DeckPreview },
  props: [
    "code",
    "playNum",
    "playRate",
    "winRate",
    "players",

    "isFeature",
    "linkDetail"
  ],
  computed: {
    winRateBounds() {
      var interval = Z * Math.sqrt( this.winRate*(1-this.winRate) / this.playNum )
      return {
        lower: this.winRate - interval,
        upper: this.winRate + interval,
        gap: interval*2,
      }
    },
    detailLink() {
        return '/?code=' + this.code
        // return "https://lor.mobalytics.gg/decks/code/" + this.baseDeck
    },
  },
  methods: {
    showDeck() {
      this.$emitter.emit('showDeck', this.code)
    },
    openURL(url) {
            if (this.IS_ELECTRON) {
                this.$emitter.emit('showDeckDetail', this.code)
            } else {
                window.open(url, "_blank")
            }
        }
  }
}
</script>