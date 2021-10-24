<template>

    <div class="left-nav">
        <button class="left-nav-btn tooltip"
            :class="{
                selected: currentPage == PAGES.my,
                disabled: !lorRunning
            }" 
            @click="handleProfileClick"
            :disabled="!lorRunning"
        >
            <span class="icon-default"
                v-if="!localHistoryLoading"><i class="fas fa-user-circle"></i></span>
            <span class="icon-default icon-hover"
                v-if="localHistoryLoading"><i class="fas fa-redo-alt fa-spin-fast"></i></span>
            <span class="icon-hover"
                v-if="lorRunning && !localHistoryLoading && !(!hasLocalInfo || localPlayerInfo.server != 'sea') "><i class="fas fa-check"></i></span>
            <span class="icon-hover"
                v-if="lorRunning && !localHistoryLoading && (!hasLocalInfo || localPlayerInfo.server != 'sea')"><i class="fas fa-redo-alt"></i></span>
            
            <div v-if="!lorRunning || !localPlayerInfo.playerId"
                class="tooltiptext right" >{{$t('tooltips.lorlogin')}}</div>
            <div v-if="lorRunning && localPlayerInfo.playerId && !hasLocalInfo"
                class="tooltiptext right" >{{$t('str.error.playerNoHistory')}}</div>
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
        <div class="left-nav-btn menu no-click">
            <span><i class="fas fa-books"></i></span>
            <div class="menu-content right">
                <div class="card" @click="openURL('https://masteringruneterra.com/')">
                    <img src="https://masteringruneterra.com/wp-content/uploads/2021/09/MasteringRuneterraWebsiteLogo-300x129.webp">
                </div>
                <div class="card" @click="openURL(`https://playruneterra.com/${locale.replace('_', '-')}/news`)">
                    <img src="https://images.contentstack.io/v3/assets/blt0eb2a2986b796d29/blt8ba1ec1b0013e362/5ea53af4ae23d30cd1dfb3e4/lor-logo.png">
                </div>
                <div class="card square" @click="openURL('https://www.swimstrim.com/')">
                    <img src="https://www.swimstrim.com/packs/media/images/logo-8b7cd382.png">
                </div>
                <div class="card square" @click="openURL('https://runeterra.ar/')">
                    <img src="https://cdnruneterra.ar/assets/img/logo_ar_black.png">
                </div>
                <!-- <div class="card" @click="openURL('https://masteringruneterra.com/')">
                    <img src="https://picsum.photos/400/210">
                </div> -->
            </div>
        </div>
        <button class="left-nav-btn nav-bottom" 
            :class="{selected: currentPage == PAGES.contact}" 
            @click="setCurrentPage(PAGES.contact)">
            <span><i class="fas fa-comment-alt-smile"></i></span>
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
            <player-matches 
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
                        
                        <input spellcheck="false" autocomplete='off' class="search-bar" 
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
            <player-matches v-if="!isLoading && playerName && matches.length > 0" 
                @search="searchPlayer($event)"
                @show-deck="showDeck"
                :playerName="playerName"
                :playerRegion="playerRegion"
                :playerRank="playerRank"
                :playerLP="playerLP"
                :matches="matches"
            >
            </player-matches>

            <div class="status-text">
                <span v-if="!isLoading && !isError && matches.length <= 0">
                    {{$t('search.prompt')}}
                </span>
                <span v-if="isLoading">
                    <i class="fas fa-circle-notch fa-spin"></i> 
                    {{$t('str.loading')}}
                </span>
                <span v-if="isError">
                    <!-- <i class="fas fa-circle-notch fa-spin"></i> -->
                    {{errorText}}
                </span>
            </div>
        </div>

        <div class="main-content-container leaderboard" v-if="currentPage == PAGES.leaderboard">
            <leaderboard :apiBase="apiBase" @search="searchPlayer($event)"></leaderboard>
        </div>

        <div class="main-content-container contact" v-if="currentPage == PAGES.contact">
            <contact-info :apiBase="apiBase"></contact-info>
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
            <deck-detail :baseDeck="deckCode" :fixedHeight="true"></deck-detail>
        </div>
    </div>

    <div class="bottom-bar">
        <div class="left">
            <div class="app-name url" @click="openURL('https://www.lormaster.com')">{{ $t("appName") }}</div>
            <div v-if="!localApiEnabled && lorRunning" class="api-warning warning"><small><i class="fas fa-exclamation-triangle"></i>{{ $t("str.error.localApiError")}}</small></div>
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

import BaseWindowControls from '../../components/BaseWindowControls.vue'
import axios from 'axios'
import DeckRegions from '../../components/DeckRegions.vue'
import Leaderboard from '../../components/Leaderboard.vue'
import PlayerMatches from '../../components/PlayerMatches.vue'
import DeckDetail from '../../components/DeckDetail.vue'
import LocaleChanger from '../../components/LocaleChanger.vue'
import ContactInfo from '../../components/ContactInfo.vue'

import { mapActions } from 'vuex'

const requestDataWaitTime = 400 //ms
const requestHistoryWaitTime = 100 //ms
const requestStatusWaitTime = 1000 //ms
const inputNameListLength = 10;

// import ua from 'universal-analytics'

// const portNum = "26531"
// const API_BASE = `http://127.0.0.1:${portNum}`

let cancelToken, localCancleToken
var lastStatusRequestTime
var requestHistoryTimeout, prevHistoryRequest

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
    
    contact: 3,
    settings: 4,
}

export default {
    components: { 
        BaseWindowControls,
        DeckRegions,
        Leaderboard,
        PlayerMatches,
        DeckDetail,
        LocaleChanger,
        ContactInfo,
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
            isError: false,

            errorType: "",
            
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
            localApiEnabled: true,
            localMatches: [],
            localPlayerInfo: {}, // playerId, server, language, rank, lp
            localHistoryLoading: false,
            localHistoryWaiting: false,

            // Options
            autoLaunch: null,
            debugInfos: "",

            portNum: '26531',
        }
    },
    computed: {
        errorText() {
            
            var error = this.errorType
            console.log("Processing error text from type", error)
            if (error == 0) {
                return this.$t('str.error.playerNotFound')
            } else if (error == 1 || error == 2) {
                return this.$t('str.error.playerNoHistory')
            } else {
                return this.$t('str.error.unkown')
            }
        },
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
            return this.localMatches && this.localMatches.length > 0
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
        },
    },
    mounted() {
        console.log("Mounted")
        console.log(process.env.NODE_ENV)
        console.log("$store.state.locale", this.locale)
        
        // Testing switching locale
        // if (process.env.NODE_ENV == "development") {
        //     this.$store.commit('changeLocale', 'zh_tw')
        // }
        
        // console.log(this.user)

        try {

            // var test = 'Hello'
            
            this.requestStatusInfo()
            
            if (!window.ipcRenderer) { return }
            this.handleGameEnd()
            this.requestVersionData()
            this.initLocalSettings()
            this.initStore()
            this.initChangeLocale()
            
        } catch (error) {
            console.log(error)
        }
        
        
    },
    methods: {

        ...mapActions([
            'changeLocale'
        ]),

        initStore() {
            window.ipcRenderer.send('request-store', 'ui-locale')

            window.ipcRenderer.on('reply-store', (event, key, val) => {
                console.log("Got store", key, val)

                if (key == 'ui-locale' && val) {
                    this.$i18n.locale = val
                    console.log("Change locale to", val)
                }
            })
        },

        // Change Locale
        initChangeLocale() {

            window.ipcRenderer.on('to-change-locale', (event, newLocale) => {
                this.$i18n.locale = newLocale
                console.log("Changing locale to", newLocale)
            })
        },

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

        handleProfileClick() {
            if (!this.hasLocalInfo || (this.currentPage == PAGES.my && this.localPlayerInfo.server != 'sea')) {
                this.requestLocalHistory()
            }
            this.setCurrentPage(PAGES.my)
        },

        // Page Switch
        setCurrentPage(page) {

            var pagekeys = Object.keys(PAGES)
            var label = "From [" + pagekeys[this.currentPage] + "] to [" + pagekeys[page] +"]"

            this.sendUserEvent({
                category: "Main Window",
                action: "Change Tab",
                label: label,
                value: null,
            })
            this.currentPage = page
        },
        selectRegion(region) {
            this.sendUserEvent({
                category: "Main Window Search",
                action: "Select Region",
                label: regionNames[region],
                value: null,
            })

            this.selectedRegion = region
            var searchBar = document.querySelector(".search-bar")
            if (searchBar) searchBar.focus()
            
            this.searchName()
        },
        searchPlayer(data) {
            
            this.sendUserEvent({
                category: "Main Window Search",
                action: "Leaderboard Search",
                label: data.region + ": " + data.name + "#" + data.tag,
                value: null,
            })

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
                
                this.sendUserEvent({
                    category: "Main Window Search",
                    action: "Auto Complete",
                    label: this.playerName + "#" + this.playerTag,
                    value: null,
                })

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

                    this.sendUserEvent({
                        category: "Main Window Search",
                        action: "User Input [New]",
                        label: `${this.searchText}`,
                        value: null,
                    })

                    // Perform the actual search
                    this.requestHistoryData()
                    this.resetInputFocus()
                } else if (splited.length == 1 && splited[0] == this.playerName && this.playerTag) {
                    // When trying to search the same people, do a refresh
                    this.requestHistoryData()
                    this.resetInputFocus()

                    this.sendUserEvent({
                        category: "Main Window Search",
                        action: "User Input [Refresh]",
                        label: `${this.searchText}`,
                        value: null,
                    })

                } else {
                    // Alert the player needed info

                    this.sendUserEvent({
                        category: "Main Window Search",
                        action: "User Input [Error]",
                        label: `${this.searchText}`,
                        value: null,
                    })

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
        errorHistory(error) {
            this.clearInfo()
            this.isError = true
            this.errorType = error
            // this.playerName = "No history found"

        },
        openURL(url) {
            if (window.openExternal) {
                window.openExternal(url)
            } else {
                window.open(url);
            }
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
            
        },
        requestStatusInfo() {
            // Keeps requesting status
            
            // DevStatus
            if (process.env.NODE_ENV == "development") {
                console.log("Request Status Data")
                const testRegion = 'sea'
                // const testRegion = 'americas'
                const testStatus = `{"language": "zh-TW", "lorRunning": true, "playerId": "FlyingFish#1111","port": "21337","server": "${testRegion}"}`
                this.processStatusInfo(JSON.parse(testStatus))
                return
            } 

            lastStatusRequestTime = Date.now()
            axios.get(`${this.apiBase}/status`)
                .then((response) => {
                    this.processStatusInfo(response.data)
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
                            setTimeout(this.requestStatusInfo, 100)
                        } else {
                            setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime);
                        }
                    }
                })
        },
        initAnalytics(uid) {
            if (window.ipcRenderer) { window.ipcRenderer.send('user-init', uid) }
        },
        processStatusInfo(data) {
            var updateLocalPlayer = false
            if (this.localPlayerInfo.playerId != data.playerId) {
                // there is a change in player ID
                updateLocalPlayer = true

                if (data.playerId) {
                    try {
                        this.initAnalytics(data.playerId)
                        // window.ipcRenderer.send('user-init', data.playerId)
                    } catch (error) {
                        console.log(error)
                    }
                }
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
                    this.changeLocale(newLocale)
                }
            }
            // console.log(this.locale)

            this.lorRunning = data.lorRunning
            this.localApiEnabled = data.isLocalApiEnable
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
            this.isError = false;
            this.playerRegion = regionNames[this.selectedRegion]

            prevHistoryRequest = newRequest

            this.sendUserEvent({
                category: "Main Window Requests",
                action: "Request Search",
                label: "URL: " + newRequest,
                value: null,
            })

            const requestHistoryStartTime = Date.now()

            axios.get( newRequest ,
                    { cancelToken: cancelToken.token }) // Pass the cancel token
                .then((response) => {
                    this.isLoading = false;

                    this.sendUserEvent({
                        category: "Main Window Requests",
                        action: "Got Search Result [Success]",
                        label: "URL: " + newRequest,
                        value: Date.now() - requestHistoryStartTime,
                    })

                    this.processSearchHistory(response.data)

                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled")
                    } else {
                        console.log('error', e)
                        if (e.response) {
                            var data = e.response.data
                            this.errorHistory(data.status.error)
                        } else {
                            this.errorHistory(3) // Unkown Error
                        }
                        this.isLoading = false

                        this.sendUserEvent({
                            category: "Main Window Requests",
                            action: "Got Search Result [Fail]",
                            label: "Type: "+ this.errorType +" | URL: " + newRequest,
                            value: Date.now() - requestHistoryStartTime,
                        })

                        
                    }
                })

        },
        requestLocalHistory() {

            console.log("Request Local History")

            // DevLocal
            if (process.env.NODE_ENV == "development") {

                // const testData = require('../../assets/data/testLocalHistoryData')
                const testData = require('../../assets/data/testLocalData')['flyingfish#0000']

                // this.playerName = "FlyingFish"
                // this.playerRegion = "americas"
                // this.processSearchHistory(testData)

                // pass
                // this.processLocalHistory(testData['flyingfish#0000'])
                this.localHistoryLoading = true
                setTimeout(() => {
                    this.localHistoryLoading = false
                    Math.random() > 0.5 ? this.processLocalHistory(testData) : this.processLocalHistory([])
                }, 1000)
                

                return
            }

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

            let apiLink;
            if (server === 'sea') {
                apiLink = `${this.apiBase}/local`
            } else {
                apiLink = `${this.apiBase}/search/${server}/${name}/${tag}`
            }

            console.log("Request Local History", apiLink)
            this.localHistoryLoading = true

            this.sendUserEvent({
                category: "Main Window Requests",
                action: "Request Local History",
                label: "URL: " + apiLink,
                value: null,
            })

            const requestLocalHistoryStartTime = Date.now()

            axios.get(apiLink,
                    { cancelToken: localCancleToken.token }) // Pass the cancel token
                .then((response) => {
                    this.localHistoryLoading = false

                    if (response.data == "Error") {
                        console.log("Local History Search Error")
                    } else {

                        this.sendUserEvent({
                            category: "Main Window Requests",
                            action: "Got Local History Result [Success]",
                            label: "URL: " + apiLink,
                            value: Date.now() - requestLocalHistoryStartTime,
                        })

                        if (server === 'sea') {
                            let key = (name + '#' + tag).toLowerCase()
                            // console.log('Current key', key)
                            this.processLocalHistory(response.data[key])
                        } else {
                            this.processLocalHistory(response.data)
                        }
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else {
                        console.log('error', e)
                        this.localHistoryLoading = false

                        this.sendUserEvent({
                            category: "Main Window Requests",
                            action: "Got Local History Result [Fail]",
                            label: "URL: " + apiLink,
                            value: Date.now() - requestLocalHistoryStartTime,
                        })
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
            this.sendUserEvent({
                category: "Main Window Deck",
                action: this.isShowDeck ? "Show Deck" : "Hide Deck",
                label: deck,
                value: null,
            })
            
        },
        hideDeck() {

            this.sendUserEvent({
                category: "Main Window Deck",
                action: "Hide Deck (Collapse Button)",
                label: null,
                value: null,
            })

            this.isShowDeck = false
        },
        processHistory(data, playerName, playerServer) {
            console.log("Process History!", playerName, playerServer)
            console.log(data)

            var matchInfo = {
                matches: [],
                rank: null,
                lp: null
            }

            if (!data) return matchInfo

            if (playerServer == 'sea') {
                // sea players only have local data
                for (let match of data) {
                    let opponentName, opponentRank, opponentLp, opponentTag, opponentDeck, 
                        deck, rounds, win, time, order;

                    matchInfo.rank = match.playerRank // Currently no value
                    matchInfo.lp = match.playerLp // Currently no value

                    opponentName = match.opponentName
                    opponentTag = null // Cannot get
                    opponentRank = match.opponentRank // Currently no value
                    opponentLp = match.opponentLp // Currently no value
                    opponentDeck = match.deck_tracker.opGraveyardCode
                    deck = match.deck_tracker.deckCode
                    rounds = null // Cannot get
                    win = match.localPlayerWon
                    time = match.startTime
                    order = null // Cannot get

                    let badges = [] // Currently no value

                    let details = {
                        openHand: match.deck_tracker.openHand,
                        replacedHand: match.deck_tracker.replacedHand,
                        timeline: match.deck_tracker.timeline,
                        startTime: match.startTime,
                        endTime: match.endTime,
                    }
                    
                    matchInfo.matches.push({
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
                        details: details,
                    })
                }
            } else {
                // Processing for normal Data
                for (var key in data) {

                    var match = data[key]
                    if (!match) continue // Skip if null history

                    var isFirstPlayer = match.player_info[0].name.toLowerCase() == playerName.toLowerCase()
                    var player, playerGame, opponent, opponentGame
                    var info = match.info
                    var details = null
                    
                    if (match.local && match.local.deck_tracker) {
                        details = {
                            openHand: match.local.deck_tracker.openHand,
                            replacedHand: match.local.deck_tracker.replacedHand,
                            timeline: match.local.deck_tracker.timeline,
                            startTime: match.local.startTime,
                            endTime: match.local.endTime,
                        }
                    }

                    var opponentName, opponentRank, opponentLp, opponentTag, opponentDeck, 
                        deck, rounds, win, time, order;
                    
                    if (isFirstPlayer) {
                        playerGame = info.players[0]
                        opponentGame = info.players[1]

                        player = match.player_info[0]
                        opponent = match.player_info[1]
                    } else {
                        playerGame = info.players[1]
                        opponentGame = info.players[0]

                        player = match.player_info[1]
                        opponent = match.player_info[0]
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

                    if (!matchInfo.rank && player.rank !== "") {
                        matchInfo.rank = player.rank + 1 // player.rank starts from 0
                    }
                    
                    if (!matchInfo.lp) matchInfo.lp = player.lp
                    
                    deck = playerGame.deck_code
                    opponentDeck = opponentGame.deck_code
                    order = playerGame.order_of_play
                    win = playerGame.game_outcome == "win"
                    rounds = info.total_turn_count
                    var badges = []
                    if (info.game_mode) badges.push(info.game_mode.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))
                    if (info.game_type) badges.push(info.game_type.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))

                    time = info.game_start_time_utc

                    matchInfo.matches.push({
                        opponentName: opponentName,
                        deck: deck,
                        region: regionShort[playerServer],
                        opponentDeck: opponentDeck,
                        opponentRank: opponentRank,
                        opponentLp: opponentLp,
                        opponentTag: opponentTag,
                        rounds: rounds,
                        win: win,
                        time: time,
                        badges: badges,
                        details: details,
                    })
                }

            }

            return matchInfo
        },
        processSearchHistory(data) {
            var Info = this.processHistory(
                data, this.playerName, this.playerRegion)
            this.matches = Info.matches
            this.playerRank = Info.rank
            this.playerLP = Info.lp
        },
        processLocalHistory(data) {
            var info = this.processHistory(data, this.localPlayerInfo.name, this.localPlayerInfo.server)
            this.localMatches = info.matches
            this.localPlayerInfo.rank = info.rank
            this.localPlayerInfo.lp = info.lp
        },
    },

}

</script>

<style lang="scss">
    .tooltip {
        position: relative;

        .tooltiptext {
            visibility: hidden;
            opacity: 0;

            transition: visibility 0s linear 200ms, opacity 200ms ease;

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
            bottom: 0%;
            left: 50%;
            transform:translateX(-50%);
            
            /* Position the tooltip */
            &.top {
                bottom: 120%;
                left: 50%;
                transform:translateX(-50%);
            }

            &.right {
                top: 50%;
                bottom: auto;
                left: 105%;
                transform: translateY(-50%);
            }

            &.left {
                top: 50%;
                bottom: auto;
                right: 105%;
                left: auto;
                transform: translateY(-50%);
            }

            &.top-end {
                top: auto;
                bottom: 120%;
                left: auto;
                right: 0%;
                transform:translateX(0%);
            }

            &.top-start {
                top: auto;
                bottom: 120%;
                left: 0%;
                right: auto;
                transform:translateX(0%);
            }

            &.top-bottom-right {
                bottom: 100%;
                right: -10px;
                left: auto;
                transform: none;
                margin-bottom: 22px;
            }
        
            /* left: 50%; */
            /* margin-left: -50%; */
            .fas {
                margin-right: 5px;
            }
        }

        &:hover {
            .tooltiptext {
                visibility: visible;
                opacity: 1;
                transition: visibility 0s linear 0s, opacity 200ms ease;
            }
        }
    }
</style>

<style lang="scss" scoped>

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

    .status-text {
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
        max-width: 650px;
        padding: 0px 50px;
        height: calc(100vh - 88px); 
        /* top bar: -43 | bottom bar: -45 */
        overflow-y: scroll;
        box-sizing: border-box;
    }

    .left-nav {
        position: absolute;
        top: 0;
        left: 0;
        width: 80px;
        height: 100vh;
        background: var(--col-light-bg);
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

        display: flex;
        justify-content: center;
        // vertical-align: middle;
        // text-align: center;
        align-items: center;

        &.no-click {
            cursor: default;
        }


        &.menu {

            $trans: 200ms ease;
            $mid-radius: 10px;

            position: relative;
            transition: background-color $trans, color $trans;

            &::before {
                
                content: "";
                position: absolute;
                background-color: var(--col-light-bg);
                top: 100%;
                right: 0px;
                width: 10px;
                height: 20px;
                border-top-right-radius: $mid-radius;

                transition: box-shadow $trans;

                pointer-events: none;
            }

            &:hover {

                color: white;

                &::before {
                    box-shadow: 0 -5px 0 0 var(--col-lighter-bg);
                }

                background-color: var(--col-lighter-bg);

                .menu-content {
                    visibility: visible;
                    opacity: 1;
                    transition: visibility 0s linear 0s, opacity $trans;
                }
            }

            .menu-content {

                border-radius: 0px $mid-radius $mid-radius $mid-radius;

                background-color: var(--col-lighter-bg);

                position: absolute;
                z-index: 10;

                top: 0px;
                bottom: auto;
                left: 100%;
                // transform: translateY(-50%);
                padding: 8px;

                visibility: hidden;
                opacity: 0;
                transition: visibility 0s $trans, opacity $trans;

                width: 250px;
                max-height: 400px;

                overflow: auto;
                
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 4px;
                grid-auto-rows: 110px;
                place-items: center;

                box-sizing: border-box;
                
                .card {
                    padding: 4px;
                    cursor: pointer;

                    border: 1px solid var(--col-lighter-bg);
                    transition: border $trans, background-color $trans;
                    
                    border-radius: 6px;

                    width: 100%;
                    height: 100%;

                    display: flex;
                    align-items: center;
                    justify-content: center;

                    box-sizing: border-box;

                    grid-column: 1 / span 2;

                    &.square {
                        grid-column: auto / span 1;
                    }
                    
                    &:hover {
                        // border: 1px solid var(--col-light-grey);
                        background-color: var(--col-grey);
                    }

                    img {
                        max-width: 100%;
                        max-height: 100%;
                    }
                }
            }

            
        }
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
        color: var(--col-lighter-grey);
        margin-top: auto;
    }

    .left-nav-btn.nav-bottom ~ .left-nav-btn.nav-bottom {
        margin-top: 0px;
    }

    .left-nav-btn.nav-bottom:last-child {
        margin-bottom: calc(45px + 10px);
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
        background: var(--col-lighter-bg);
        z-index: 6;

        display: flex;
        justify-content: space-between;
        align-items: center;

        color: white;

        .url {
            color: var(--col-gold);
            cursor: pointer;
        }
    }

    .bottom-bar .left, .bottom-bar .right {
        padding: 20px;
        display: flex;
        gap: 10px;
    }

    .bottom-bar .left div {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .warning i {
        padding-right: 6px;
    }

    .version.download {
        cursor: pointer;
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

