<template>
  <div class="py-2">
    <div class="flex gap-2 items-baseline">
      <deck-preview class="max-w-[200px]" :deck="code" @click.stop="showDeck"></deck-preview>
      <div class="flex gap-2">
        <!-- Summary -->
        <p>{{playNum}} Matches</p>
        <p>{{(playRate*100).toFixed(2)}}% Play Rate</p>
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
    <p>{{(winRate*100).toFixed(2)}}% <span class=" text-sm text-gray-300 hover:text-gray-200">{{(winRateBounds.lower*100).toFixed(2)}}%-{{(winRateBounds.upper*100).toFixed(2)}}%</span></p>
    
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