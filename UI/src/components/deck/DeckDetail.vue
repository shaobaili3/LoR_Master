<template>
<div class="w-full">
    <div class="deck-detail" 
    :class="{'fixed-height': fixedHeight}"
    v-if="cards.length > 0">
        <card-preview v-for="(card, index) in cards" :key="index"
        :name="card.name"
        :cost="card.cost"
        :count="card.count"
        :code="card.code"
        :type="card.type"
        :supertype="card.supertype"
        :set="card.set"
        :typeRef="card.typeRef"
        >{{card.name}}</card-preview>
    </div>
    <div class="actions" 
    :class="{'fixed-height': fixedHeight}"
    v-if="showCopy && this.baseDeck">
        <!-- <a class="actions-btn" :href="deckDetailLink" target="_blank"><span class="actions-icon fa fa-external-link-alt"></span>Detail</a> -->
        <div class="actions-btn" v-if="showURL" @click="openURL(deckDetailLink)"><span class="actions-icon fa fa-external-link-alt"></span>Detail</div>
        <div class="actions-btn tooltip" @click="copyDeckcode"><span class="actions-icon far fa-copy"
            :class="{'fa-exclamation-triangle': !isValid}"
        ></span>{{copyText}}
            <div class="tooltiptext top-end" v-if="!isValid">{{$t('tooltips.incompleteDeck')}}</div>
        </div>
    </div>
</div>
</template>

<script>

import DeckEncoder from '../../modules/runeterra/DeckEncoder'
import CardPreview from './CardPreview.vue'

export default {
    components: {
        CardPreview,
    },
    mounted() {
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
        extra: {
            type: Array,
            default: () => [],
        }
    },
    watch: {
        // locale(newLoacle, oldLocale) {
        //     this.loadSetsJson(newLoacle)
        // }
    },
    computed: {
        deckDetailLink() {
            return "https://lor.mobalytics.gg/decks/code/" + this.baseDeck
        },
        cards() {
            var cards = []

            if( this.sets == null ) return cards
            
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

            // Append extra played cards to baseDeck
            if (baseDeck && this.extra) {
                baseDeck = baseDeck.concat(this.extra)
            }

            if (baseDeck) {
                // make sure cards not in current Deck are shown
                // console.log("baseDeck", baseDeck)
                // console.log("extra", this.extra)
                for (var j in baseDeck) {
                    // Loop through base deck
                    var cardCode = baseDeck[j].code
                    // Get full information from the sets collection
                    var card = this.sets.find(card => card.cardCode == cardCode)
                    var cardCount = baseDeck[j].count
                    var baseCount = baseDeck[j].count
                    
                    // Append extra played cards to playedDeck as well?
                    // deck = deck.concat(this.extra)

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

                        var typeRef = ""
                        if (card.supertype != "" || card.rarityRef == "Champion") {
                            typeRef = "Champion"
                        } else if (card.spellSpeedRef != "") {
                            typeRef = "Spell"
                        } else if (card.keywordRefs && card.keywordRefs.includes("LandmarkVisualOnly")) {
                            typeRef = "Landmark"
                        } else {
                            typeRef = "Unit"
                        }

                        cards.push({
                            code: cardCode, 
                            name: card.name,
                            count: cardCount,
                            baseCount: baseCount,
                            cost: card.cost, 
                            type: card.type,
                            typeRef: typeRef,
                            supertype: card.supertype,
                            set: card.set
                        })
                    } else if (cardCode && cardCount) {
                        cards.push({
                            code: cardCode, 
                            // name: `?`.repeat(Math.floor( 2 + Math.random() * 4)) + `${Math.random() > 0.35 ? ' ': ''}` + `?`.repeat(Math.floor( 2 + Math.random() * 4)),
                            name: "???",
                            count: cardCount,
                            baseCount: baseCount,
                            cost: "?", 
                            type: "Unknown",
                            typeRef: "Unknown",
                            supertype: null,
                            set: "1",
                        })
                    }

                }
            }
            // console.log(cards)
            return cards.sort(function (a, b) {
                if (a.type === "Unknown") {
                    return 1
                }
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
            return this.copied ? this.$t('str.copied') : this.$t('str.copy')
        },
        isValid() {
            return this.cards.reduce((prev, card) => {
                return prev + card.baseCount
            }, 0) == 40
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
        overflow-y: scroll;
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