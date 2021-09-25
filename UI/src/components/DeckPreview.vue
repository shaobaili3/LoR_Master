<template>
    <div class="row deck btn" :class="{won: won, loss: !won, cheveron: cheveron}">
        <deck-regions :deck="deck"></deck-regions>
        <deck-champs :deck="deck"></deck-champs>
        <div v-if="cheveron" class="icon cheveron fa fa-chevron-down"></div>
    </div>
</template>

<script>

import DeckEncoder from '../modules/runeterra/DeckEncoder'
import championCards from '../assets/data/champion.js'
import DeckChamps from './DeckChamps.vue';
import DeckRegions from './DeckRegions.vue';
//https://painttist.github.io/lor-champ-icons/data/champion.js

export default {
    components: {
        DeckChamps,
        DeckRegions,
    },
    data() {
    }, 
    mounted() {
    },
    props: {
        deck: String,
        won: Boolean,
        cheveron: {
            type: Boolean,
            default: false,
        },
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
        justify-content: center;
        border-radius: 6px;
        align-items: center;
        gap: 5px;
    }

    .row.deck.cheveron {
        justify-content: flex-start;
    }

    .icon.cheveron {
        width: 10px;
        padding: 5px;
        margin-left: auto;
    }

    .btn.won:hover {
        background-color: var(--col-gold);
        cursor: pointer;
    }

    .btn.loss:hover {
        background-color: var(--col-lighter-grey);
        cursor: pointer;
    }

    @media screen and (max-width: 275px) {
        .icon {
            width: 15px;
            height: 15px;
        }
    }

</style>