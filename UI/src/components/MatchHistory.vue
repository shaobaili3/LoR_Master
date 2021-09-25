<template>
    <div class="match" :class="{won: won, loss: !won}">
        <div class="row opponent">
            <p @click="search" class="match-info-title">
                vs <span class="name">{{opponentName}}</span>
            </p>
            <div class="opponent-info" v-if="opponentRank"><i class="fas fa-trophy"></i> {{opponentRank}}</div>
            <div class="history-info">{{time}}</div>
            <div class="history-info">{{rounds}} rounds</div>
            <div class="match-info-badge" v-for="(badge, index) in filteredBadges" :key="index" >
                <span v-if="badge=='recent' || badge=='frequent'" class="match-info-badge-icon fa" :class="{'fa-clock': badge=='recent', 'fa-angle-double-up': badge=='frequent'}"></span>
                {{badge}}</div>
        </div>
        <div class="row decklist">
            <deck-preview @click="showDeck(deck)" :deck="deck" :won="won"></deck-preview>
            <!-- <div class="text-vs">VS</div> -->
            <!-- <deck-preview @click="showDeck" :deck="deck"></deck-preview> -->
            <span class="vs-text">VS</span>
            <deck-preview @click="showDeck(opponentDeck)" :deck="opponentDeck" :won="won"></deck-preview>
        </div>
    </div>

    <!-- <deck-detail v-if="visibleDeck == 1" :deck="deck"></deck-detail> -->
    <!-- <deck-detail v-if="visibleDeck == 2" :deck="opponentDeck"></deck-detail> -->

</template>

<script>

import DeckPreview from '../components/DeckPreview.vue'

export default {
    components: {
        DeckPreview,
    },
    mounted() {
    },
    data() {
        return {
            visibleDeck: 0
        }
    },
    emits: ['showDeck', 'search'],
    props: {
        opponentName: String,
        opponentRank: String,
        opponentLp: String,
        rounds: Number,
        deck: String,
        opponentDeck: String,
        win: Boolean,
        time: String,
        badges: Array,
    },
    computed: {
        opponentLink() {
            return "/profile/" + this.opponentName
        },
        won() {
            // return parseFloat(this.winrate) > 0.5;
            return this.win
        },
        filteredBadges() {
            if (!this.badges) return null
            var filtered = this.badges.map(b => b.trim()).filter((badge, pos, self) => {
                // remove "Constructed" and duplicates
                return !badge.includes("Constructed") && self.indexOf(badge) == pos
                })
            return filtered
        }
    },
    methods: {
        showDeck(deck) {
            // console.log("Show Deck", deck)
            this.$emit('showDeck', deck)
            // console.log(window)
            // console.log(window.testData)
        },
        search() {
            // console.log("Match History Search")
            this.$emit('search')
        },
        showOpponentDeck() {
            // console.log("Show Oppo Deck")
            if (this.visibleDeck == 2)
                this.visibleDeck = 0
            else
                this.visibleDeck = 2
        },
    }
}
</script>

<style scoped>

    

    .match {
        display: flex;
        width: 100%;
        flex-direction: column;
        background: linear-gradient(60deg, var(--col-grey), var(--col-lighter-grey));
        box-sizing: border-box;
        padding: 5px;
        border-radius: 6px;
        
        overflow: hidden;

        border-left: 3px solid var(--col-background);
        border-right: 3px solid var(--col-background);
        margin-top: 4px;

        font-size: 1em;
    }

    .match.won {
        /* background: linear-gradient(-60deg,rgb(224, 171, 24), rgb(78, 78, 78) 60%); */
        /* box-shadow: inset 0px 0px 0px 2px var(--col-gold); */
        background: linear-gradient(60deg, var(--col-dark-gold), var(--col-gold));
        /* box-shadow: 2px solid gold; */
        /* background: linear-gradient(90deg,rgb(224, 171, 24) 1%, rgb(94, 94, 94) 1%); */
    }

    .match.loss {
        /* background: linear-gradient(300deg,rgb(224, 171, 24), rgb(94, 94, 94)); */
        /* background: linear-gradient(300deg,rgb(224, 171, 24) 20%, rgb(94, 94, 94) 20%); */
        /* background: linear-gradient(-90deg,rgb(224, 171, 24) 1%, rgb(94, 94, 94) 1%); */
    
    }

    .match-info-badge-icon {
        /* margin-right: 3px; */
        /* width: 10px; */
        /* display: flex; */
        /* align-content: center; */
        /* justify-content: center; */
    }

    .match-info-badge {
        font-size: 0.7em;
        color: rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.2);
        padding: 3px 8px;
        margin-right: 5px;
        border-radius: 50px;
        cursor: default;
    }

    .match-info-badge:hover {
        color: rgba(255, 255, 255, 1);
        background: rgba(255, 255, 255, 0.3);
    }

    .history-info {
        font-size: 0.8em;
        color: rgba(255, 255, 255, 0.7);
        padding: 8px 6px;
        cursor: default;
        white-space: nowrap;
    }

    .history-info:hover {
        color: rgba(255, 255, 255, 1);
    }

    .opponent-info {
        font-size: 0.8em;
        color: rgba(255, 255, 255, 1);
        padding: 8px 6px 8px 0px;
        cursor: default;
        white-space: nowrap;
    }

    .opponent-info i {
        font-size: 0.85em;
    }
    
    .row {
        display: flex;
        align-items: center;
    }


    .row.decklist {
        /* justify-content: space-between; */
        justify-content: center;
        align-items: center;
    }

    .vs-text {
        padding: 0px 10px;
    }

    .match-history-dots {
        display: flex;
        gap: 8px;
        /* height: 20px; */

        justify-content: flex-start;
        align-items: center;

        padding: 2px 2px 5px 2px;
        margin: 0;
        margin-left: 8px;
        margin-right: 8px;
    }

    .row.match-history-dots .dot {
        height: 10px;
        width: 10px;
        border-radius: 10px;

        background-color: var(--col-background);
        opacity: 0.1;
    }

    .row.match-history-dots .dot.played {
        opacity: 0.3;
        background: rgb(255,255,255);
    }

    .row.match-history-dots .dot.played.won {
        opacity: 0.7;
        background: rgb(255,255,255);
    }

    /* .row.match-history-dots:hover .dot {
        display: none;
    } */

    .row.match-history-dots:hover .dot {
        opacity: 0.05;
    }

    .row.match-history-dots:hover .dot.played {
        /* display: initial; */
        opacity: 0.5;
        /* background-color: var(--col-background); */
    }

    .match-history-dots:hover .dot.played.won {
        opacity: 1;
        background: rgb(255,255,255);
        box-shadow: 1px 2px 5px -2px #000000;
    }

    .match-history-summary {
        /* display: block; */
        /* display: flex; */
        /* align-items: center; */
        line-height: 10px;
        height: 10px;
        text-align: center;
        /* height: 20px; */
        /* line-height: 20px; */
        font-size: 0.8em;
        /* display: none; */
        opacity: 0.7;
        white-space: nowrap;
    }

    .match-history-dots:hover .match-history-summary {
        opacity: 1;
    }

    

    .match-info-title {
        /* display: block; */
        padding: 5px 5px 5px 1px;
        margin: 0;
        margin-left: 8px;
        margin-right: 5px;
        
        /* padding-bottom: 5px; */
        /* border-radius: 6px; */
        text-decoration: none;
        white-space: nowrap;

        /* border-bottom: 2px solid transparent; */
        border-radius: 0px;

        cursor: pointer;
    }

    .match-info-title:hover .name {
        text-decoration: underline;
    }

    .btn:hover {
        /* background-color: rgba(255, 255, 255, 0.5); */
        /* text-decoration: underline; */
        /* border-bottom: 1px solid white; */
        cursor: pointer;
    }

    @media screen and (max-width: 275px) {
        .match {
            font-size: 0.85em;
        }

        .match-info-title {
            padding: 3px 3px 3px 1px;
            margin-left: 5px;
        }

        .match-history-dots {
            gap: 5px;
            margin-left: 5px;
        }

        .history-info {
            padding-right: 2px;
        }

    }

</style>