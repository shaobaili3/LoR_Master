<template>
    <div class="icon-container">
        <region-icon class="region-icon" v-for="(faction, index) in getFactions" :key="index" :faction="faction"></region-icon>
    </div>
</template>

<script>

import RegionIcon from './image/RegionIcon.vue'
import DeckEncoder from '../modules/runeterra/DeckEncoder'
//https://painttist.github.io/lor-champ-icons/data/champion.js

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
            default: 3
        }
    },
    computed: {
        getFactions() {
            return this.getFactionsComplex.slice(0, this.maxFactions)
        },
        getFactionsComplex() {
            var factionIDs = []

            var deck = null
            try { deck = DeckEncoder.decode(this.deck)} catch(err) {
                return factionIDs
            }
            
            for (var j in deck) {
                if (factionIDs.indexOf(deck[j].faction.id) == -1) {
                    factionIDs.push(deck[j].faction.id)
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