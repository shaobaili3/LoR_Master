<template>
  <div class="py-2">
    <div class="flex-wrap justify-center md:justify-start flex gap-2 items-center md:items-baseline">
      <deck-preview class="max-w-[200px]" :deck="code" @click.stop="showDeck"></deck-preview>
      <div class="block sm:flex gap-3 md:pl-2">
        <!-- Summary -->
        <p>{{$t("matches.games", {num: playNum})}}</p>
        <p>{{$t('matches.usage', {num: (playRate*100).toFixed(2)})}}</p>
      </div>
    </div>
    <div class="w-full h-1 bg-gray-200 rounded-full my-2 relative">
      <div class="h-2 bg-gold-300 absolute -translate-y-1/2 top-1/2 rounded-full"
      :style="{
        width: winRateBounds.gap * 100 + '%',
        left: winRateBounds.lower * 100 + '%',
      }"
      ></div>
      <div v-for="player in players" :key="player._id">
        <div class="h-2 w-2 bg-gold-200 absolute -translate-y-1/2 top-1/2 rounded-full group hover:z-10"
          v-if="player.win_rate > winRateBounds.upper"
          :style="{
            left: player.win_rate * 100 + '%',
          }"
        >
          <div class="hidden group-hover:block absolute right-0 top-2 min-w-[10rem] w-fit pointer-events-none text-left ml-2 pl-2 pr-2 py-2 bg-gray-800">
            <p class="text-sm text-gray-300">
              <span class="pre-info"><i class="fas" :class="player.server === 'sea' ? 'fa-globe-asia' : 'fa-globe-'+player.server"></i></span>
              {{$t('str.regions.'+player.server)}}
            </p>
            <p class="text-xl">{{player.riot_id.split('#')[0]}}</p>
            <p>
              {{$t("matches.games", {num: player.count})}}
            </p>
            <p>{{(player.win_rate * 100).toFixed(2) + '% ' + $t('dash.winRate')}}</p>
            
          </div>
        </div>
      </div>
    </div>
    <p 
    class=" block w-full text-left"
      :style="{
        paddingLeft: `${winRateBounds.lower*100}%`
      }"
    >{{(winRate*100).toFixed(2)}}% <span class=" text-sm text-gray-300 hover:text-gray-200">{{(winRateBounds.lower*100).toFixed(2)}}%-{{(winRateBounds.upper*100).toFixed(2)}}%</span></p>
    
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
    "players"
  ],
  computed: {
    winRateBounds() {
      var interval = Z * Math.sqrt( this.winRate*(1-this.winRate) / this.playNum )
      return {
        lower: this.winRate - interval,
        upper: this.winRate + interval,
        gap: interval*2,
      }
    }
  },
  methods: {
    showDeck() {
      this.$emitter.emit('showDeck', this.code)
    }
  }
}
</script>