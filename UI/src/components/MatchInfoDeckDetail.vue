<template>
    <div class="deck-detail" v-if="cards.length > 0">
        <cards-preview v-for="(card, index) in cards" :key="index"
        :name="card.name"
        :cost="card.cost"
        :count="card.count"
        :code="card.code"
        :type="card.type"
        :supertype="card.supertype"
        :set="card.set"
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
import set1 from '../../../data/set1-en_us.json'
import set2 from '../../../data/set2-en_us.json'
import set3 from '../../../data/set3-en_us.json'
import set4 from '../../../data/set4-en_us.json'
import set5 from '../../../data/set5-en_us.json'


const sets = set1.concat(set2, set3, set4, set5)
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
            var deck = null
            try { deck = DeckEncoder.decode(this.deck) } catch(err) {
                // console.log(cards)
                return cards
            }
            
            for (var j in deck) {
                var cardCode = deck[j].code
                var card = sets.find(card => card.cardCode == cardCode)
                if (card) {
                    // console.log(cardName, deck[j].count)
                    cards.push({
                        code: deck[j].code, 
                        name: card.name, 
                        count: deck[j].count, 
                        cost: card.cost, 
                        type: card.type, 
                        supertype: card.supertype,
                        set: card.set
                    })
                }

            }
            // console.log(cards)
            return cards.sort(function (a, b) { 
                // if (a.type > b.type) {
                //     return 1; 
                // } if (a.supertype > b.supertype) {
                //     return 1;
                // }  else {
                //     return a.cost > b.cost ? 1 : -1
                // }
                // if (a.type == "Unit" && b.type == "Spell") {
                //     return 1
                // }
                if (a.supertype == b.supertype) {
                    if (a.type == b.type) {
                        return a.cost > b.cost ? 1 : -1
                    }
                    return a.type > b.type ? 1 : -1
                }
                return a.supertype < b.supertype ? 1 : -1
            })
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
        width: 100%;
        box-sizing: border-box;
        /* height: 100px; */
        word-wrap: break-word;
        padding: 0px 4px 8px 4px;
        background-color: var(--col-background);
        font-size: 0.9em;
        border-radius: 5px;
    }

    .actions {
        margin-top: 8px;
        margin-right: 8px;
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