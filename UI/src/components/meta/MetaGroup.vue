<template>
<div class=" px-2 rounded-lg transition-colors"
  :class="{
    'bg-gray-700': expand
  }"
>
  <meta-deck 
    :code="recommended" 
    :playNum="group.play_num"
    :playRate="group.play_rate"
    :winRate="group.win_rate"
    :players="group.players"
    @click="expand = !expand"
  ></meta-deck>
  <transition name="height">
    <div v-if="expand" class=" pl-4">
      <div v-for="deck in group.decks" :key="deck.deck_code">
        <meta-deck 
          :code="deck.deck_code" 
          :playNum="deck.play_num"
          :playRate="deck.play_rate"
          :winRate="deck.win_rate"
        ></meta-deck>
      </div>
    </div>
  </transition>
</div>
</template>

<script>
import MetaDeck from '../meta/MetaDeck.vue'
export default {
  components: { MetaDeck },
  props: ["group"],
  computed: {
    recommended() {
      var highest = 0
      var code = null
      for(let deck of this.group.decks) {
        if (deck.win_rate > highest) {
          highest = deck.win_rate
          code = deck.deck_code
        }
      }
      return code
    }
  },
  data() {
    return {
      expand: false,
    }
  }
}
</script>

<style>

</style>