<template>
    <div class="deck-detail">
        <cards-preview v-for="(card, index) in cards" :key="index"
        :name="card.name"
        :cost="card.cost"
        :count="card.count"
        :code="card.code"
        >{{card.name}}</cards-preview>
        <div class="deck-code">
            <a :href="deckDetailLink" target="_blank"><span class="link-icon fa fa-external-link-alt"></span>Detail</a>
        </div>
    </div>
</template>

<script>

const { DeckEncoder } = require('runeterra')
import sets from  '../assets/data/allsets-en_us.json'
import CardsPreview from './CardsPreview.vue'
// import set1 from '../assets/data/set1-en_us.json'
// import set2 from '../assets/data/set2-en_us.json'
// import set3 from '../assets/data/set3-en_us.json'
// import set4 from '../assets/data/set4-en_us.json'

export default {
    components: {
        CardsPreview,
    },
    mounted() {
        // this.getCardsInfo()
    },
    data() {
        return {}
    }, 
    props: {
        deck: String,
    },
    computed: {
        deckDetailLink() {
            return "https://lor.mobalytics.gg/decks/code/" + this.deck
        },
        cards() {
            var cards = []
            var deck = DeckEncoder.decode(this.deck)
            for (var j in deck) {
                var cardCode = deck[j].code
                var card = sets.find(card => card.cardCode == cardCode)

                // console.log(cardName, deck[j].count)
                cards.push({code: deck[j].code, name: card.name, count: deck[j].count, cost: card.cost})

            }
            return cards.sort((a, b) => a.cost > b.cost ? 1 : -1)
        }
    },
    methods: {
        getCardsInfo() {
            // console.log(sets[0])
            
        }
    },
    
}
</script>

<style>
    .deck-detail {
        width: 270px;
        /* height: 100px; */
        word-wrap: break-word;
        padding: 10px;
        background-color: var(--col-dark-grey);
        font-size: 0.9em;
    }

    .deck-code {
        margin-top: 10px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        /* gap: 5px; */
    }

    .link-icon {
        padding-right: 5px;
    }

    a {
        color: white;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    /* @media only screen and (max-width: 768px) {
        .deck-detail {
            width: 280px;
        }
    } */
</style>