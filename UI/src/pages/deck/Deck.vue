<template>
    <base-window-controls :canClose="false" :canShrink="true" :playerName="oppoName" :playerRank="oppoRank" :titleType="infoType" :deck="deckCode"></base-window-controls>
    
    <div id="content">

        <div class="loading" :class="{invisible: !isLoading}">
            {{loadingText}}
        </div> 

        <div class="errorText" v-if="isInvalidDeckCode && isShowCode">{{$t('invalidDeck')}}</div>

        <div class="tabs" v-if="!isLoading">
            <div class="tab-title-group">
                <div class="tab-title" @click="switchTab(TABS.oppo)" :class="{active: isShowOppo}">
                    <i class="fas fa-swords"></i>
                </div>
                <div class="tab-title" @click="switchTab(TABS.oppog)" :class="{active: isShowOppoGrave}">
                    <i class="fas fa-tombstone-alt"></i>
                </div>
            </div>
            <div class="tab-title-group">
                <div class="tab-title" @click="switchTab(TABS.my)" :class="{active: isShowMy}">
                    <i class="fas fa-user-cowboy"></i>
                </div>
                <div class="tab-title" @click="switchTab(TABS.myg)" :class="{active: isShowMyGrave}">
                    <i class="fas fa-tombstone-alt"></i>                
                </div>
            </div>
        </div>

        <div id="history" class="tab-content" v-if="isShowOppo && !isLoading">

            <div class="loading" v-if="matchInfos.length <= 0"
                :class="{'zeroHeight': oppoPinnedId !== null}">
                {{loadingOppoText}}
            </div>
            
            <match-info 
                v-for="(match, index) in matchInfos" 
                :key="index"
                :opponentName="match.opponentName" 
                :rounds="match.rounds" 
                :time="match.time"
                :startTime="match.startTime"
                :matches="match.matches"
                :winrate="match.winrate"
                :badges="match.badge"
                :opponentDeck="match.opponentDeck" 
                :deck="match.deckCode"
                :total="matchTotalNum"
                :history="match.history"
            ></match-info>
        </div>

        <div class="layerpanel max-w-[280px]"  :class="{expanded: currentLayer != LAYERS.base}" v-if="isShowOppo">
                <button v-if="currentLayer == LAYERS.base" @click="onOpenDecklib" class="btn btn-decklib">Open Deck Library</button>
                <button class="btn btn-back" v-if="currentLayer != LAYERS.base" @click="onLayerBack">
                    <span><i class="fas fa-caret-down"></i></span>
                </button>
                <tracker-layer v-if="currentLayer != LAYERS.base"
                    @showDeck="onPinOppo"
                    :pinDeckId="oppoPinnedId"
                ></tracker-layer>
            </div>

        <div class="tab-content" v-if="isShowMy && !isLoading">
            <deck-regions :deck="startingDeckCode" :fixedWidth="false"></deck-regions>
            <deck-detail :deck="currentDeckCode" :baseDeck="startingDeckCode"></deck-detail>
        </div>

        <div class="tab-content" v-if="isShowOppoGrave && !isLoading">
            <div class="tab-text">{{$t('tracker.tabs.oppoPlayed')}}</div>
            <deck-detail :deck="oppoGraveCode" :baseDeck="oppoGraveCode" :showCopy="false"></deck-detail>
        </div>

        <div class="tab-content" v-if="isShowMyGrave && !isLoading">
            <div class="tab-text">{{$t('tracker.tabs.myPlayed')}}</div>
            <deck-detail :deck="myGraveCode" :baseDeck="myGraveCode" :showCopy="false"></deck-detail>
        </div>

        <div class="tab-content" v-if="isShowCode">
            <deck-regions :deck="deckCode" :fixedWidth="false"></deck-regions>
            <deck-detail :baseDeck="deckCode"></deck-detail>
        </div>

        <div class="footer" v-if="!isLoading"> 
            <div class="footer-text">{{$t('tracker.cardsInHand', {num: cardsInHandNum})}}</div>
        </div>

        <!-- <div class="layerpanel fixed" :class="{expanded: currentLayer != LAYERS.base}" v-if="!isLoading">    
            <button v-if="currentLayer == LAYERS.base" @click="onOpenDecklib" class="btn btn-decklib">Open Deck Library</button>
            <button class="btn btn-back" v-if="currentLayer != LAYERS.base" @click="onLayerBack">
                <span><i class="fas fa-caret-down"></i></span>
            </button>
            <tracker-layer v-if="currentLayer == LAYERS.decklib"></tracker-layer>
        </div> -->

    </div>
</template>


<script>

import MatchInfo from '../../components/match/MatchInfo.vue'
import axios from 'axios'
import BaseWindowControls from '../../components/base/BaseWindowControls.vue'
import DeckDetail from '../../components/deck/DeckDetail.vue'
import DeckRegions from '../../components/deck/DeckRegions.vue'
import DeckEncoder from '../../modules/runeterra/DeckEncoder'

import { mapActions } from 'vuex'

import '../../assets/scss/tooltips.scss'
import '../../assets/scss/deck.scss'

import TrackerLayer from '../../components/tracker/TrackerLayer.vue'

const requestDataWaitTime = 100; // ms
const requestServerWaitTime = 3000; //ms
const requestStatusWaitTime = 1000; //ms

// const portNum = "26531"
// const API_BASE = `http://127.0.0.1:${portNum}`

const TABS = {
    oppo: 0,
    my: 1,
    code: 2,
    oppog: 3,
    myg: 4,
}

const LAYERS = {
    base: 0,
    decklib: 1,
    deckdetail: 2,
}

var lastTrackTime, lastServerRequestTime, lastStatusRequestTime;

export default {
    components: { 
        BaseWindowControls,
        MatchInfo,
        DeckDetail,
        DeckRegions,
        TrackerLayer,
    },
    data() {
        return {
            rawDataString: null,
            matchInfos: [],
            matchTotalNum: 0,
            request: null,
            
            infoType: null,
            deckCode: null,
            titleType: null,
            currentTab: TABS.my,

            LAYERS: LAYERS,
            TABS: TABS,

            cardsInHandNum: null,

            currentDeckCode: null,
            startingDeckCode: null,
            oppoGraveCode: null,
            myGraveCode: null,
            oppoPinnedId: null,

            oppoName: null,
            oppoRank: null,
            oppoTag: null,
            oppoLp: null,

            lorRunning: false,

            portNum: '26531',

            currentLayer: 0,
        }
    },
    computed: {
        isLoading() {
            // if (this.infoType == "deckCode" && this.deckCode != "") return false
            if (this.currentDeckCode || this.startingDeckCode) return false
            if (this.matchInfos.length > 0) return false
            return (this.oppoName == null || this.oppoName == "" || this.matchInfos.length == 0)
            // return true
        },
        loadingText() {
            return this.$t('loading.readyToRock')
        },
        loadingOppoText() {
            if (this.oppoName && this.oppoTag) return this.$t('loading.history')
            return this.$t('loading.nohistory') 
        },
        isShowOppo() {
            return this.currentTab == TABS.oppo
        },
        isShowMy() {
            return this.currentTab == TABS.my
        },
        isShowCode() {
            return this.currentTab == TABS.code
        },
        isShowOppoGrave(){
            return this.currentTab == TABS.oppog
        },
        isShowMyGrave() {
            return this.currentTab == TABS.myg
        },
        // showMatch() {
        //     if (this.infoType == "deckCode") {
        //         return false
        //     }
        //     return true
        // },
        isInvalidDeckCode() {
            try {
                var deck = DeckEncoder.decode(this.deckCode)
            } catch (err) {
                // console.log(err.message)
                return true
            }
            return false
        },
        apiBase() {
            if (this.IS_ELECTRON) {
                return `http://127.0.0.1:${this.portNum}`
            }
            return `https://lmtservice.herokuapp.com`
        },
    },
    mounted() {
        // console.log(JSON.stringify(this.matchInfos))
        // this.getMatchInfo()
        // this.getSubData()
        // console.log("Mounted")
        // this.requestData()
        console.log("Page Deck Mounted")

        this.infoType = "match"

        // this.hideWindow()
        if (this.IS_ELECTRON) {
            window.ipcRenderer.on('return-port', (event, port) => {
                console.log("New Port:", port)
                this.portNum = port
            })

            window.ipcRenderer.send("get-port")

            this.initStore()
            this.initChangeLocale()
        }
        
        this.requestStatusInfo()
        this.requestTrackInfo()
        // this.requestServerInfo()
        
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

            console.log("Initing Change Locale | current locale", this.$i18n.locale)

            window.ipcRenderer.on('to-change-locale', (event, newLocale) => {
                this.$i18n.locale = newLocale
                console.log("Changing locale to", newLocale)
            })

            window.ipcRenderer.on('request-test-history', (event) => {
                this.requestTestOppoHistory()
            })
        },

        hideWindow() {
            if (window.hideWindow) {
                window.hideWindow()
            }
        },
        makeWindowVisible() {
            if (window.makeVisible) {
                window.makeVisible()
            }
        },
        switchTab(newTab) {
            
            if (this.IS_ELECTRON) {
                this.sendUserEvent({
                    category: "Tracker Event",
                    action: "Switch Tab",
                    label: "From: " + this.currentTab + " | To: " + newTab,
                    value: null,
                })
            }

            this.currentTab = newTab
        },
        // showOppo() {
        //     this.currentTab = TABS.oppo
        // },
        // showMy() {
        //     this.currentTab = TABS.my
        // },
        // showOppoGrave() {
        //     this.currentTab = TABS.oppog
        // },
        // showMyGrave() {
        //     this.currentTab = TABS.myg
        // },
        // showCode() {
        //     this.currentTab = TABS.code
        // },
        async getSubData() {
            if (window.sock)
            for await (const [topic, msg] of window.sock) {
                // console.log("Received Sub:", topic.toString(), " message:", msg.toString())
                // this.oppoName = msg.toString()
                // window.testData = msg.toString()
                // console.log(mainWindow)
                this.processRawData(msg)
            }
        },
        requestOpponentHistory() {
            // http://192.168.20.4:${portNum}/history/asia/J01/J01

            console.log("Request Opponent History for " + this.oppoName + "#" + this.oppoTag)

            axios.get(`${this.apiBase}/history/${this.server}/${this.oppoName}/${this.oppoTag}`)
                .then((response) => {
                    console.log("Opponent Data", response.data)
                    this.processOpponentHistory(response.data)
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })
        },
        requestTestOppoHistory() {
            const stormHistoryAPI = `${this.apiBase}/history/americas/storm/5961`
            axios.get(stormHistoryAPI)
                .then((response) => {
                    console.log("Opponent Data", response.data)
                    this.processOpponentHistory(response.data)
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })
        },
        requestStatusInfo() {
            
            if (!this.IS_ELECTRON) {
                var data = require('../../assets/data/testStatus')
                this.server = data.server
                if (data.language) {
                    var newLocale = data.language.replace('-', '_').toLowerCase()
                    if (this.locale != newLocale) {
                        console.log("Switch Locale", this.locale, newLocale)
                        this.changeLocale(newLocale)
                    }
                }

                return
            }

            // Keeps requesting status
            lastStatusRequestTime = Date.now()
            axios.get(`${this.apiBase}/status`)
                .then((response) => {
                    var data = response.data
                    var elapsedTime = Date.now() - lastStatusRequestTime // ms
                    this.server = data.server
                    
                    if (data.language) {
                        var newLocale = data.language.replace('-', '_').toLowerCase()
                        if (this.locale != newLocale) {
                            console.log("Switch Locale", this.locale, newLocale)
                            this.changeLocale(newLocale)
                        }
                    }

                    // console.log("Server", this.server)

                    if (requestStatusWaitTime > elapsedTime) {
                        setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime); 
                    } else {
                        setTimeout(this.requestStatusInfo, 100)
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else { 
                        console.log('error', e) 
                        setTimeout(this.requestStatusInfo, 100)
                    }
                })
        },
        requestOppoInfo() {
            // Getting opponent rank, lp and tag
            // Once per opponent change

            if (!this.IS_ELECTRON) {
                this.oppoTag = "5961"
                this.oppoName = "Storm"
                this.requestOpponentHistory()
                return
            }

            axios.get(`${this.apiBase}/opInfo`)
                .then((response) => {
                    var op = response.data
                    if (op.rank !== "") {
                        this.oppoRank = op.rank + 1
                    }
                    this.oppoTag = op.tag
                    console.log("opInfo:", op.name)
                    this.oppoName = op.name
                    this.oppoLp = op.lp

                    this.requestOpponentHistory()
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        // console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })
        },
        requestTrackInfo() {

            if (!this.IS_ELECTRON) {

                if (!this.startingDeckCode) {
                    Math.random() > 0.2 ? this.processTrackInfo(require('../../assets/data/testTrack')) : this.processTrackInfo({
                        positional_rectangles: null
                    })
                } else {
                    this.processTrackInfo(require('../../assets/data/testTrack'))
                }
                
                setTimeout(this.requestTrackInfo, 1000);
                return
            }

            lastTrackTime = Date.now()
            axios.get(`${this.apiBase}/track`)
                .then((response) => {

                    this.processTrackInfo(response.data)
                    
                    var elapsedTime = Date.now() - lastTrackTime // ms
                    if (requestDataWaitTime > elapsedTime) {
                        setTimeout(this.requestTrackInfo, requestDataWaitTime - elapsedTime); 
                    } else {
                        setTimeout(this.requestTrackInfo, 100);
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        // console.log("Request cancelled");
                    } else 
                    { 
                        console.log('error', e) 

                        var elapsedTime = Date.now() - lastTrackTime // ms
                        if (requestDataWaitTime > elapsedTime) {
                            setTimeout(this.requestTrackInfo, requestDataWaitTime - elapsedTime); 
                        } else {
                            setTimeout(this.requestTrackInfo, 100);
                        }
                    }
                })
            
        },
        processTrackInfo(data) {

            if (data.positional_rectangles && data.positional_rectangles.OpponentName) {
                // Check if there is opponent
                var opName = data.positional_rectangles.OpponentName

                if (opName.includes('_')){
                    // opponent is AI
                    this.oppoName = 'AI';
                    this.makeWindowVisible()
                    
                } else if ((!this.oppoName) || (this.oppoName.toLowerCase() != opName.toLowerCase())) {
                    // If there is no oppoName set or there is a change in the name
                    console.log("Track Info:", opName)
                    this.oppoName = opName
                    this.requestOppoInfo()
                    this.makeWindowVisible()
                }
                
            } else {
                // Clear Info about opponent and matches if there is no opponent

                this.oppoName = null
                this.oppoTag = null
                this.oppoRank = null
                this.oppoLp = null
                this.matchTotalNum = 0
                this.matchInfos = []
            }
            
            if (data.deck_tracker) {
                if (data.deck_tracker.deckCode) {
                    this.makeWindowVisible()
                    if (this.startingDeckCode == null) {
                        // switching from not having deck code
                        this.handleGameStart()
                    }
                }
                this.startingDeckCode = data.deck_tracker.deckCode
                this.currentDeckCode = data.deck_tracker.currentDeckCode
                this.oppoGraveCode = data.deck_tracker.opGraveyardCode
                this.myGraveCode = data.deck_tracker.myPlayedCardsCode
                this.cardsInHandNum = data.deck_tracker.cardsInHandNum
                
            } else {
                if (this.startingDeckCode != null) {
                    // switching from having deck code
                    this.handleGameEnd()
                }
                this.startingDeckCode = null
                this.currentDeckCode = null
                this.myGraveCode = null
                this.oppoGraveCode = null
                this.cardsInHandNum = null

                this.hideWindow()
            }
        },
        processOpponentHistory(data) {

            // Process New Data
            console.log("Process Json Data")

            // if ((data.type == "deckCode" && data.deckCode != "" && data.deckCode != this.deckCode)) {
                // Changes Deck Code
                // Make window appear to display deck code
                // window.showWindow()
                // Switches to code tab
                // this.showCode()
            // } else 
            if (JSON.stringify(this.matchInfos) != JSON.stringify(data)) {
                // Changes Match Info
                console.log("New Match Info")

                if (window.showWindow) window.showWindow()
                this.switchTab(TABS.oppo)
            }
            
            this.matchTotalNum = 0;
            this.matchInfos = data;

            console.log("Match Info Updated: ")
            console.log(this.matchInfos)

            for (const i in data) {
                // this.matchTotalNum += match.matches
                this.matchTotalNum += data[i].matches

                // when total matchNum bigger than 10, set it to 10 for better display.
                if (this.matchTotalNum > 10) {
                    this.matchTotalNum = 10
                }
            }
            // console.log(this.matchTotalNum)

        },
        handleGameEnd() {
            if (this.IS_ELECTRON) {
                window.ipcRenderer.send("game-end-trigger")
            }
        },
        handleGameStart() {
            if (this.IS_ELECTRON) {
                window.ipcRenderer.send("game-start-trigger")
            }
        },

        onOpenDecklib() {
            this.currentLayer = LAYERS.decklib
        },
        setLayer(newLayer) {
            this.currentLayer = newLayer
        },
        onLayerBack() {
            this.currentLayer -= 1
        },
        onPinOppo(code, id) {
            console.log("Pinning", code, id)
            // this.oppoPinnedCode = code
            this.oppoPinnedId = id
        },
    }

}

</script>