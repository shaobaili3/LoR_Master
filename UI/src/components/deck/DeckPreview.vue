<template>
    <div class="row deck btn" :class="{won: won, loss: !won, cheveron: cheveron}">
        <div class="row" :class="{fixedWidth: fixedWidth}">
            <deck-regions :deck="deck" :fixedWidth="false"></deck-regions>
            <deck-champs :deck="deck" :fixedWidth="!cheveron"></deck-champs>
            <div v-if="cheveron" class="icon cheveron fa fa-chevron-down"></div>
        </div>
    </div>
</template>

<script>

import DeckEncoder from '../../modules/runeterra/DeckEncoder'
import championCards from '../../assets/data/champion.js'
import DeckChamps from './DeckChamps.vue';
import DeckRegions from './DeckRegions.vue';
//https://painttist.github.io/lor-champ-icons/data/champion.js

export default {
    components: {
        DeckChamps,
        DeckRegions,
    },
    data() {
        return {}
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
        fixedWidth: { // 180px vs 100%
            type: Boolean,
            default: false,
        }
    },
    computed: {
    },
    methods: {
    }
}
</script>

<style>

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

    .row.deck .row {
        /* width: 100%; */
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .row.deck .row.fixedWidth {
        width: 160px;
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

    @media screen and (max-width: 190px) {
        .row.deck .row{
            gap: 2px;
            /* padding: 4px 2px; */
        }
    }

</style>