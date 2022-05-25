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

import en_us_array from "../../data/en_us.json"

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
  Runeterra: 12,
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
      var factionIDs = []
      var champFactions = []

      var factionCounts = []
      for (var region in regionRefID) {
        factionCounts[regionRefID[region]] = 0
      }

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

            if (card.rarityRef == "Champion" && card.collectible) {
              if (champFactions.indexOf(regionID) == -1 && regionID != regionRefID.Runeterra) {
                champFactions.push(regionID)
              }
            }

            factionCounts[regionID] += 1

            if (factionIDs.indexOf(regionID) == -1) {
              factionIDs.push(regionID)
            }
          }
        }
      }

      if (factionIDs.indexOf(regionRefID.Runeterra) != -1) {
        // There is runeterra champions included
        if (champFactions.length > 0) {
          // Use the other champion's region
          factionIDs = champFactions
        } else {
          // Use the region with most number of cards
          var max = 0
          for (var ref in regionRefID) {
            var k = regionRefID[ref]
            if (factionCounts[k] > max) {
              max = factionCounts[k]
              factionIDs = [k]
            }
            k += 1
          }
        }
      }

      if (this.fixedWidth) {
        // Add filler champ icons
        var fillerIcons = this.maxFactions - factionIDs.length
        for (let i = 0; i < fillerIcons; i++) {
          factionIDs.push(99)
        }
      }

      return factionIDs.sort((a, b) => a - b).slice(0, this.maxFactions)
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
