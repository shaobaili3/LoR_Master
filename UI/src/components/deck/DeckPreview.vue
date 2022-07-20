<template>
  <div
    class="flex cursor-pointer items-center justify-center rounded-md transition-colors"
    @click="showDeck"
  >
    <deck-regions v-if="deck" :deck="deck"></deck-regions>
    <deck-champs :deck="deck"></deck-champs>
  </div>
</template>

<script>
import DeckChamps from "./DeckChamps.vue"
import DeckRegions from "./DeckRegions.vue"
//https://painttist.github.io/lor-champ-icons/data/champion.js

export default {
  components: {
    DeckChamps,
    DeckRegions,
  },
  data() {
    return {}
  },
  mounted() {},
  props: {
    deck: String,
    clickToShow: {
      type: Boolean,
      default: true,
    },
  },
  computed: {},
  methods: {
    showDeck() {
      if (this.clickToShow) {
        this.$emitter.emit("showDeck", this.deck)
      }
    },
  },
}
</script>

<style>
.row {
  display: flex;
  align-items: baseline;
}

.row.deck {
  /* width: 40%; */
  width: 100%;
  padding: 5px 5px 3px 5px;
  justify-content: center;
  border-radius: 6px;
  align-items: center;
  gap: 5px;
}

.row.deck .row {
  /* width: 100%; */
  display: flex;
  align-items: center;
  gap: 5px;
}

.row.deck.cheveron {
  justify-content: flex-start;
}

.icon.cheveron {
  width: 10px;
  padding: 5px;
  margin-left: auto;
}

@media screen and (max-width: 190px) {
  .row.deck .row {
    gap: 2px;
    /* padding: 4px 2px; */
  }
}
</style>
