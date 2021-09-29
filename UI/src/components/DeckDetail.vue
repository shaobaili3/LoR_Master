<template>
    <div class="deck-detail" 
    :class="{'fixed-height': fixedHeight}"
    v-if="cards.length > 0">
        <cards-preview v-for="(card, index) in cards" :key="index"
        :name="card.name"
        :cost="card.cost"
        :count="card.count"
        :code="card.code"
        :type="card.type"
        :supertype="card.supertype"
        :set="card.set"
        :locale="locale"
        >{{card.name}}</cards-preview>
    </div>
    <div class="actions" 
    :class="{'fixed-height': fixedHeight}"
    v-if="showCopy">
        <!-- <a class="actions-btn" :href="deckDetailLink" target="_blank"><span class="actions-icon fa fa-external-link-alt"></span>Detail</a> -->
        <div class="actions-btn" v-if="showURL" @click="openURL(deckDetailLink)"><span class="actions-icon fa fa-external-link-alt"></span>Detail</div>
        <div class="actions-btn" @click="copyDeckcode"><span class="actions-icon far fa-copy"></span>{{copyText}}</div>
    </div>
</template>

<script>

// const { DeckEncoder } = require('runeterra')
import DeckEncoder from '../modules/runeterra/DeckEncoder'
// import sets from  '../assets/data/allsets-en_us.json'
import CardsPreview from './CardsPreview.vue'
import set1 from '../../../Resource/set1-en_us.json'
import set2 from '../../../Resource/set2-en_us.json'
import set3 from '../../../Resource/set3-en_us.json'
import set4 from '../../../Resource/set4-en_us.json'
import set5 from '../../../Resource/set5-en_us.json'


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
        baseDeck: String,
        showCopy: {
            type: Boolean,
            default: true,
        },
        showURL: {
            type: Boolean,
            default: false,
        },
        fixedHeight: {
            type: Boolean,
            default: false,
        },
        locale: {
            type: String,
            default: 'en_us'
        }
    },
    computed: {
        deckDetailLink() {
            return "https://lor.mobalytics.gg/decks/code/" + this.baseDeck
        },
        cards() {
            var cards = []
            var deck = null
            if (this.deck) try { deck = DeckEncoder.decode(this.deck) } catch(err) {
                console.log(err)
                // return cards
            }
            
            var baseDeck = null
            if (this.baseDeck) try { baseDeck = DeckEncoder.decode(this.baseDeck) } catch(err) {
                console.log(err)
                // return cards
            }

            if (baseDeck) {
                // make sure cards not in current Deck are shown
                for (var j in baseDeck) {
                    // Loop through base deck
                    var cardCode = baseDeck[j].code
                    // Get full information from the sets collection
                    var card = sets.find(card => card.cardCode == cardCode)
                    var cardCount = baseDeck[j].count
                    
                    if (deck) {
                        // make sure currentDeck exist
                        
                        // Finding the same card in current deck
                        var currentCard = deck.find(card => card.code == cardCode)
                    
                        // Get the current card copy count
                        if (currentCard) {
                            cardCount = currentCard.count
                        } else {
                            cardCount = 0
                        }
                    }

                    if (card) {
                        cards.push({
                            code: cardCode, 
                            name: card.name,
                            count: cardCount, 
                            cost: card.cost, 
                            type: card.type, 
                            supertype: card.supertype,
                            set: card.set
                        })
                    }

                }
            }

            return cards.sort(function (a, b) {
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

            copyToClipboard(this.baseDeck)
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
        color: white;
    }

    .deck-detail.fixed-height {
        height: 100%;
        overflow: scroll;
    }

    .actions {    
        width: 100%;
        padding: 8px;

        box-sizing: border-box;

        display: flex;
        justify-content: flex-end;
        align-items: center;
        background: var(--col-background);

        color: white;
    }

    .actions.fixed-height {
        position: absolute;
        bottom: 0px;
        right: 0px;
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