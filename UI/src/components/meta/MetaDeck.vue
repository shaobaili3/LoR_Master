<template>
  <div class="py-2">
    <div class="flex-wrap justify-center md:justify-start flex gap-2 items-center md:items-baseline">
      <deck-preview class="max-w-[200px]" :deck="code" @click.stop="showDeck"></deck-preview>
      <div class="block sm:flex gap-4">
        <!-- Summary -->
        <p>{{$t("matches.games", {num: playNum})}}</p>
        <p>{{$t('matches.usage', {num: (playRate*100).toFixed(2)})}}</p>
      </div>
    </div>
    <div class="w-full h-1 bg-gray-200 rounded-full my-2 relative">
      <div class="h-2 bg-gold-200 absolute -translate-y-1/2 top-1/2 rounded-full"
      :style="{
        width: winRateBounds.gap * 100 + '%',
        left: winRateBounds.lower * 100 + '%',
      }"
      ></div>
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
    "winRate"
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