<template>
    <div class="row deck btn" :class="{won: won, loss: !won}">
        <div class="region-icon icon faction" v-for="(faction, index) in factions" :key="index"
        :style=" {backgroundImage: getRegionImgUrl(faction)}"></div>
        <!-- <div class="region-icon icon faction" :style=" {backgroundImage: getRegionImgUrl(0)}"></div> -->
        <!-- <div class="region-icon icon"></div> -->
        <!-- <div class="region-icon icon">DE</div> -->
        <div class="champion-icon icon champ" v-for="(champ, index) in champions" :key="index"
            :style=" {backgroundImage: getChampionImgUrl(champ)}">
            <!-- <img :src="getChampionImgUrl(champ)" alt=""> -->
        </div>
        <!-- <div class="champion-icon icon">TF</div> -->
        <!-- <div class="fa fa-ellipsis-h"></div> -->
        <div class="icon cheveron fa fa-chevron-down"></div>
    </div>
</template>

<script>

const { DeckEncoder } = require('runeterra')
import championCards from '../assets/data/champion.js'

export default {
    data() {
        return {
        }
    }, 
    mounted() {
        var deck = DeckEncoder.decode(this.deck);
        // console.log(deck)
        
        // console.log("DeckEncoder: ", DeckEncoder.decode(this.deck))
    },
    props: {
        deck: String,
        won: Boolean,
    },
    computed: {
        factions() {
            var deck = DeckEncoder.decode(this.deck);
            var factionIDs = []
            const maxFactionIDs = 3;
            for (var i in deck) {
                if (factionIDs.indexOf(deck[i].faction.id) == -1) {
                    factionIDs.push(deck[i].faction.id)
                    if (factionIDs.length >= maxFactionIDs) {
                        return factionIDs;
                    }
                }
                // console.log(deck[i].faction.id)
            }
            // console.log(factionIDs)
            return factionIDs
        },
        champions() {
            var deck = DeckEncoder.decode(this.deck);
            const maxChamp = 2;
            var champs = []
            // console.log(championCards.champions)
            for (var i in championCards.champions) {
                var champCode = championCards.champions[i]
                for (var j in deck) {
                    var cardCode = deck[j].code
                    if (cardCode == champCode) {
                        champs.push(champCode)
                        if (champs.length >= maxChamp) {
                            return champs;
                        }
                    }
                }
            }
            // console.log(champs)
            return champs
        },
    },
    methods: {
        getChampionImgUrl(code) {
            return 'url(' + require('../assets/images/cards/cropped/' + code + "-cropped.png") + ")"
        },
        getRegionImgUrl(regionID) {
            // return 'url(' + require('../assets/images/factions/' + regionID + ".png") + ")"
            return 'url(' + require('../assets/images/regions/' + regionID + ".svg") + ")"
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
        padding: 7px 15px;
        justify-content: flex-start;
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

        padding: 10px;
        text-align: center;
        /* line-height: 30px; */
        /* vertical-align: middle; */
        width: 20px;
        height: 20px;
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

        filter: brightness(0) invert(1) opacity(0.8);

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

    .btn:hover .icon.faction {
        filter: brightness(0) invert(1) opacity(1);
    }

    .btn:hover .icon.champ {
        border: 2px solid rgba(255, 255, 255, 1);
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

</style>