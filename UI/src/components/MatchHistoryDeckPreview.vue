<template>
    <div class="row deck btn" :class="{won: won, loss: !won}">
        <deck-regions :deck="deck"></deck-regions>
        <deck-champs :deck="deck"></deck-champs>
    </div>
</template>

<script>

// const { DeckEncoder } = require('runeterra')
import DeckEncoder from '../modules/runeterra/DeckEncoder'
import championCards from '../assets/data/champion.js'
import DeckRegions from './DeckRegions.vue';
import DeckChamps from './DeckChamps.vue';
//https://painttist.github.io/lor-champ-icons/data/champion.js


const maxChamp = 2;
const maxSlot = 5;
const maxFactions = 3;

// function importAll(r) {
//     let images = {};
//     r.keys().map((item, index) => { images[item.replace('./', '')] = r(item); });
//     return images;
// }

// const cardImages = importAll(require.context('../assets/images/cards/cropped/', false, /\.(png|jpe?g|svg)$/));
// const regionImages = importAll(require.context('../assets/images/regions/', false, /\.(png|jpe?g|svg)$/));

export default {
    components: {
        DeckRegions,
        DeckChamps,
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
        deck: String,
        won: Boolean,
    },
    computed: {
        getChamps() {
            var champs = this.getChampsFactions.champs
            var factions = this.getChampsFactions.factions
            return champs.slice(0, maxSlot - Math.min(factions.length, maxFactions))
        },
        getFactions() {
            var factions = this.getChampsFactions.factions
            return factions.slice(0, maxFactions)
        },
        extraChampString() {
            var champs = this.getChampsFactions.champs
            var factions = this.getChampsFactions.factions
            var extra = (champs.length - (maxSlot - Math.min(factions.length, maxFactions)))
            // console.log(extra)
            if (extra > 0)
                return "+" + extra
            return ""
        },

        getChampsFactions() {
            
            var deck = null
            try { deck = DeckEncoder.decode(this.deck)} catch(err) {
                return
            }
            
            // console.log(factionIDs)
            // return factionIDs

            // console.log(deck)

            // var deck = DeckEncoder.decode(this.deck);
            var champs = []
            var factionIDs = []
            // console.log(championCards.champions)
            
            for (var j in deck) {
                if (factionIDs.indexOf(deck[j].faction.id) == -1) {
                    factionIDs.push(deck[j].faction.id)
                }
                for (var i in championCards.champions) {
                var champCode = championCards.champions[i]
                    var cardCode = deck[j].code
                    if (cardCode == champCode) {
                        champs.push(champCode)
                        // if (champs.length >= maxChamp) {
                        //     return champs;
                        // }
                    }
                }
            }
            
            return {
                champs: champs, 
                factions: factionIDs
            }
        },
    },
    methods: {
        
        getChampionImgUrl(code) {
            // const champImageBaseUrl = 'https://raw.githubusercontent.com/painttist/lor-champ-icons/master/images/cards/cropped/';
            // const champImageBaseUrl = 'https://painttist.github.io/lor-champ-icons/images/cards/cropped/';
            // return "url('" + champImageBaseUrl + code + "-cropped.png')"

            // -- Local
            // - v1
            var fileName = code + "-cropped.png"
            // return "url('" + cardImages[fileName] + "')"

            // - v2
            return "url(" + require('../assets/images/cards/cropped/' + fileName) + ")"
        },
        getRegionImgUrl(regionID) {
            
            // Remote

            // const regionImageBaseUrl = 'https://painttist.github.io/lor-champ-icons/images/regions/';
            // return "url(" + regionImageBaseUrl + regionID + ".svg)";
            
            // Local

            return "url(" + require('../assets/images/regions/' + regionID + ".svg") + ")"
        },
    }
}
</script>

<style scoped>

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

    .row.opponent {
        /* margin-bottom: 10px; */
        /* padding-left: 330px; */
    }

    .icon {
        
        display: block;
        margin-right: 0;
        margin-left: 0;

        padding: 9px;
        text-align: center;
        /* line-height: 30px; */
        /* vertical-align: middle; */
        width: 18px;
        height: 18px;
        color: white;

        /* background-color: white; */
        

        background-position: 50% 50%;
        background-size: cover;

        /* background-image: url('../assets/images/cards/cropped/01DE012-cropped.png'); */
    }

    .icon.cheveron {
        width: 10px;
        padding: 5px;
        margin-left: auto;
    }

    .icon.faction {
        opacity: 0.8;
        /* width: 26px; */
        padding: 9px 9px;
        /* padding-left: 0px; */
        filter: brightness(0) invert(1) drop-shadow(0.5px 1px 0.5px rgba(0, 0, 0, 0.1));
        /* box-shadow: 2px 2px 3px -2px black; */
        /* filter: drop-shadow(-2px 2px 1px rgba(43, 38, 27, 0.6)); */
        /* filter: drop-shadow(-0.5px 1px 0.5px white); */
    }

    .icon.champ {
        border-radius: 30px;
        border: 2px solid rgba(220, 220, 220, 1);
        /* box-shadow: -2px 2px 2px 0px rgba(43, 38, 27, 0.6) inset; */
    }

    .btn {
        /* box-shadow: 2px 2px 2px 0px rgba(43, 38, 27, 0.8); */
        /* border: 2px solid transparent; */
    }

    .btn.won:hover {
        /* mix-blend-mode: normal; */
        background-color: var(--col-gold);
        /* box-shadow: -1px 1px 2px 0px rgba(43, 38, 27, 0.7), 1px -1px 2px 0px rgba(255, 255, 255, 0.3);
        transform: translate(2px, -2px); */
        cursor: pointer;
        /* border: 2px solid white; */
    }

    .btn.loss:hover {
        /* mix-blend-mode: normal; */
        background-color: var(--col-lighter-grey);
        /* box-shadow: -1px 1px 2px 0px rgba(43, 38, 27, 0.7), 1px -1px 2px 0px rgba(255, 255, 255, 0.3);
        transform: translate(2px, -2px); */
        cursor: pointer;
        /* border: 2px solid white; */
    }

    @media screen and (max-width: 275px) {
        .icon {
            width: 15px;
            height: 15px;
        }
    }

</style>