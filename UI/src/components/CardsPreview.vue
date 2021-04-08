<template>
    <div class="cardContainer"
        :class="{spell: type == 'Spell', unit: type == 'Unit', champ: supertype == 'Champion', landmark: type == 'Landmark'}"
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

export default {
    // mounted() {
    //     this.getCardsInfo()
    // },
    // data() {
    //     return {}
    // }, 
    props: {
        code: String,
        name: String,
        count: Number,
        cost: Number,
        type: String,
        supertype: String,
        set: String,
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
            const locale = 'en_us'
            // const locale = 'zh_tw'
            return cardDisplayUrlBase + this.set.toLowerCase()  + '/' + locale + '/img/cards/' + this.code + '.png' 
        }
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
    visibility: initial;
    /* position: relative; */
}

.cardDisplay {
    /* content: ""; */
    /* display: none; */
    visibility: hidden;
    position: absolute;
    top: 0;
    left: 0;

    pointer-events: none;

    width: 270px;
    height: auto;
    /* width: auto; */
    /* height: 100px; */
    /* background: white; */

    z-index: 10;

    /* background-size: contain; */
}

.cardContent {
    flex: 1 0;
    padding: 9px 4px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.cardCost {
    background: var(--col-light-grey);
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
    width: 250px;
    padding: 0px 10px;
    background: var(--col-lighter-grey);
    background-clip: content-box;
    /* margin-top: 4px; */
    /* padding-top: 10px; */
    /* border-top: 1px solid white; */
    /* background-origin: content-box; */
}




</style>