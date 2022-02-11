<template>
  <region-icon
    class=""
    v-for="(faction, index) in getFactions"
    :key="index"
    :faction="faction"
  ></region-icon>
</template>

<script>
import RegionIcon from "../image/IconRegion.vue"
import DeckEncoder from "../../modules/runeterra/DeckEncoder"
//https://painttist.github.io/lor-champ-icons/data/champion.js

// import set1 from '../../../Resource/set1-en_us.json'
// import set2 from '../../../Resource/set2-en_us.json'
// import set3 from '../../../Resource/set3-en_us.json'
// import set4 from '../../../Resource/set4-en_us.json'
// import set5 from '../../../Resource/set5-en_us.json'

import en_us_array from "../../../../Resource/en_us.json"

const en_us = [].concat(...en_us_array).reduce((a, v) => ({ ...a, [v.cardCode]: v }), {})

// console.log("EN_US in Deck Regions:", en_us)

const regionRefID = {
  Demacia: 0,
  Freljord: 1,
  Ionia: 2,
  Noxus: 3,
  PiltoverZaun: 4,
  ShadowIsles: 5,
  Bilgewater: 6,
  Shurima: 7,
  Targon: 9,
  BandleCity: 10,
}

export default {
  components: {
    RegionIcon,
  },
  data() {
    return {
      champs: [],
      factions: [],
    }
  },
  mounted() {},
  props: {
    deck: {
      type: String,
      require: true,
    },
    maxFactions: {
      type: Number,
      default: 2,
    },
    fixedWidth: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    getFactions() {
      return this.getFactionsComplex.slice(0, this.maxFactions)
    },
    getFactionsComplex() {
      var factionIDs = []

      var cards = null
      if (!this.deck) return []
      try {
        cards = DeckEncoder.decode(this.deck)
      } catch (err) {
        return factionIDs
      }

      for (var j in cards) {
        var cardCode = cards[j].code
        var card = en_us[cardCode]
        if (card) {
          if (card.regions && card.regions.length == 1) {
            // Only considers mono region cards
            var regionID = regionRefID[card.regionRefs[0]]

            if (factionIDs.indexOf(regionID) == -1) {
              factionIDs.push(regionID)
            }
          }
        }
      }

      if (this.fixedWidth) {
        // Add filler champ icons
        var fillerIcons = this.maxFactions - factionIDs.length
        for (let i = 0; i < fillerIcons; i++) {
          factionIDs.unshift(-1)
        }
      }

      return factionIDs.sort((a, b) => a - b)
    },
  },
  methods: {},
}
</script>

<style scoped>
.icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
