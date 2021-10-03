<template>
    <div class="cardContainer"
        :class="{empty: count == 0, spell: typeRef == 'Spell', unit: typeRef == 'Unit', champ: typeRef == 'Champion', landmark: typeRef == 'Landmark'}"
        :style="{background: getCardPreviewBackgroundStyle()}">
        <div class="cardContent cardCost">{{cost}}</div>
        <div class="cardContent cardName">{{name}}</div>
        <div class="cardContent cardCount">x{{count}}</div>
        <!-- <div class="cardDisplay" :style="{background: getCardDisplay()}"></div> -->
        <img class="cardDisplay" :src = "getCardDisplayUrl()" alt="">
    </div>
</template>

<script>

// Image from mobalytics | 220x40
// https://cdn-lor.mobalytics.gg/production/images/cards-preview/01DE029.webp

import axios from 'axios'

const requestStatusWaitTime = 1000 //ms
var lastStatusRequestTime

export default {
    mounted() {
    },
    data() {
    }, 
    props: {
        code: String,
        name: String,
        count: Number,
        cost: Number,
        type: String,
        typeRef: String,

        supertype: String,
        set: String,

        locale: {
            type: String,
            default: 'en_us'
        }
    },
    computed: {
        
    },
    methods: {
        getCardPreviewBackgroundStyle() {
            // const champImageBaseUrl = 'https://raw.githubusercontent.com/painttist/lor-champ-icons/master/images/cards/cropped/';
            const cardPreviewUrlBase = 'https://cdn-lor.mobalytics.gg/production/images/cards-preview/';
            
            // const gradient = "linear-gradient(90deg, rgb(191, 176, 131) 30%, rgba(191, 176, 131, 0) 70%),"
            var gradient
            if (this.supertype == "Champion") {
                gradient = "linear-gradient(90deg, var(--col-darker-gold) 30%, rgba(158, 114, 18, 0) 70%),"
            } else {
                gradient = "linear-gradient(90deg, rgb(65, 65, 65) 30%, rgba(65, 65, 65, 0) 70%),"
            }
            
            return gradient + "url(" + cardPreviewUrlBase + this.code + ".webp) right top no-repeat"
        },
        getCardDisplay() {
            return "url(" + this.getCardDisplayUrl() + ")"
        },
        getCardDisplayUrl() {
            const cardDisplayUrlBase = 'https://dd.b.pvp.net/latest/'
            // const locale = 'zh_tw'
            return cardDisplayUrlBase + this.set.toLowerCase()  + '/' + this.locale + '/img/cards/' + this.code + '.png' 
        },
    }
}
</script>

<style>

.cardContainer {
    max-width: 320px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 4px;
    cursor: default;

    position: relative;
    /* border-radius: 4px; */
}

.cardContainer:hover .cardDisplay {
    /* display: block; */
    /* visibility: initial; */
    /* position: relative; */
    opacity: 1;

    transition: opacity 0.15s cubic-bezier(0.075, 0.82, 0.165, 1);
}

.cardContainer.empty .cardCount{
    opacity: 0.5;
}

.cardDisplay {
    /* content: ""; */
    /* display: none; */
    /* visibility: hidden; */
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;

    pointer-events: none;

    width: 100%;
    height: auto;
    /* width: auto; */
    /* height: 100px; */
    /* background: white; */
    
    filter: drop-shadow(3px 3px 2px rgba(43, 38, 27, 0.6));

    z-index: 10;

    transition: opacity 0.15s cubic-bezier(0.075, 0.82, 0.165, 1);

    /* background-size: contain; */
}

.cardContent {
    flex: 1 0;
    padding: 8px 3px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 34px;
    max-height: 15.5vw;
    box-sizing: border-box;
    font-size: clamp(12px, 8vw, 15px);
}

.cardCost {
    background: var(--col-blue-light-grey);
    /* background: var(--col-dark-gold); */
    /* color: var(--col-dark-grey); */
    /* width: 50%; */
    /* height: 70%; */
    /* padding: 5px; */
    /* border-radius: 50px 0px 0px 50px; */
    border-radius: 0px 8px 8px 0px;
    /* border-radius: 20px; */
}

.cardName {
    flex: 8 0;
    justify-content: flex-start;
    /* padding: 9px 2px 9px 6px; */
    padding-left: 6px;
    text-shadow: rgb(0 0 0) 0px 1px 3px;
    box-sizing: border-box;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

.cardCount {
    /* padding: 0px; */
    background: var(--col-light-grey);
}

.champ .cardCost {
    /* color: black; */
    background: var(--col-mid-gold);
}

.champ .cardCount {
    /* padding: 0px; */
    background: var(--col-mid-gold);
}

:not(.spell) + .spell, 
:not(.unit) + .unit, 
:not(.landmark) + .landmark{
    position: relative;
    margin-top: 12px;
}

:not(.spell) + .spell::before, 
:not(.unit) + .unit::before, 
:not(.landmark) + .landmark::before{
    content: "";
    /* display: block; */
    position: absolute;
    top: -6px;
    height: 1px;
    width: 100%;
    padding: 0px 5px;
    box-sizing: border-box;
    background: var(--col-lighter-grey);
    background-clip: content-box;
    /* margin-top: 4px; */
    /* padding-top: 10px; */
    /* border-top: 1px solid white; */
    /* background-origin: content-box; */
}




</style>