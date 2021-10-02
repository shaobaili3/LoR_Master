<template>
    <div class="icon-container">
        <region-icon class="region-icon" v-for="(faction, index) in getFactions" :key="index" :faction="faction"></region-icon>
    </div>
</template>

<script>

import RegionIcon from './image/RegionIcon.vue'
import DeckEncoder from '../modules/runeterra/DeckEncoder'
//https://painttist.github.io/lor-champ-icons/data/champion.js

// import set1 from '../../../Resource/set1-en_us.json'
// import set2 from '../../../Resource/set2-en_us.json'
// import set3 from '../../../Resource/set3-en_us.json'
// import set4 from '../../../Resource/set4-en_us.json'
// import set5 from '../../../Resource/set5-en_us.json'

import en_us_array from '../../../Resource/en_us.json'

const en_us = [].concat(...en_us_array)

// console.log("EN_US in Deck Regions:", en_us)

const regionRefID = {
    "Demacia": 0,
    "Freljord": 1,
    "Ionia": 2,
    "Noxus": 3,
    "PiltoverZaun": 4,
    "ShadowIsles": 5,
    "Bilgewater": 6,
    "Shurima": 7,
    "Targon": 9,
    "BandleCity": 10
}

export default {
    components: {
        RegionIcon
    },
    data() {
        return {
            champs : [],
            factions : [],
        }
    }, 
    mounted() {
    },
    props: {
        deck: {
            type: String,
            require: true
        },
        maxFactions: {
            type: Number,
            default: 2
        },
        fixedWidth: {
            type: Boolean,
            default: true
        }
    },
    computed: {
        getFactions() {
            return this.getFactionsComplex.slice(0, this.maxFactions)
        },
        getFactionsComplex() {
            var factionIDs = []

            var cards = null
            try { cards = DeckEncoder.decode(this.deck)} catch(err) {
                return factionIDs
            }
            
            for (var j in cards) {
                
                var cardCode = cards[j].code
                var card = en_us.find(card => card.cardCode == cardCode)
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
            
            return factionIDs
        }
    },
    methods: {
    }
}
</script>

<style scoped>
    .icon-container {
        display: flex;
        /* padding: 4px; */

        gap: 2px;
        
        align-items: center;
        justify-content: center;
        
        /* border-radius: 50px; */
    }

    .btn:hover .icon-container .icon.faction, 
    .btn.active .icon-container .icon.faction {
        opacity: 1;
        filter: brightness(0) invert(1) drop-shadow(1px 2px 1px rgba(0, 0, 0, 0.6));
    }

    
</style>