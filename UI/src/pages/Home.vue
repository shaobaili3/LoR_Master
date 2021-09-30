<template>

    <div class="left-nav">
        <button class="left-nav-btn tooltip"
            :class="{
                selected: currentPage == PAGES.my,
                disabled: !hasLocalInfo
            }" 
            @click="(hasLocalInfo && setCurrentPage(PAGES.my)) + requestLocalHistory()"
            :disabled="!hasLocalInfo"
        >
            <span class="icon-default"
                v-if="!localHistoryLoading"
            ><i class="fas fa-user-circle"></i></span>
            <span class="icon-default icon-hover"
                v-if="localHistoryLoading"
            ><i class="fas fa-redo-alt fa-spin-fast"></i></span>
            <span class="icon-hover"
                v-if="!localHistoryLoading"
            ><i class="fas fa-check"></i></span>
            <div class="tooltiptext right" v-if="!hasLocalInfo">{{$t('tooltips.lorlogin')}}</div>
        </button>
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
        <button class="left-nav-btn nav-bottom" 
            :class="{selected: currentPage == PAGES.settings}" 
            @click="setCurrentPage(PAGES.settings)">
            <span><i class="fas fa-cog"></i></span>
        </button>
    </div>
    
    <base-window-controls :title="''" :titleType="'window'"></base-window-controls>
    
    <div class="content">
        <div class="main-content-container" v-if="currentPage == PAGES.my">
            <player-matches v-if="hasLocalInfo" 
                @search="searchPlayer($event)"
                @show-deck="showDeck"
                :playerName="localPlayerInfo.name"
                :playerRegion="localPlayerInfo.server"
                :playerRank="localPlayerInfo.rank"
                :playerLP="localPlayerInfo.lp"
                :matches="localMatches"
            >
            </player-matches>
        </div>

        <div class="main-content-container search" v-if="currentPage == PAGES.search">
            <div class="sticky-top">
                <div class="region-tabs">
                    <div class="region-option" 
                    v-for="(region, index) in regions"
                    :class="{selected: selectedRegion == region}" 
                    :key="index"
                    @click="selectRegion(region)">{{region}}</div>
                </div>
                <div class="search-bar-container">
                    <div class="search-bar-input-container">
                        <button class="search-btn inside left" 
                            :class="{active: searchText!=''}"
                            @click="searchHistory">
                            <span v-if="!isSameSearch"><i class="fas fa-search"></i></span>
                            <span v-if="isSameSearch"><i class="fas fa-redo-alt"></i></span>
                        </button>
                        
                        <input autocomplete='off' class="search-bar" 
                            @keyup="searchName" 
                            @keyup.enter="searchHistory"
                            @keyup.up="autoCompleteIndexMinus"
                            @keyup.down="autoCompleteIndexPlus"

                            @focus="searchName"

                            v-model="searchText"
                            :placeholder="$t('search.player.placeholder')"
                            />
                        <button class="search-btn inside right" @click="clearSearch" v-if="searchText!=''"><span><i class="fas fa-times"></i></span></button>
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
                </div>
            </div>
            <!-- Player Info -->
            <player-matches v-if="!isLoading && playerName" 
                @search="searchPlayer($event)"
                @show-deck="showDeck"
                :playerName="playerName"
                :playerRegion="playerRegion"
                :playerRank="playerRank"
                :playerLP="playerLP"
                :matches="matches"
            >
            </player-matches>

            <div class="loading-text" v-if="isLoading">
                <i class="fas fa-circle-notch fa-spin"></i> 
                {{$t('str.loading')}}
            </div>
        </div>

        <div class="main-content-container leaderboard" v-if="currentPage == PAGES.leaderboard">
            <leaderboard :apiBase="apiBase" @search="searchPlayer($event)"></leaderboard>
        </div>

        <div class="main-content-container settings" v-if="currentPage == PAGES.settings">
            <div class="title">{{$t('str.settings')}}</div>
            <div class="settings-list">
                <div class="settings-list-item">
                    <div class="settings-title">{{ $t('settings.options.autoLaunch') }} {{autoLaunch ? $t('settings.enabled') : $t('settings.disabled')}}</div>
                    <button class="settings-btn" v-if="autoLaunch" @click="setAutoLaunch(false)">{{ $t('settings.disable') }}</button>
                    <button class="settings-btn" v-if="!autoLaunch" @click="setAutoLaunch(true)">{{ $t('settings.enable') }}</button>
                </div>
                <div class="settings-list-item">
                    <locale-changer></locale-changer>
                </div>
            </div>

            <!-- <div class="debug-info">
                {{debugInfos}}
            </div> -->
        </div>
    </div>

    <div class="deck-content-container" :class="{hidden: !isShowDeck}">
        <div class="deck-content-top-bar">
            <button class="collapse-btn" @click="hideDeck"><span><i class="fas fa-chevron-right"></i></span></button>
            <deck-regions :deck="deckCode" :fixedWidth="false"></deck-regions>
        </div>
        <div class="deck-content-detail">
            <deck-detail :locale="locale" :baseDeck="deckCode" :fixedHeight="true"></deck-detail>
        </div>
    </div>

    <div class="bottom-bar">
        <div class="left">
            <div class="app-name">{{ $t("appName") }}</div>
        </div>
        <div class="right">
            <!-- <div class="version download tooltip" v-if="!isUpdatedVersion" @click="openURL(downloadUrl)">
                <span class="tooltiptext">
                    <i class="fas fa-arrow-to-bottom"></i> {{remoteVersion}}
                </span>
                <i class="fas fa-exclamation-triangle"></i> {{version}}</div> -->
            <div class="version tooltip"
            :class="{download: updateDownloaded}"
            @click="installDownloadedUpdate()"
            >
                <span class="tooltiptext top-bottom-right">
                    <span v-if="isUpdatedVersion"><i class="fas fa-check"></i></span>{{versionTooltip}}
                </span>
                <i class="fas" :class="{'fa-redo-alt': updateDownloaded}"></i>
                {{versionText}}</div>
        </div>
    </div>
</template>

<script>

import BaseWindowControls from '../components/BaseWindowControls.vue'
import axios from 'axios'
import DeckRegions from '../components/DeckRegions.vue'
import Leaderboard from '../components/Leaderboard.vue'
import PlayerMatches from '../components/PlayerMatches.vue'
import DeckDetail from '../components/DeckDetail.vue'
import LocaleChanger from '../components/LocaleChanger.vue'

const requestDataWaitTime = 400 //ms
const requestHistoryWaitTime = 100 //ms
const requestStatusWaitTime = 1000 //ms
const inputNameListLength = 10;

// const portNum = "26531"
// const API_BASE = `http://127.0.0.1:${portNum}`

let cancelToken, localCancleToken
var lastStatusRequestTime
var requestLocalHistoryTimeout, requestHistoryTimeout, prevHistoryRequest

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
    my: 0,
    search: 1,
    leaderboard: 2,
    settings: 3,
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

export default {
    mounted() {
        console.log("Mounted")
        // var test = 'Hello'
        this.requestVersionData()
        this.requestStatusInfo()
        this.handleGameEnd()

        this.initLocalSettings()
    },
    components: { 
        BaseWindowControls,
        DeckRegions,
        Leaderboard,
        PlayerMatches,
        DeckDetail,
        LocaleChanger
    },
    data() {
        return {
            // rawDataString: null,
            deckCode: null,
            isShowDeck: false,
            matches: [],
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
            updateProcess: 0,
            updateDownloaded: false,

            currentPage: PAGES.search,

            PAGES: PAGES,

            lorRunning: null,
            localMatches: [],
            localPlayerInfo: {}, // playerId, server, language, rank, lp
            localHistoryLoading: false,
            localHistoryWaiting: false,

            // Options
            autoLaunch: null,
            debugInfos: "",
            locale: 'en_us',

            portNum: '26531',
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
        hasLocalInfo() {
            return this.localMatches.length > 0
        },
        versionText(){
            if (this.updateDownloaded) {
                return "Restart"
            }
            return this.version
        },
        versionTooltip() {
            if (this.isUpdatedVersion) { 
                return "Updated"
            } else if (this.updateDownloaded) {
                return "Update on next start" 
            } else if (this.updateProcess > 0) {
                return `Downloading... ${this.updateProcess}%`
            } else if (this.remoteVersion) {
                return `Latest: ${this.remoteVersion}`
            }
            return this.$t('str.loading') 
        },
        apiBase() {
            return `http://127.0.0.1:${this.portNum}`
        }
    },
    methods: {

        // Local Settings
        initLocalSettings() {
            window.ipcRenderer.on('check-auto-launch-return', (event, isEnabled) => {
                this.autoLaunch = isEnabled
            })

            window.ipcRenderer.on('debug-info-display', (event, info) => {
                console.log(info)
                this.debugInfos = info
            })

            window.ipcRenderer.on('return-port', (event, port) => {
                console.log("New Port:", port)
                this.portNum = port
            })

            window.ipcRenderer.send("get-port")

            this.checkAutoLaunch()
        },

        checkAutoLaunch() {
            window.ipcRenderer.send("check-auto-launch")
        },
        setAutoLaunch(enable) {
            window.ipcRenderer.send('set-auto-launch', enable)
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

            console.log("Search Player", data)

            if (this.regions.includes(data.region)) {
                // SEA will not be included
                this.setCurrentPage(PAGES.search)
                this.selectRegion(data.region)
                this.searchText = data.name
                this.resetInputFocus()

                this.playerName = data.name
                this.playerTag = data.tag
                this.requestHistoryData()
            }
        },

        // Search bar
        clearSearch() {
            this.searchText = ''
            this.searchName()
            document.querySelector(".search-bar").focus()
        },
        searchName() {
            if (this.searchText.length > 0) {
                this.requestNameData()
            } else {
                this.resetInputNameList()
            }
        },
        resetInputNameList() {
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
            // console.log("searchHistoryAutoComplete")
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
                
                // Perform the actual search
                this.requestHistoryData()
                this.resetInputFocus()
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
                } else if (splited.length == 1 && splited[0] == this.playerName && this.playerTag) {
                    // When trying to search the same people, do a refresh
                    this.requestHistoryData()
                    this.resetInputFocus()
                } else {
                    // Alert the player needed info
                }
            }
            
        },
        clearInfo() {
            this.playerName = ""
            this.playerTag = ""
            this.playerRank = null
            this.playerLP = null
            this.playerRegion = null
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

            console.log("processHistoryData", data)

            for (var key in data) {

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

                this.playerName = player.name // Sync name so all caps are correct
                opponentName = opponent.name
                
                if (opponent.rank !== "") {
                    opponentRank = opponent.rank + 1 // rank starts from 0
                } else {
                    opponentRank = "" // ranks can be empty
                }

                opponentLp = opponent.lp
                opponentTag = opponent.tag

                if (this.playerRank == null && player.rank !== "") { 
                    this.playerRank = player.rank + 1 // player.rank starts from 0
                }
                if (!this.playerLP) this.playerLP = player.lp
                
                deck = playerGame.deck_code
                opponentDeck = opponentGame.deck_code
                order = playerGame.order_of_play
                win = playerGame.game_outcome == "win"
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
        installDownloadedUpdate() {
            if (this.updateDownloaded) {
                console.log("Trigger Intall Update")
                window.ipcRenderer.send("install-update")
            } else {
                console.log("Download not finished")
            }
        },
        handleGameEnd() {
            window.ipcRenderer.on('game-end-handle', (event) => {
                console.log("Game Ended: Requesting local history")
                this.requestLocalHistory()
            })
        },
        requestVersionData() {

            console.log("Request Version Data")
            window.ipcRenderer.on('app-version', (event, arg) => {
                console.log("Current Version is:", arg)
                // window.appVersion = arg
                this.version = arg
            })

            window.ipcRenderer.on('checking-for-update', (event) => {
                console.log("Checking For Update")
                this.updateDownloaded = false // Reset Update downloaded
            })

            window.ipcRenderer.on('update-available', (event, info) => {
                // console.log(info)
                // window.appVersionLatest = info.version
                
                console.log("Latest Version is:", info.version)
                this.remoteVersion = info.version
            })

            window.ipcRenderer.on('update-not-available', (event, arg) => {
                console.log("Version is Latest")
                this.remoteVersion = this.version
            })

            window.ipcRenderer.on('download-process', (event, arg) => {
                console.log(arg)
                if (Math.floor(arg.percent) < 100)
                    this.updateProcess = Math.floor(arg.percent)
            })

            window.ipcRenderer.on('update-downloaded', (event, arg) => {
                console.log(arg)
                console.log("Update Downloaded!")
                this.updateDownloaded = true
            })

            window.ipcRenderer.send("check-update")
            

            // --- Version 2 ---
            // console.log(window)
            // console.log(window.appVersion)

            // if (window && window.appVersion) {
            //     this.version = window.appVersion
            //     console.log("Got Version Data:", window.appVersion)
            // } else {
            //     setTimeout(this.requestVersionData, requestDataWaitTime);
            // }
            
            // axios.get(`${this.apiBase}/version`)
            //     .then((response) => {
            //         var data = response.data
            //         this.version = data.version
            //         this.remoteVersion = data.remoteVersion
            //         this.downloadUrl = data.downloadUrl
            //     })
            //     .catch((e) => {
            //         if (axios.isCancel(e)) {
            //             // Console log is cancel
            //         } else { 
            //             console.log('error', e) 
                        
            //             setTimeout(this.requestVersionData, requestDataWaitTime);
            //         }
            //     })
        },
        requestStatusInfo() {
            // Keeps requesting status
            lastStatusRequestTime = Date.now()
            axios.get(`${this.apiBase}/status`)
                .then((response) => {
                    var data = response.data

                    var updateLocalPlayer = false
                    if (this.localPlayerInfo.playerId != data.playerId) {
                        // there is a change in player ID
                        updateLocalPlayer = true
                    }

                    if (data.playerId != "") {

                        this.localPlayerInfo.playerId = data.playerId
                        var nameid = data.playerId.split('#')
                        var oldName = this.localPlayerInfo.name
                        var oldTag = this.localPlayerInfo.tag
                        
                        this.localPlayerInfo.name = nameid[0]
                        this.localPlayerInfo.tag = nameid[1]

                        if (this.localMatches.length <= 0) {
                            // if the matches are still empty
                            // updateLocalPlayer = true
                        }

                    } else {
                        this.localPlayerInfo.playerId = null
                        this.localPlayerInfo.name = null
                        this.localPlayerInfo.tag = null

                        this.localMatches = []
                    }

                    this.localPlayerInfo.server = data.server
                    this.localPlayerInfo.language = data.language

                    if (updateLocalPlayer) {
                        this.requestLocalHistory()
                    }
                    
                    if (data.language) {
                        var newLocale = data.language.replace('-', '_').toLowerCase()
                        if (this.locale != newLocale) {
                            console.log("Switch Locale", this.locale, newLocale)
                        }
                        this.locale = newLocale
                    }
                    // console.log(this.locale)

                    this.lorRunning = data.lorRunning

                    var elapsedTime = Date.now() - lastStatusRequestTime // ms
                    if (requestStatusWaitTime > elapsedTime) {
                        setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime); 
                    } else {
                        setTimeout(this.requestStatusInfo, 100);
                    }
                    
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else { 
                        console.log('error', e)
                        var elapsedTime = Date.now() - lastStatusRequestTime // ms
                        if (elapsedTime > requestStatusWaitTime) {
                            setTimeout(this.requestStatusInfo, 100);
                        } else {
                            setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime);
                        }
                    }
                })
        },
        requestNameData() {
            
            axios.get(`${this.apiBase}/name/${regionNames[this.selectedRegion]}/${this.searchText}`)
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
        requestHistoryData() {

            console.log("Enters Request History Data")

            if (this.localHistoryLoading) {
                // Before start, wait until old local search resolves
                if (requestHistoryTimeout) clearTimeout(requestHistoryTimeout)
                requestHistoryTimeout = setTimeout(this.requestHistoryData, requestHistoryWaitTime);
                return
            }

            var newRequest = `${this.apiBase}/search/${regionNames[this.selectedRegion]}/${this.playerName}/${this.playerTag}`
            if (prevHistoryRequest == newRequest && this.isLoading) {
                // Don't refresh if the request is the same and ongoing
                return
            }

            //Check if there are any previous pending requests
            if (typeof cancelToken != typeof undefined) {
                cancelToken.cancel("Operation canceled due to new request.")
            }
            
            //Save the cancel token for the current request
            cancelToken = axios.CancelToken.source()

            this.isLoading = true;
            this.playerRegion = regionNames[this.selectedRegion]

            prevHistoryRequest = newRequest

            axios.get( newRequest ,
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
                    } else { 
                        console.log('error', e) 
                        this.isLoading = false
                    }
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

        requestLocalHistory() {

            // if (this.isLoading) {
            //     // Before starting everything check to see if there is already a search request
            //     if (requestLocalHistoryTimeout) clearTimeout(requestLocalHistoryTimeout)
            //     requestLocalHistoryTimeout = setTimeout(this.requestLocalHistory, requestHistoryWaitTime);
            //     this.localHistoryWaiting = true
            //     return
            // }

            // Not waiting for other search requests
            // this.localHistoryWaiting = false
            
            if (this.localHistoryLoading) {
                // Don't do anything if there is already a local search request
                return
            }

            // Now ready for a new request

            //Check if there are any previous pending requests
            if (typeof localCancleToken != typeof undefined) {
                localCancleToken.cancel("Operation canceled due to new request.")
            }
            
            //Save the cancel token for the current request
            localCancleToken = axios.CancelToken.source()
            
            var server = this.localPlayerInfo.server
            var name = this.localPlayerInfo.name
            var tag = this.localPlayerInfo.tag

            if (!(server && name && tag)) {
                // Checks to see if there is all the information
                // Don't do anything if not enough data
                return
            }

            console.log("Request Local History", `${this.apiBase}/search/${server}/${name}/${tag}`)
            this.localHistoryLoading = true

            axios.get(`${this.apiBase}/search/${server}/${name}/${tag}`,
                    { cancelToken: localCancleToken.token }) // Pass the cancel token
                .then((response) => {
                    this.localHistoryLoading = false

                    if (response.data == "Error") {
                        console.log("Local History Search Error")
                    } else {
                        this.processLocalHistory(response.data)
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else {
                        console.log('error', e)
                        this.localHistoryLoading = false
                    }
                    
                })
        },
        processLocalHistory(data) {

            console.log("Process Local History!")

            this.localMatches = []
            this.localPlayerInfo.rank = null
            this.localPlayerInfo.lp = null

            for (var key in data) {

                if (!data[key]) continue // Skip if null history

                var isFirstPlayer = data[key].player_info[0].name.toLowerCase() == this.localPlayerInfo.name.toLowerCase()
                
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

                opponentName = opponent.name
                
                if (opponent.rank !== "") {
                    opponentRank = opponent.rank + 1 // rank starts from 0
                } else {
                    opponentRank = "" // ranks can be empty
                }
                
                opponentLp = opponent.lp
                opponentTag = opponent.tag

                if (!this.localPlayerInfo.rank && player.rank !== "") {
                    this.localPlayerInfo.rank = player.rank + 1 // player.rank starts from 0
                }
                
                if (!this.localPlayerInfo.lp) this.localPlayerInfo.lp = player.lp
                
                deck = playerGame.deck_code
                opponentDeck = opponentGame.deck_code
                order = playerGame.order_of_play
                win = playerGame.game_outcome == "win"
                rounds = info.total_turn_count
                var badges = []
                if (info.game_mode) badges.push(info.game_mode.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))
                if (info.game_type) badges.push(info.game_type.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))

                time = processDate(info.game_start_time_utc)

                this.localMatches.push({
                    opponentName: opponentName,
                    deck: deck,
                    region: regionShort[this.localPlayerInfo.server],
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
    },

}

</script>

<style scoped>

    .region-tabs {
        display: flex;
        /* gap: 5px; */
        /* padding-left: 15px; */
    }

    .region-option {
        
        /* color: #ABABAB; */
        cursor: pointer;

        width: 60px;
        height: 32px;

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

        box-sizing: border-box;
        
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
        padding: 0px 20px 0px 50px;
        border-radius: 40px;
        box-sizing: border-box;
    }

    .search-bar:focus {
        outline: 0px;
        background: var(--col-dark-grey);
    }

    .search-bar-auto-complete {
        opacity: 0;
        visibility: hidden;

        position: absolute;
        top: 50px;
        left: 10px;
        text-align: left;
        background: var(--col-background);
        /* padding: 5px 0px 0px 0px; */
        
        border-radius: 8px;
        overflow: hidden;

        z-index: 2;

        transition: visibility 0s linear 300ms, opacity 300ms;
    }

    .search-bar-input-container:focus-within + .search-bar-auto-complete {
        opacity: 1;
        visibility: visible;

        transition: visibility 0s linear 0s, opacity 300ms;
    }

    .auto-complete-item {
        padding: 6px 15px 8px 9px;
        cursor: pointer;
    }

    .auto-complete-item:hover, .auto-complete-item.selected {
        background: var(--col-dark-grey);
    }

    .search-btn {
        color: var(--col-dark-white);
        background: none;
        outline: 0px;
        border: 0px;
        cursor: pointer;
        width: 6%;
        text-align: right;
    }

    .search-btn.active {
        color: white;
    }

    .search-btn.inside {
        position: absolute;
        width: 36px;
        height: 50px;
        padding: 0px;
        font-size: 16px;
        text-align: center;
    }

    .search-btn.right {
        right: 10px;
    }

    .search-btn.left {
        left: 10px;
    }

    .loading-text {
        font-size: 24px;
        margin: 20px 0px;
    }


    .content {
        text-align: center;
        display: block;
        width: calc(100% - 80px);
        min-width: 550px;
        margin-left: 80px;
        margin-top: 43px;
        /* padding: 10px 40px; */
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
        z-index: 6;
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
        height: calc(100vh - 88px); 
        /* top bar: -43 | bottom bar: -45 */
        overflow-y: scroll;
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

    .left-nav-btn.nav-bottom {
        margin-top: auto;
        margin-bottom: calc(45px + 10px);
        color: var(--col-lighter-grey);
    }

    .left-nav-btn.nav-bottom.selected {
        color: white;
    }

    .left-nav-btn.selected:not(:disabled):hover .icon-default,
    .left-nav-btn .icon-hover{
        display: none;
    }

    .left-nav-btn .icon-default {
        display: inline;
    }

    .left-nav-btn.selected:not(:disabled):hover .icon-hover{
        display: inline;
        cursor: pointer;
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
        font-size: 16px;

        white-space: nowrap;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px 10px;

        box-sizing: border-box;

        position: absolute;
        z-index: 10;

        /* Position the tooltip */
        bottom: 120%;
        left: 50%;
        transform:translateX(-50%);
        
        /* left: 50%; */
        /* margin-left: -50%; */
    }

    .tooltip .tooltiptext .fas {
        margin-right: 5px;
    }

    .tooltip .tooltiptext.top {
        /* Position the tooltip */
        bottom: 120%;
        left: 50%;
        transform:translateX(-50%);
    }

    .tooltip .tooltiptext.right {
        /* Position the tooltip */
        top: 50%;
        bottom: auto;
        left: 105%;
        transform: translateY(-50%);
    }

    .tooltip .tooltiptext.top-bottom-right {
        /* Position the tooltip */
        bottom: 100%;
        right: -10px;
        left: auto;
        transform: none;
        margin-bottom: 22px;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
    }

    .sticky-top {
        position: sticky;
        top: 0;
        background: var(--col-background);
        z-index: 2;
    }

    /* Settings Page */

    .settings .title {
        font-size: 32px;
        text-align: left;
        padding: 10px 0px 20px 0px;
    }

    .settings-list-item {
        margin-bottom: 10px;
        display: flex;
        font-size: 18px;
        align-items: center;
    }

    .settings-list-item .settings-title {
        display: inline-block;
    }

    .settings-list-item .settings-btn {
        display: inline-block;
        margin-left: auto;
        border: 0px;
        background: var(--col-dark-grey);
        color: white;
        font-size: 0.9em;
        padding: 8px 15px;
        outline: none;
        cursor: pointer;
        border-radius: 100px;
    }

    .settings .debug-info {
        margin-top: 50px;
        background: var(--col-dark-grey);
        padding: 20px;
        overflow: scroll;
    }

</style>