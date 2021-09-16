<template>
    <div class="row deck btn" :class="{won: won, loss: !won}">
        <deck-champs :deck="deck"></deck-champs>
        <deck-regions :deck="deck"></deck-regions>
        <div class="icon cheveron fa fa-chevron-down"></div>
    </div>
</template>

<script>

// const { DeckEncoder } = require('runeterra')
import DeckEncoder from '../modules/runeterra/DeckEncoder'
import championCards from '../assets/data/champion.js'
import DeckChamps from './DeckChamps.vue';
import DeckRegions from './DeckRegions.vue';
//https://painttist.github.io/lor-champ-icons/data/champion.js

// function importAll(r) {
//     let images = {};
//     r.keys().map((item, index) => { images[item.replace('./', '')] = r(item); });
//     return images;
// }

// const cardImages = importAll(require.context('../assets/images/cards/cropped/', false, /\.(png|jpe?g|svg)$/));
// const regionImages = importAll(require.context('../assets/images/regions/', false, /\.(png|jpe?g|svg)$/));

export default {
    components: {
        DeckChamps,
        DeckRegions
    },
    data() {
    }, 
    mounted() {
    },
    props: {
        deck: String,
        won: Boolean,
    },
    computed: {
    },
    methods: {
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
        justify-content: flex-start;
        border-radius: 6px;
        align-items: center;
        gap: 5px;
    }

    .icon.cheveron {
        width: 10px;
        padding: 5px;
        margin-left: auto;
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