<template>
  <div
    class="flex justify-center flex-1 p-1 rounded cursor-pointer w-fit hover:bg-gray-700 btn"
    @click="showDeck"
    :class="{
      won: won,
      loss: !won,
      cheveron: cheveron,
      invisible: !deck,
      'scale-75 -my-2 -mx-4': size == 1,
    }"
  >
    <div class="flex items-center" :class="{ 'w-[160px] sm:w-[190px]': fixedWidth }">
      <deck-regions :deck="deck" :fixedWidth="true"></deck-regions>
      <deck-champs :deck="deck" :fixedWidth="!cheveron"></deck-champs>
      <div v-if="cheveron" class="icon cheveron fa" :class="{ 'fa-chevron-down': !isShown, 'fa-chevron-up': isShown }"></div>
    </div>
  </div>
</template>

<script>
import DeckEncoder from "../../modules/runeterra/DeckEncoder"
import championCards from "../../assets/data/champion.js"
import DeckChamps from "./DeckChamps.vue"
import DeckRegions from "./DeckRegions.vue"
//https://painttist.github.io/lor-champ-icons/data/champion.js

const DeckPreviewSize = {
  xs: 0,
  sm: 1,
  md: 2,
  lg: 3,
}

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
    won: Boolean,
    cheveron: {
      type: Boolean,
      default: false,
    },
    fixedWidth: {
      // 180px vs 100%
      type: Boolean,
      default: false,
    },
    isShown: {
      type: Boolean,
      default: false,
    },
    clickToShow: {
      type: Boolean,
      default: true,
    },
    size: {
      typeof: DeckPreviewSize,
      default: DeckPreviewSize.md,
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
