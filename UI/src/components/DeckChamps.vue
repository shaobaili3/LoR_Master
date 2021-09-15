<template>
    <div class="icon-container">
        <!-- <div class="count">
            <slot></slot>
        </div> -->
        <div class="champion-icon icon champ" v-for="(champ, index) in getChamps" :key="index"
            :style=" {backgroundImage: getChampionImgUrl(champ)}">
        </div>
        <div class="extra-champ" v-if="extraChampString">{{extraChampString}}</div>
        
    </div>
</template>

<script>

import DeckEncoder from '../modules/runeterra/DeckEncoder'
import championCards from '../assets/data/champion.js'

const maxChamp = 2;

export default {
    components: {

    },
    data() {
        return {
            champs : [],
            factions : [],
        }
    }, 
    mounted() {
        this.getChampsFromDeck()
    },
    props: {
        deck: String
    },
    computed: {
        // factions() {
        //     var deck = DeckEncoder.decode(this.deck);
        //     var factionIDs = []
        //     for (var i in deck) {
        //         if (factionIDs.indexOf(deck[i].faction.id) == -1) {
        //             factionIDs.push(deck[i].faction.id)
        //             if (factionIDs.length >= maxFactionIDs) {
        //                 return factionIDs;
        //             }
        //         }
        //         // console.log(deck[i].faction.id)
        //     }
        //     // console.log(factionIDs)
        //     return factionIDs
        // },
        getChamps() {
            return this.champs.slice(0, maxChamp)
        },
        extraChampString() {
            // console.log("Champ length:", this.champs.length)
            // console.log(this.champs)
            var extra = (this.champs.length - maxChamp)
            // console.log(extra)
            if (extra > 0)
                return "+" + extra
            return ""
        }
    },
    methods: {
        
        getChampsFromDeck() {
            
            var deck = null
            try { deck = DeckEncoder.decode(this.deck)} catch(err) {
                return
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
            this.champs = champs
        },
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
    }
}
</script>

<style scoped>

    .icon-container {
        display: flex;
        gap: 2px;
        padding: 4px;
        align-items: center;

        border-radius: 50px;
    }

    .icon-container:hover {
        background: var(--col-dark-grey);
    }

    .icon-container.active {
        background: var(--col-light-grey);
    }
    
    .count {
        padding: 2px;
        background: var(--col-darker-grey);
        border-radius: 100%;
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

    @media screen and (max-width: 275px) {
        .icon {
            width: 15px;
            height: 15px;
        }
    }

</style>