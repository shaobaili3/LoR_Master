<template>
    <!-- <p><span>{{cost}}--</span><slot></slot><span>--{{count}}</span></p> -->
    <div class="cardContainer"
        :style=" {background: getCardPreviewBackgroundStyle()}">
        <div class="cardContent cardCost">{{cost}}</div>
        <div class="cardContent cardName">{{name}}</div>
        <div class="cardContent cardCount">x{{count}}</div>
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
    },
    computed: {
        
    },
    methods: {
        getCardPreviewBackgroundStyle() {
            // const champImageBaseUrl = 'https://raw.githubusercontent.com/painttist/lor-champ-icons/master/images/cards/cropped/';
            const cardPreviewUrlBase = 'https://cdn-lor.mobalytics.gg/production/images/cards-preview/';
            
            // const gradient = "linear-gradient(90deg, rgb(191, 176, 131) 30%, rgba(191, 176, 131, 0) 70%),"
            const gradient = "linear-gradient(90deg, rgb(65, 65, 65) 30%, rgba(65, 65, 65, 0) 70%),"
            
            return gradient + "url(" + cardPreviewUrlBase + this.code + ".webp) right top no-repeat"
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
    
    /* border-radius: 4px; */
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
    padding: 7px 2px;
    /* border-radius: 50px 0px 0px 50px; */
    border-radius: 0px 8px 8px 0px;
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

</style>