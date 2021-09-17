<template>

    <div class="left-nav">
        <button class="left-nav-btn disabled"><span><i class="fas fa-user-circle"></i></span></button>
        <button class="left-nav-btn" 
            :class="{selected: currentPage == PAGES.search}" 
            @click="setCurrentPage(PAGES.search)">
            <span><i class="fas fa-search"></i></span>
        </button>
        <button class="left-nav-btn" 
            :class="{selected: currentPage == PAGES.leaderboard}" 
            @click="setCurrentPage(PAGES.leaderboard)">
            <span><i class="fas fa-trophy"></i></span>
        </button>
    </div>
    
    <base-window-controls :title="''" :titleType="'window'"></base-window-controls>
    
    <div class="content">
        <div class="main-content-container" v-if="currentPage == PAGES.search">
            <div class="region-tabs">
                <div class="region-option" 
                v-for="(region, index) in regions"
                :class="{selected: selectedRegion == region}" 
                :key="index"
                @click="selectRegion(region)">{{region}}</div>
            </div>
            <div class="search-bar-container">
                <div class="search-bar-input-container">
                    <input class="search-bar" 
                        @keyup="searchName" 
                        @keyup.enter="searchHistory"
                        @keyup.up="autoCompleteIndexMinus"
                        @keyup.down="autoCompleteIndexPlus"
                        v-model="searchText"
                        placeholder="eg.Storm#5961"
                        />
                    <button class="search-btn inside" @click="clearSearch" v-if="searchText!=''"><span><i class="fas fa-times"></i></span></button>
                </div>
                <div class="search-bar-auto-complete">
                    <div class="auto-complete-item" 
                        v-for="(name, index) in filteredInputNameList" :key="index" 
                        :class="{selected: autoCompleteIndex == index}"
                        @click="searchHistoryAutoComplete(index)"
                    >
                        {{name}}
                    </div>
                </div>
                
                <button class="search-btn" @click="searchHistory">
                    <span v-if="!isSameSearch"><i class="fas fa-search"></i></span>
                    <span v-if="isSameSearch"><i class="fas fa-redo-alt"></i></span>
                </button>
            </div>
            <div class="player-name" v-if="!isLoading">{{playerName}}</div>
            <div class="summary-container" v-if="!isLoading">
                <div class="player-summary">
                    <!-- <div class="detail server">Server: SEA</div> -->
                    <div class="detail rank" v-if="playerRank">
                        <span class="pre-info"><i class="fas fa-trophy"></i></span> 
                        {{playerRank}}</div>
                    <div class="detail lp" v-if="playerLP">
                        <span class="pre-info"><i class="iconfy">LP</i></span>
                        {{playerLP}}</div>
                    <div class="detail region" v-if="playerRegion">
                        <span class="pre-info"><i class="fas" :class="'fa-globe-'+playerRegion"></i></span>
                        {{playerRegionFC}}</div>
                </div>
                <div class="decks-summary" @wheel.prevent="horizontalScroll">
                    <div class="champion-icons btn" 
                    v-for="(deck, index) in uniqueDeckCodes" :key="index"
                    :class="{active: filterDeckCode == deck}"
                    @click="setFilterDeckCode(deck)">
                        <deck-champs :deck="deck" :showRegion="true"></deck-champs>
                    </div>
                </div>
                <div class="history-summary">
                    <div class="winrate" v-if="winrate">{{winrate}} <span class="subtext">WIN</span></div>
                    <div class="winloss" v-if="winloss">{{winloss}}</div>
                </div>
                <!-- <div class="history-chart">
                    <div class="decks-filter">
                        <div class="deck-option">Lee Zoe</div>
                        <div class="deck-option">Azir Irelia</div>
                    </div>
                </div> -->
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
                ></match-history>
                
            </div>

            <div class="loading-text" v-if="isLoading">
                <i class="fas fa-circle-notch fa-spin"></i> 
                Loading...
            </div>
        </div>

        <div class="main-content-container leaderboard" v-if="currentPage == PAGES.leaderboard">
            <leaderboard @search="searchPlayer($event)"></leaderboard>
        </div>
    </div>

    <div class="deck-content-container" :class="{hidden: !isShowDeck}">
        <div class="deck-content-top-bar">
            <button class="collapse-btn" @click="hideDeck"><span><i class="fas fa-chevron-right"></i></span></button>
            <deck-regions :deck="deckCode"></deck-regions>
        </div>
        <div class="deck-content-detail">
            <match-history-deck-detail :deck="deckCode"></match-history-deck-detail>
        </div>
    </div>

    <div class="bottom-bar">
        <div class="left">
            <div class="status">LoR Master Tracker</div>
        </div>
        <div class="right">
            <div class="version download tooltip" v-if="!isUpdatedVersion" @click="openURL(downloadUrl)">
                <span class="tooltiptext">
                    <i class="fas fa-arrow-to-bottom"></i> {{remoteVersion}}
                </span>
                <i class="fas fa-exclamation-triangle"></i> {{version}}</div>
            <div class="version tooltip" v-if="isUpdatedVersion">
                <span class="tooltiptext">
                    <i class="fas fa-check"></i> Updated
                </span>
                {{version}}</div>
        </div>
    </div>
</template>

<script>

import BaseWindowControls from '../components/BaseWindowControls.vue'
import axios from 'axios'
import MatchHistory from '../components/MatchHistory.vue'
import DeckRegions from '../components/DeckRegions.vue'
import DeckChamps from '../components/DeckChamps.vue'
import MatchHistoryDeckDetail from '../components/MatchHistoryDeckDetail.vue'
import Leaderboard from '../components/Leaderboard.vue'

const requestDataWaitTime = 400 //ms
const inputNameListLength = 10;

const portNum = "63312"
const API_BASE = `http://127.0.0.1:${portNum}`

let cancelToken

const regionNames = {
    'NA': 'americas',
    'EU': 'europe',
    'AS': 'asia',
}

const regionShort = {
    'americas': 'NA',
    'europe' : 'EU',
    'asia' : 'AS',
}

const PAGES = {
    search: 0,
    leaderboard: 1
}

function firstCap(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function processDate(dateString) {
    var time
    var date = new Date(dateString)

    var milliElapsed = Date.now() - date
    var secondsElapsed = milliElapsed / 1000
    var minElapse = secondsElapsed / 60
    var hoursElapse = minElapse / 60
    var daysElapsed = hoursElapse / 24

    if (secondsElapsed < 60) {
        time = Math.floor(secondsElapsed) + " sec. ago"
    } else if (minElapse < 60) {
        time = Math.floor(minElapse) + " min. ago"
    } else if (hoursElapse < 24) {
        if (Math.floor(hoursElapse) == 1) {
            time = Math.floor(hoursElapse) + " hour ago"
        } else {
            time = Math.floor(hoursElapse) + " hours ago"
        }
    } else if (daysElapsed < 7) {
        if ( Math.floor(daysElapsed) == 1) {
            time = Math.floor(daysElapsed) + " day ago"
        } else {
            time = Math.floor(daysElapsed) + " days ago"
        }
    } else {
        time = date.toLocaleDateString()
    }

    return time
}

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

export default {
    mounted() {
        console.log("Mounted")
        // var test = 'Hello'
        this.requestVersionData()
    },
    components: { 
        BaseWindowControls,
        MatchHistory,
        DeckRegions,
        MatchHistoryDeckDetail,
        Leaderboard,
        DeckChamps
    },
    data() {
        return {
            // rawDataString: null,
            deckCode: null,
            isShowDeck: false,
            matches: null,
            playerName: "",
            playerTag: "",
            playerRank: null,
            playerLP: null,
            playerRegion: null,
            searchText: "",
            isLoading: false,
            inputNameList: [],
            autoCompleteIndex: -1,
            regions: ["NA", "EU", "AS"],
            selectedRegion: "NA",

            version: "",
            remoteVersion: "",
            downloadUrl: null,

            currentPage: PAGES.search,

            PAGES: PAGES,

            filterDeckCode: null,
        }
    },
    computed: {
        isUpdatedVersion() {
            return this.version == this.remoteVersion
        },
        filteredInputNameList() {
            return this.inputNameList.map(i => i.split('#')[0]);
        },
        isSameSearch() {
            return ((this.searchText == this.playerName) && (this.playerTag) && (this.selectedRegion == regionShort[this.playerRegion]))
        },
        uniqueDeckCodes() {
            if (!this.matches) return null
            // console.log(frequencies(this.matches.map(x => x.deck)))
            return this.matches.map(x => x.deck).filter(filterUnique)
        },
        filteredMatches() {
            if (!this.matches) return null
            if (!this.filterDeckCode) return this.matches.filter(n => n) // filters out null decks
            return this.matches.filter(x => x.deck == this.filterDeckCode) // filters according to deck code
        },
        playerRegionFC() {
            return firstCap(this.playerRegion)
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
            return `${this.totalWins}W ${loss}L`
        },
        winrate() {
            if (!this.filteredMatches) return null
            return Math.floor(this.totalWins/this.totalMatches*100) + "%"
        },
    },
    methods: {
        // Support Functions
        animateScroll(el, distance, duration) {
            var scrollAmount = 0;
            // Duration in seconds
            // var step = distance / duration / fps;
            // var interval = 1000 / fps;

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

            // var slideTimer = setInterval(
                
            // function(){
            //     el.scrollLeft += step;
            //     scrollAmount += step;
            //     if(Math.abs(scrollAmount) >= Math.abs(distance)){
            //         window.clearInterval(slideTimer);
            //     }
            // }, interval);
        },
        horizontalScroll(event) {
            var el = event.currentTarget

            if (event.deltaY > 0) {
                // el.scrollLeft += 100;
                this.animateScroll(el, 100, 300);
            } else {
                // el.scrollLeft -= 100;
                this.animateScroll(el, -100, 300);
            }

            // console.log("deltaY:", event.deltaY)
            // console.log("wheelDelta:", event.wheelDelta)

            // console.log("scrollLeft:", el.scrollLeft)
        },
        // Page Switch
        setCurrentPage(page) {
            this.currentPage = page
        },
        selectRegion(region) {
            this.selectedRegion = region
            var searchBar = document.querySelector(".search-bar")
            if (searchBar) searchBar.focus()
            
            this.searchName()
        },
        searchPlayer(data) {

            // console.log("Search Player", data)
            
            if (this.regions.includes(data.region)) {
                // SEA will not be included
                this.setCurrentPage(PAGES.search)
                this.selectRegion(data.region)
                this.searchText = data.name
                this.resetInputFocus()

                // this.searchHistory()
                this.playerName = data.name
                this.playerTag = data.tag
                this.requestHistoryData()
            }

            // console.log(data)
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

        // Search bar
        clearSearch() {
            this.searchText = ''
            this.searchName()
            document.querySelector(".search-bar").focus()
        },
        searchName() {
            // console.log("searchName")
            if (this.searchText.length > 0) {
                this.requestNameData()
            } else {
                this.resetInputNameList()
            }
        },
        resetInputNameList() {
            // console.log("resetList")
            this.inputNameList = []
            this.autoCompleteIndex = -1
        },
        resetInputFocus() {
            var searchBar = document.querySelector(".search-bar")
            if (searchBar) searchBar.blur()
            this.resetInputNameList()
        },
        autoCompleteIndexPlus() {
            this.autoCompleteIndex += 1
            if (this.autoCompleteIndex > inputNameListLength - 1) {
                this.autoCompleteIndex = inputNameListLength - 1
            }
        },
        autoCompleteIndexMinus() {
            this.autoCompleteIndex -= 1
            if (this.autoCompleteIndex < -1) {
                this.autoCompleteIndex = -1
            }
        },
        searchHistoryAutoComplete(index) {
            this.autoCompleteIndex = index
            this.searchHistory()
        },
        searchHistory() {
            var splited
            if (this.inputNameList.length > 0 && this.inputNameList[this.autoCompleteIndex]) {
                // Use auto complete to fill the search
                // Sets player info for search
                splited = this.inputNameList[this.autoCompleteIndex].split("#")
                this.playerName = splited[0]
                this.playerTag = splited[1]

                this.searchText = this.playerName
                this.resetInputFocus()

                // Perform the actual search
                this.requestHistoryData()
            } else {
                // Use user input
                splited = this.searchText.split("#")
                if (splited.length == 2 && splited[0].length > 0 && splited[1].length > 0) {
                    // Check if format is correct
                    // Sets player info for search
                    this.playerName = splited[0]
                    this.playerTag = splited[1]

                    // Perform the actual search
                    this.requestHistoryData()
                    this.resetInputFocus()
                } else {
                    if (splited.length == 1 && splited[0] == this.playerName && this.playerTag) {
                        // When trying to search the same people, do a refresh
                        this.requestHistoryData()
                        this.resetInputFocus()
                    }
                }
            }
            
        },
        // requestDataAgain() {
        //     return new Promise(resolve => {
        //         setTimeout(() => {
        //             resolve('Requesting new Data')
        //         }, requestDataWaitTime);
        //     })
        // },
        clearInfo() {
            this.playerName = ""
            this.playerTag = ""
            this.playerRank = null
            this.playerLP = null
            this.playerRegion = null
            this.filterDeckCode = null
            this.matches = []
        },
        errorHistory() {
            this.clearInfo()
            this.playerName = "No history found"
        },
        processHistoryData(data) {
            this.matches = []
            this.playerRank = null
            this.playerLP = null
            this.filterDeckCode = null
            // var totalWins = 0
            // var totalLoss = 0
            // var totalMatches = data.length

            // console.log(data)
            for (var key in data) {
                // console.log(data[key])

                if (!data[key]) continue // Skip if null history

                var isFirstPlayer = data[key].player_info[0].name.toLowerCase() == this.playerName.toLowerCase()
                
                var player, playerGame, opponent, opponentGame;
                var info = data[key].info
                
                var opponentName, opponentRank, opponentLp, opponentTag, opponentDeck, 
                    deck, rounds, win, time, order;
                
                if (isFirstPlayer) {
                    playerGame = info.players[0]
                    opponentGame = info.players[1]

                    player = data[key].player_info[0]
                    opponent = data[key].player_info[1]
                } else {
                    playerGame = info.players[1]
                    opponentGame = info.players[0]

                    player = data[key].player_info[1]
                    opponent = data[key].player_info[0]
                }

                if (!playerGame || !opponentGame || !player || !opponent) continue;

                this.playerName = player.name
                opponentName = opponent.name
                
                opponentRank = opponent.rank
                opponentLp = opponent.lp
                opponentTag = opponent.tag

                if (!this.playerRank) this.playerRank = player.rank
                if (!this.playerLP) this.playerLP = player.lp
                
                deck = playerGame.deck_code
                opponentDeck = opponentGame.deck_code
                order = playerGame.order_of_play
                win = playerGame.game_outcome == "win"
                // if (win) {
                //     totalWins += 1
                // } else {
                //     totalLoss += 1
                // }
                rounds = info.total_turn_count
                var badges = []
                if (info.game_mode) badges.push(info.game_mode.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))
                if (info.game_type) badges.push(info.game_type.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))

                time = processDate(info.game_start_time_utc)

                this.matches.push({
                    opponentName: opponentName,
                    deck: deck,
                    region: regionShort[this.playerRegion],
                    opponentDeck: opponentDeck,
                    opponentRank: opponentRank,
                    opponentLp: opponentLp,
                    opponentTag: opponentTag,
                    rounds: rounds,
                    win: win,
                    time: time,
                    badges: badges,
                })
            }
        },
        openURL(url) {
            window.openExternal(url);
        },
        requestVersionData() {
            axios.get(`${API_BASE}/version`)
                .then((response) => {
                    var data = response.data
                    this.version = data.version
                    this.remoteVersion = data.remoteVersion
                    this.downloadUrl = data.downloadUrl
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        // Console log is cancel
                    } else { 
                        console.log('error', e) 
                        
                        setTimeout(this.requestVersionData, requestDataWaitTime);
                    }
                })
        },
        async requestNameData() {
            
            axios.get(`${API_BASE}/name/${regionNames[this.selectedRegion]}/${this.searchText}`)
                .then((response) => {
                    if (response.data == "Error") {
                        // Error
                    } else {
                        // console.log(response.data)
                        if (document.querySelector(".search-bar") == document.activeElement) {
                            // If the search bar is still in focus
                            this.inputNameList = response.data.slice(0, inputNameListLength);
                        } else {
                            this.resetInputNameList()
                        }
                        
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })
        },
        async requestHistoryData() {

            this.isLoading = true;
            this.inputNameList = [];

            //Check if there are any previous pending requests
            if (typeof cancelToken != typeof undefined) {
                cancelToken.cancel("Operation canceled due to new request.")
            }
            
            //Save the cancel token for the current request
            cancelToken = axios.CancelToken.source()
            
            this.playerRegion = regionNames[this.selectedRegion]
            axios.get(`${API_BASE}/search/${regionNames[this.selectedRegion]}/${this.playerName}/${this.playerTag}`,
                    { cancelToken: cancelToken.token }) // Pass the cancel token
                .then((response) => {
                    this.isLoading = false;

                    if (response.data == "Error") {
                        console.log("History Search Error")
                        this.errorHistory()
                    } else {
                        this.processHistoryData(response.data)
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })

        },
        showDeck(deck) {
            // console.log("Main Show Deck", deck)
            if (this.deckCode == deck && this.isShowDeck == true) {
                this.isShowDeck = false
            } else {
                this.deckCode = deck
                this.isShowDeck = true
            }
            
        },
        hideDeck() {
            this.isShowDeck = false
        },
    },

}

</script>

<style scoped>

    .region-tabs {
        display: flex;
        /* gap: 5px; */
        padding-left: 15px;
    }

    .region-option {
        
        /* color: #ABABAB; */
        cursor: pointer;

        width: 60px;
        height: 30px;

        line-height: 30px;

        /* border: 1px solid #ABABAB; */
        /* border-radius: 4px 4px 0px 0px; */

        align-items: center;
        text-align: center;
        vertical-align: middle;

        font-size: 16px;
        color: var(--col-gold);
        border: 0px;
        border-bottom: 2px transparent solid;
        
    }

    .region-option:hover {
        /* color: white; */
        border-bottom: 2px var(--col-gold) solid;
    }

    .region-option.selected {
        cursor: default;
        /* color: var(--col-background);
        background:white;
        border: 1px solid white;
        border-radius: 4px 4px 0px 0px; */
        color: white;
        border-bottom: 2px var(--col-gold) solid;
    }

    .search-bar-container {
        width: 100%;
        display: flex;
        flex-wrap: nowrap;

        position: relative;
        margin-top: 15px;
    }

    .search-bar-input-container {
        width: 100%;
        position: relative;
    }

    .search-bar {
        width: 100%;
        height: 50px;

        color: white;
        font-size: 16px;

        /* border: 1px solid #FFFFFF;
        box-sizing: border-box;
        border-radius: 0px 4px 4px 4px;
        background: var(--col-background); */

        border: none;
        background-color: var(--col-darker-grey);
        padding: 0px 20px 0px 20px;
        border-radius: 40px;
        box-sizing: border-box;
    }

    .search-bar:focus {
        outline: 0px;
        background: var(--col-dark-grey);
    }

    .search-bar-auto-complete {
        position: absolute;
        top: 50px;
        left: 10px;
        text-align: left;
        background: var(--col-background);
        /* padding: 5px 0px 0px 0px; */
        
        border-radius: 8px;
        overflow: hidden;

        z-index: 2;
    }

    .auto-complete-item {
        padding: 6px 15px 8px 9px;
        cursor: pointer;
    }

    .auto-complete-item:hover, .auto-complete-item.selected {
        background: var(--col-dark-grey);
    }

    .search-btn {
        color: white;
        background: none;
        outline: 0px;
        border: 0px;
        cursor: pointer;
        width: 6%;
        text-align: right;
    }

    .search-btn.inside {
        position: absolute;
        right: 10px;
        width: 36px;
        height: 50px;
    }

    .player-name {
        font-size: 24px;
        margin-top: 15px;
        text-align: left;
    }

    .summary-container {
        margin: 5px 0px 15px 0px;
        display: flex;
        gap: 10px;
        justify-content: space-between;
        align-items: center;
    }

    .match-history-container {
        height: calc(100vh - 320px);
        overflow: scroll;
    }

    .loading-text {
        font-size: 24px;
        margin: 20px 0px;
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
        color: rgba(255,255,255,0.6);
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
        overflow-x: scroll;
        white-space: nowrap;
        width: 55%;
        text-align: left;
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

    .content {
        text-align: center;
        display: block;
        width: calc(100% - 80px);
        min-width: 550px;
        margin-left: 80px;
        margin-top: 43px;
        padding: 10px 40px;
        box-sizing: border-box;
        white-space: normal;
        color: white;
    }

    .deck-content-container {
        display: block;
        position: fixed;
        width: 250px;
        height: calc(100vh - 88px);
        top: 0px;
        right: 0px;

        margin-top: 43px;

        background: var(--col-background);
        /* overflow: scroll; */

        transition: right 0.2s ease;
    }

    .deck-content-container.hidden {
        right: -250px;

    }

    .deck-content-top-bar {
        height: 50px;
        display: flex;
        justify-content: center;
    }

    .collapse-btn {
        display: block;
        position: absolute;
        
        width: 40px;
        height: 50px;

        background: none;
        outline: 0px;
        border: 0px;
        color: white;

        cursor: pointer;
        left: 0px;
    }

    .deck-content-detail {
        height: calc(100vh - 138px);
    }

    .main-content-container {
        margin: auto;
        max-width: 550px;
    }

    .main-content-container.leaderboard {
        height: calc(100vh - 88px);
        overflow: scroll;
    }

    .left-nav {
        position: absolute;
        top: 0;
        left: 0;
        width: 80px;
        height: 100vh;
        background: #282828;
        z-index: 5;
        display: flex;
        flex-direction: column;

        gap: 10px;

        padding-top: 80px;

        box-sizing: border-box;

    }

    .left-nav-btn {
        height: 50px;
        font-size: 24px;
        color: var(--col-gold);
        background: none;
        border: 0px;
        cursor: pointer;
    }

    .left-nav-btn:focus {
        outline: 0px;
    }

    .left-nav-btn.selected {
        color: white;
        cursor: default;
    }

    .left-nav-btn.disabled {
        color: var(--col-grey);
        cursor: default;
    }



    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 45px;
        background: #383838;
        z-index: 6;

        display: flex;
        justify-content: space-between;
        align-items: center;

        color: white;
    }

    .bottom-bar .left, .bottom-bar .right {
        padding: 20px;
    }

    .version.download {
        cursor: pointer;
    }

    .tooltip {
        position: relative;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        display: block;
        /* width: 120px; */
        white-space: nowrap;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px 10px;

        box-sizing: border-box;

        /* Position the tooltip */
        position: absolute;
        z-index: 1;
        bottom: 120%;
        left: 50%;
        transform:translateX(-50%);
        
        
        /* left: 50%; */
        /* margin-left: -50%; */
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
    }

</style>