<template>
    <div class="icon-container">
        <champ-icon v-for="(champ, index) in getChamps" :key="index" :code="champ"></champ-icon>
        <div class="extra-champ" :class="{'fixed-width': fixedWidth }" v-if="extraChampString">{{extraChampString}}</div>
        <deck-regions v-if="getChamps.length <= 0 && showRegion" :deck="deck" :fixedWidth="fixedWidth"></deck-regions>
    </div>
</template>

<script>

import DeckEncoder from '../../modules/runeterra/DeckEncoder'
import championCards from '../../assets/data/champion.js'
import ChampIcon from '../image/ChampIcon.vue'
import DeckRegions from './DeckRegions.vue'

// const maxChamp = 2;

export default {
    components: { ChampIcon, DeckRegions },
    data() {
        return {}
    }, 
    mounted() {
    },
    props: {
        deck: {
            type: String,
            require: true
        },
        maxChamp: {
            type: Number,
            default: 2
        },
        showRegion: {
            type: Boolean,
            default: false
        },
        fixedWidth: {
            type: Boolean,
            default: true
        }
    },
    computed: {
        getChamps() {
            return this.getChampsFromDeck.slice(0, this.maxChamp)
        },
        extraChampString() {
            var extra = (this.getChampsFromDeck.length - this.maxChamp)
            if (extra > 0)
                return "+" + extra
            return ""
        },
        getChampsFromDeck() {
            var deck = null
            try { deck = DeckEncoder.decode(this.deck)} catch(err) {
                console.log(err)
                console.log(this.deck)
                return []
            }
            var champs = []
            for (var j in deck) {
                for (var i in championCards.champions) {
                    var champCode = championCards.champions[i]
                    var cardCode = deck[j].code
                    if (cardCode == champCode) {
                        champs.push(champCode)
                    }
                }
            }
            // Add filler champ icons
            if (this.fixedWidth) {
                var fillerIcons = this.maxChamp - champs.length
                for (let i = 0; i < fillerIcons; i++) {
                    champs.push("")
                }
            }
            return champs
        },
    },
    methods: {
    }
}
</script>

<style scoped>

    .icon-container {
        display: flex;
        gap: 2px;
        /* padding: 4px; */
        align-items: center;
        position: relative;

        /* border-radius: 50px; */
    }
    
    .btn:hover .icon-container .icon.champ,
    .btn.active .icon-container .icon.champ {
        border: 2px solid rgba(255, 255, 255, 1);
        box-shadow: 1px 2px 5px -2px #000000;
    }

    .icon {
        border: 2px solid transparent;
    }

    .extra-champ.fixed-width {
        position: absolute;
        top: 0;
        right: -20px;
        transform: translate(0, 50%);
    }

    /*     
    .count {
        padding: 2px;
        background: var(--col-darker-grey);
        border-radius: 100%;
    } */

</style>