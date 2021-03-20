<template>
    <div class="deck-detail">
        <cards-preview v-for="(card, index) in cards" :key="index"
        :name="card.name"
        :cost="card.cost"
        :count="card.count"
        :code="card.code"
        >{{card.name}}</cards-preview>
        <div class="actions">
            <!-- <a class="actions-btn" :href="deckDetailLink" target="_blank"><span class="actions-icon fa fa-external-link-alt"></span>Detail</a> -->
            <div class="actions-btn" @click="openURL(deckDetailLink)"><span class="actions-icon fa fa-external-link-alt"></span>Detail</div>
            <div class="actions-btn" @click="copyDeckcode"><span class="actions-icon far fa-copy"></span>{{copyText}}</div>
        </div>
    </div>
</template>

<script>

// const { DeckEncoder } = require('runeterra')
import DeckEncoder from '../modules/runeterra/DeckEncoder'
// import sets from  '../assets/data/allsets-en_us.json'
import CardsPreview from './CardsPreview.vue'
import set1 from '../assets/data/set1-en_us.json'
import set2 from '../assets/data/set2-en_us.json'
import set3 from '../assets/data/set3-en_us.json'
import set4 from '../assets/data/set4-en_us.json'


const sets = set1.concat(set2, set3, set4)
// console.log(sets)

export default {
    components: {
        CardsPreview,
    },
    mounted() {
        // this.getCardsInfo()
    },
    data() {
        return {
            copied: false,
        }
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
                if (card) {
                    // console.log(cardName, deck[j].count)
                    cards.push({code: deck[j].code, name: card.name, count: deck[j].count, cost: card.cost})
                }

            }
            return cards.sort((a, b) => a.cost > b.cost ? 1 : -1)
        },
        copyText() {
            return this.copied ? 'Copied!' : 'Copy'
        }
    },
    methods: {
        copyDeckcode() {
            const copyToClipboard = str => {
              const el = document.createElement('textarea');
              el.value = str;
              el.setAttribute('readonly', '');
              el.style.position = 'absolute';
              el.style.left = '-9999px';
              document.body.appendChild(el);
              const selected =
                document.getSelection().rangeCount > 0
                  ? document.getSelection().getRangeAt(0)
                  : false;
              el.select();
              document.execCommand('copy');
              document.body.removeChild(el);
              if (selected) {
                document.getSelection().removeAllRanges();
                document.getSelection().addRange(selected);
              }
            };

            copyToClipboard(this.deck)
            this.copied = true
            setTimeout(() => {this.copied = false}, 1250)
        },
        openURL(url) {
            window.openExternal(url);
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

    .actions {
        margin-top: 10px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        /* gap: 5px; */
    }

    .actions-btn {
        margin-left: 10px;
        cursor: pointer;
    }

    .actions-btn:hover {
        text-decoration: none;
    }

    .actions-icon {
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