<template>
    <div class="sticky-top">
        <div class="player-name">{{playerName}}</div>
        <div class="summary-container">
            <div class="player-summary">
                <div class="detail rank" v-if="playerRank">
                    <span class="pre-info"><i class="fas fa-trophy"></i></span> 
                    {{playerRank}}</div>
                <div class="detail lp" v-if="playerLP || playerLP === 0">
                    <span class="pre-info"><i class="iconfy">LP</i></span>
                    {{playerLP}}</div>
                <div class="detail region" v-if="playerRegion">
                    <span class="pre-info"><i class="fas" :class="'fa-globe-'+playerRegion"></i></span>
                    {{playerRegionFC}}</div>
            </div>
            <div class="decks-summary" @wheel.prevent="horizontalScroll">
                <div class="champion-icons btn" 
                v-for="(obj, index) in uniqueDeckCodes" :key="index"
                :class="{active: filterDeckCode == obj.deck}"
                @click="setFilterDeckCode(obj.deck)">
                    <deck-champs :deck="obj.deck" :showRegion="true" :fixedWidth="false"></deck-champs>
                </div>
            </div>
            <div class="history-summary">
                <div class="winrate" v-if="winrate">{{winrate}} <span class="subtext">{{$t('dash.winRate')}}</span></div>
                <div class="winloss" v-if="winloss">{{winloss}}</div>
            </div>
        </div>
    </div>

    <div class="match-history-container" v-if="!isLoading">
        <match-history 
            @show-deck="showDeck"
            @search="searchPlayer({region: match.region, name: match.opponentName, tag: match.opponentTag})"
            v-for="(match, index) in filteredMatches" :key="index"
            :opponentName="match.opponentName" 
            :opponentRank="match.opponentRank"
            :opponentLp="match.opponentLp"
            :deck="match.deck"
            :opponentDeck="match.opponentDeck"
            :rounds="match.rounds"
            :win="match.win"
            :time="match.time"
            :badges="match.badges"
            :details="match.details"
        ></match-history>
    </div>
</template>

<script>
import DeckChamps from './DeckChamps.vue';
import MatchHistory from './MatchHistory.vue';


// Some helper math functions
function FLip(x) {
    return 1 - x
}
function Square(x) {
    return x * x
}
function EaseOut(x) {
    return FLip(Square(FLip(x)))
}
function Clamp(x, min, max) {
    return Math.min(Math.max(x, min), max);
}

function filterUnique(value, index, self) {
    return self.indexOf(value) === index;
}

const frequencies = arr =>
    arr.reduce((a, v) => {
        a[v] = a[v] ? a[v] + 1 : 1;
        return a;
    }, {});

function firstCap(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export default {
    components: {
        MatchHistory,
        DeckChamps
    },
    mounted() {
    },
    props: {
        playerName: String,
        playerRank: String,
        playerLP: String,
        playerRegion: String,
        matches: Array,
    },
    data() {
        return {
            filterDeckCode: null,
        }
    },
    emits: {
        search: ({ region, name, tag }) => {
            if (region && name && tag) {
                return true
            } else {
                console.warn('Invalid submit event payload!')
                return false
            }
        },
        showDeck: (deck) => {
            if (deck) {
                return true
            } else {
                return false
            }
        }
    },
    computed: {
        
        playerRegionFC() {
            return this.$t('str.regions.'+this.playerRegion)
        },
        
        uniqueDeckCodes() {
            if (!this.matches) return null
            var decks = this.matches.map(x => x.deck)
            var decks_freq = decks.reduce((a, v) => {
                a[v] = a[v] ? a[v] + 1 : 1;
                return a;
            }, {})
            var decks_freq_array = []
            Object.keys(decks_freq).map(function(key, index) {
                decks_freq_array[index] = {deck: key, num: decks_freq[key]}
            });

            decks_freq_array.sort((a, b) => b.num - a.num)
            // Large num in front

            return decks_freq_array
        },
        filteredMatches() {
            if (!this.matches) return null
            if (!this.filterDeckCode) return this.matches.filter(n => n) // filters out null decks
            return this.matches.filter(x => x.deck == this.filterDeckCode) // filters according to deck code
        },
        totalWins() {
            if (!this.filteredMatches) return null
            return this.filteredMatches.reduce((total, match) => match.win ? total+1 : total, 0) // adds up all the wins
        },
        totalMatches(){
            return this.filteredMatches.length
        },
        winloss() {
            if (!this.filteredMatches) return null
            var loss = this.totalMatches - this.totalWins
            return this.$t('dash.winloss', {win: this.totalWins, loss: loss})
        },
        winrate() {
            if (!this.filteredMatches) return null
            return Math.floor(this.totalWins/this.totalMatches*100) + "%"
        },
        

    },
    methods: {
        // Helpers
        animateScroll(el, distance, duration) {
            var scrollAmount = 0;
            var start, prePos;

            function step(timestamp) {
                if (start === undefined) {
                    start = timestamp;
                    prePos = 0;
                }
                const elapsed = timestamp - start;
                var newPos = distance * EaseOut(Clamp(elapsed / duration, 0, 1))
                
                el.scrollLeft += newPos - prePos;
                prePos = newPos;

                if (elapsed < duration) { // Stop the animation after 2 seconds
                    window.requestAnimationFrame(step);
                }
            }

            window.requestAnimationFrame(step);
        },
        horizontalScroll(event) {
            var el = event.currentTarget

            if (event.deltaY > 0) {
                this.animateScroll(el, 100, 300);
            } else {
                this.animateScroll(el, -100, 300);
            }
        },

        
        // Filter related
        setFilterDeckCode(code) {
            if (this.filterDeckCode == code) {
                // If trying to set the same, clear the filter
                this.filterDeckCode = null
            } else {
                this.filterDeckCode = code
            }
        },

        searchPlayer(data) {
            this.$emit('search', data)
        },

        showDeck(deck) {
            // console.log("Show Deck", deck)
            this.$emit('showDeck', deck)
            // console.log(window)
            // console.log(window.testData)
        },
    }

}
</script>

<style scoped>

    .player-name {
        font-size: 24px;
        padding-top: 15px;
        text-align: left;
    }

    .summary-container {
        padding: 5px 0px 15px 0px;
        display: flex;
        gap: 10px;
        justify-content: space-between;
        align-items: center;
    }

    .match-history-container {
        /* height: calc(100vh - 325px); */
        /* overflow-y: scroll; */
        margin-bottom: 25px;
    }

    
    .player-summary {
        text-align: left;
        width: 20%;
    }

    .player-summary .name {
        font-size: 24px;
        margin-bottom: 5px;
    }

    .player-summary .detail {
        font-size: 12px;
        color: var(--col-lighter-grey);
    }

    .player-summary .detail .pre-info {
        display: inline-block;
        width: 20px;
        border-right: 1px solid var(--col-lighter-grey);
    }

    .player-summary:hover .detail {
        color: var(--col-dark-white);
    }

    .player-summary:hover .detail.rank {
        color: white;
    }

    .iconfy {
        font-size: 0.9em;
        font-weight: 900;
    }

    .decks-summary {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
        width: 55%;
        text-align: left;

        padding-bottom: 5px;
    }

    .decks-summary .champion-icons {
        display: inline-flex;
        padding: 5px;
        border-radius: 50px;
        margin: 0px 2px;
        cursor: pointer;
    }

    .decks-summary .champion-icons:hover {
        background: var(--col-dark-grey);
    }

    .decks-summary .champion-icons.active {
        background: var(--col-light-grey);
    }

    .history-summary {
        font-size: 24px;
        /* margin-left: 20px; */
        text-align: right;
        width: 22%;
    }

    .history-summary .winrate {
        font-size: 24px;
        color: white;
        /* color: var(--col-lighter-grey); */
    }

    .history-summary .winrate .subtext {
        font-size: 0.75em;
        color: white;
    }

    .history-summary .winloss {
        font-size: 18px;
        color: var(--col-lighter-grey);
    }

    .history-summary:hover .winloss {
        color: var(--col-dark-white);
    }

    .sticky-top {
        position: sticky;
        top: 0;
        background: var(--col-background);
        z-index: 1;
    }

    .main-content-container.search .sticky-top{
        position: sticky;
        top: 97px;
        background: var(--col-background);
    }

</style>