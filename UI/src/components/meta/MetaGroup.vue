<template>
<div class=" px-2 rounded-lg transition-colors"
  :class="{
    'bg-gray-600': expand
  }"
>
  <meta-deck 
    :code="group.code" 
    :playNum="group.playNum"
    :playRate="group.playRate"
    :winRate="group.winRate"
    @click="expand = !expand"
  ></meta-deck>
  <transition name="height">
    <div v-if="expand" class=" pl-4">
      <div v-for="deck in group.decks" :key="deck.code">
        <meta-deck 
          :code="deck.code" 
          :playNum="deck.playNum"
          :playRate="deck.playRate"
          :winRate="deck.winRate"
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
  data() {
    return {
      expand: false,
    }
  }
}
</script>

<style>

</style>