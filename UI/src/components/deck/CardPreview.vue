<template>
    <div class="cardContainer group"
        :class="{empty: count == 0, spell: typeRef == 'Spell', unit: typeRef == 'Unit', 
        champ: typeRef == 'Champion', landmark: typeRef == 'Landmark',
        unknown: typeRef == 'Unkown'
        }"
        :style="{background: getCardPreviewBackgroundStyle()}">
        <div class="cardContent cardCost">{{cost}}</div>
        <div class="cardContent cardName">{{name}}</div>
        <div class="cardContent cardCount">x{{count}}</div>
        <div v-if="type === 'Unknown'" class="
            lab-secret
            transition-opacity opacity-0 group-hover:opacity-100 
            absolute left-1/2 top-0 transform -translate-x-1/2
            px-4 bg-black h-full flex items-center justify-center
            whitespace-nowrap z-10 pointer-events-none
            w-full 
            ">
            {{$t('str.labSecrets')}}
        </div>
        <card-image class="cardDisplay" :code="code" :set="set"></card-image>
    </div>
</template>

<script>

// Image from mobalytics | 220x40
// https://cdn-lor.mobalytics.gg/production/images/cards-preview/01DE029.webp

import axios from 'axios'
import CardImage from '../image/CardImage.vue'

const requestStatusWaitTime = 1000 //ms
var lastStatusRequestTime

export default {
    components: { CardImage },
    mounted() {
    },
    data() {
        return {}
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
    },
    computed: {
    },
    methods: {
        getCardPreviewBackgroundStyle() {
            // const champImageBaseUrl = 'https://raw.githubusercontent.com/painttist/lor-champ-icons/master/images/cards/cropped/';
            // const unkown = 'https://cdn-lor.mobalytics.gg/production/images/subscribe-banner.jpg'
            
            const grayOverlay = 'linear-gradient(90deg, rgb(65, 65, 65) 30%, rgba(65, 65, 65, 0) 70%)'

            // const colored = 'linear-gradient(94deg, rgba(73,213,245,1) 44%, rgba(167,79,255,1) 90%)'
            const colored2 = 'linear-gradient(120deg, rgba(19,28,69,1) 10%, rgba(73,213,245,1) 50%, rgba(167,79,255,1) 90%)'
            if (this.typeRef === "Unknown") {
                return `${colored2}`
            }
            
            const cardPreviewUrlBase = 'https://cdn-lor.mobalytics.gg/production/images/cards-preview/';
            
            // const gradient = "linear-gradient(90deg, rgb(191, 176, 131) 30%, rgba(191, 176, 131, 0) 70%),"
            var gradient
            if (this.supertype == "Champion") {
                gradient = "linear-gradient(90deg, var(--col-darker-gold) 30%, rgba(158, 114, 18, 0) 70%),"
            } else {
                gradient = `${grayOverlay},`
            }
            
            return gradient + "url(" + cardPreviewUrlBase + this.code + ".webp) right top no-repeat"
        },
        
    }
}
</script>

<style scoped>

.lab-secret {
    background: linear-gradient(120deg, rgba(0,20,20,1) 14%, rgba(255,154,38,1) 14%, rgba(255,154,38,1) 23%, rgba(0,20,20,1) 23%, rgba(0,20,20,1) 42%, rgba(255,154,38,1) 42%, rgba(250,155,43,1) 53%, rgba(0,20,20,1) 53%, rgba(0,20,20,1) 72%, rgba(255,154,38,1) 72%, rgba(248,156,46,1) 81%, rgba(0,20,20,1) 81%);
    /* background: linear-gradient(120deg, rgba(0,0,0,1) 14%, rgba(255,154,38,1) 14%, rgba(240,159,55,1) 23%, rgba(0,0,0,1) 23%, rgba(0,0,0,1) 72%, rgba(186,117,35,1) 72%, rgba(248,156,46,1) 81%, rgba(0,0,0,1) 81%); */
}
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
    @apply transition-opacity;

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