<template>
    <div class="match" :class="{won: won, loss: !won}">
        <div class="row opponent">
            <!-- <router-link class="opponent-name btn" :to="opponentLink">
                {{opponentName}}
            </router-link> -->
            <p class="match-info-title">
                <!-- {{matches}} / {{total}} -->
                {{useRate}}% Usage
            </p>
            <div class="match-info-badge" v-for="(badge, index) in badges" :key="index">
                <span class="match-info-badge-icon fa" :class="{'fa-clock': badge=='recent', 'fa-angle-double-up': badge=='frequent'}"></span>
                {{badge}}</div>
            <div class="history-info">{{time}}</div>
            <div class="history-info">{{matches}} Games</div>
        </div>
        <div class="row match-history-dots">
            <div class="match-history-summary">{{wonNum}} W - {{lostNum}} L </div>
            <div class="dot" :class="{'won' : isWonGame(index), 'played' : isPlayedGame(index)}" v-for="index in total" :key="index"></div>
            
        </div>
        <div class="row decklist">
            <deck-preview @click="showDeck" :deck="deck" :won="won"></deck-preview>
            <!-- <div class="text-vs">VS</div> -->
            <!-- <deck-preview @click="showDeck" :deck="deck"></deck-preview> -->
        </div>
    </div>

    <deck-detail v-if="visibleDeck == 1" :deck="deck"></deck-detail>
    <!-- <deck-detail v-if="visibleDeck == 2" :deck="opponentDeck"></deck-detail> -->

</template>

<script>

import DeckDetail from '../components/MatchInfoDeckDetail.vue'
import DeckPreview from '../components/MatchInfoDeckPreview.vue'

export default {
    components: {
        DeckDetail,
        DeckPreview,
    },
    mounted() {
        this.subscribeData();
    },
    data() {
        return {
            visibleDeck: 0
        }
    },
    props: {
        opponentName: String,
        rounds: Number,
        deck: String,
        opponentDeck: String,
        winrate: String,
        time: String,
        matches: Number,
        badges: Array,
        total: Number,
        history: String,
    },
    computed: {
        opponentLink() {
            return "/profile/" + this.opponentName
        },
        won() {
            // return parseFloat(this.winrate) > 0.5;
            return true
        },
        useRate() {
            return Math.floor(this.matches / this.total * 100);
        },
        wonNum() {
            return (this.history.match(/W/g)||[]).length
        },
        lostNum() {
            return (this.history.match(/L/g)||[]).length
        }
    }, 
    methods: {
        showDeck() {
            // console.log("Show Deck")
            // console.log(window)
            // console.log(window.testData)
            if (this.visibleDeck == 1)
                this.visibleDeck = 0
            else
                this.visibleDeck = 1
        },
        showOpponentDeck() {
            // console.log("Show Oppo Deck")
            if (this.visibleDeck == 2)
                this.visibleDeck = 0
            else
                this.visibleDeck = 2
        },
        subscribeData() {
            // console.log(window)
        },
        isWonGame(index) {
            var i = index - 1
            // console.log(this.history)
            if (i >= this.history.length) return false
            return (this.history[i] == 'W')
        },
        isPlayedGame(index) {
            var i = index - 1
            // console.log(this.history)
            if (i >= this.history.length) return false
            return (this.history[i] == 'W' || this.history[i] == 'L')
        }
    }
}
</script>

<style scoped>

    .match {
        display: flex;
        width: 100%;
        flex-direction: column;
        background: linear-gradient(60deg, var(--col-grey), var(--col-lighter-grey));
        padding: 5px;
        border-radius: 6px;
        margin-top: 5px;
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
        font-size: 0.8em;
        color: rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.2);
        padding: 5px 10px;
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
        padding: 8px 5px;
        cursor: default;
    }

    .history-info:hover {
        color: rgba(255, 255, 255, 1);
        
    }
    
    .row {
        display: flex;
        align-items: baseline;
    }

    .row.decklist {
        /* justify-content: space-between; */
        justify-content: center;
        align-items: center;
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
    }

    .match-history-dots:hover .match-history-summary {
        opacity: 1;
    }

    

    .match-info-title {
        /* display: block; */
        padding: 5px 5px 5px 5px;
        margin: 0;
        margin-left: 8px;
        margin-right: 5px;
        
        /* padding-bottom: 5px; */
        /* border-radius: 6px; */
        text-decoration: none;

        /* border-bottom: 2px solid transparent; */
        border-radius: 0px;

        cursor: default;
    }

    .btn:hover {
        /* background-color: rgba(255, 255, 255, 0.5); */
        /* text-decoration: underline; */
        /* border-bottom: 1px solid white; */
        cursor: pointer;
    }

</style>