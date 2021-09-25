<template>
    <base-window-controls :canClose="false" :canShrink="true" :playerName="oppoName" :playerRank="oppoRank" :titleType="infoType" :deck="deckCode"></base-window-controls>
    
    <div id="content">

        <div class="loading" :class="{invisible: !isLoading}">
            {{loadingText}}
        </div> 

        <div class="errorText" v-if="isInvalidDeckCode && isShowCode">Invalid Deck Code</div>

        <div class="tabs" v-if="!isLoading">
            <div class="tab-title-group">
                <div class="tab-title" @click="showOppo" :class="{active: isShowOppo}">
                    <i class="fas fa-swords"></i>
                </div>
                <div class="tab-title" @click="showOppoGrave" :class="{active: isShowOppoGrave}">
                    <i class="fas fa-tombstone-alt"></i>
                </div>
            </div>
            <div class="tab-title-group">
                <div class="tab-title" @click="showMy" :class="{active: isShowMy}">
                    <i class="fas fa-user-cowboy"></i>
                </div>
                <div class="tab-title" @click="showMyGrave" :class="{active: isShowMyGrave}">
                    <i class="fas fa-tombstone-alt"></i>                
                </div>
            </div>
        </div>

        <div id="history" class="tab-content" v-if="isShowOppo && !isLoading">

            <div class="loading" v-if="matchInfos.length <= 0">{{loadingOppoText}}</div>
            
            <match-info 
                v-for="(match, index) in matchInfos" 
                :key="index"
                :opponentName="match.opponentName" 
                :rounds="match.rounds" 
                :time="match.time"
                :matches="match.matches"
                :winrate="match.winrate"
                :badges="match.badge"
                :opponentDeck="match.opponentDeck" 
                :deck="match.deckCode"
                :total="matchTotalNum"
                :history="match.history"
            ></match-info>

        </div>

        <div class="tab-content" v-if="isShowMy && !isLoading">
            <deck-regions :deck="startingDeckCode"></deck-regions>
            <deck-detail-base :deck="currentDeckCode" :baseDeck="startingDeckCode"></deck-detail-base>
        </div>

        <div class="tab-content" v-if="isShowOppoGrave && !isLoading">
            <div class="tab-text">Opponent Graveyard</div>
            <deck-detail-base :deck="oppoGraveCode" :baseDeck="oppoGraveCode" :showCopy="false"></deck-detail-base>
        </div>

        <div class="tab-content" v-if="isShowMyGrave && !isLoading">
            <div class="tab-text">My Graveyard</div>
            <deck-detail-base :deck="myGraveCode" :baseDeck="myGraveCode" :showCopy="false"></deck-detail-base>
        </div>

        

        <div class="tab-content" v-if="isShowCode">
            <deck-regions :deck="deckCode"></deck-regions>
            <match-info-deck-detail :deck="deckCode"></match-info-deck-detail>
        </div>

        <div class="footer" v-if="!isLoading">
            <div class="footer-text">Cards in Hand: {{cardsInHandNum}}</div>
        </div>

    </div>
</template>


<script>

import MatchInfo from '../../components/MatchInfo.vue'
import axios from 'axios'
import BaseWindowControls from '../../components/BaseWindowControls.vue'
import MatchInfoDeckDetail from '../../components/MatchInfoDeckDetail.vue'
import DeckRegions from '../../components/DeckRegions.vue'
import DeckEncoder from '../../modules/runeterra/DeckEncoder'
import DeckDetailBase from '../../components/DeckDetailBase.vue'

const requestDataWaitTime = 100; // ms
const requestServerWaitTime = 3000; //ms
const requestStatusWaitTime = 1000; //ms

const portNum = "26531"
const API_BASE = `http://127.0.0.1:${portNum}`

const TABS = {
    oppo: 0,
    my: 1,
    code: 2,
    oppog: 3,
    myg: 4,
}

var lastTrackTime, lastServerRequestTime, lastStatusRequestTime;

export default {
    components: { 
        BaseWindowControls,
        MatchInfo,
        MatchInfoDeckDetail,
        DeckRegions,
        DeckDetailBase,
        // MatchInfoDeckPreview,
    },
    mounted() {
        // console.log(JSON.stringify(this.matchInfos))
        // this.getMatchInfo()
        // this.getSubData()
        // console.log("Mounted")
        // this.requestData()
        this.infoType = "match"

        // this.hideWindow()

        this.requestTrackInfo()
        // this.requestServerInfo()
        this.requestStatusInfo()
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

            cardsInHandNum: null,

            currentDeckCode: null,
            startingDeckCode: null,
            oppoGraveCode: null,
            myGraveCode: null,

            oppoName: null,
            oppoRank: null,
            oppoTag: null,
            oppoLp: null,

            lorRunning: false,
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
            return 'Ready to rock 🤘'
        },
        loadingOppoText() {
            if (this.oppoName && this.oppoTag) return "Loading History..."
            return "History unavailable"
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
        }
    },
    methods: {
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
        showOppo() {
            this.currentTab = TABS.oppo
        },
        showMy() {
            this.currentTab = TABS.my
        },
        showOppoGrave() {
            this.currentTab = TABS.oppog
        },
        showMyGrave() {
            this.currentTab = TABS.myg
        },
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
            
            axios.get(`${API_BASE}/history/${this.server}/${this.oppoName}/${this.oppoTag}`)
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
        // requestServerInfo() {
        //     lastServerRequestTime = Date.now()
        //     axios.get(`${API_BASE}/process`)
        //         .then((response) => {
        //             // console.log(response.data)

        //             var elapsedTime = Date.now() - lastServerRequestTime // ms
        //             // console.log("Elapsed ", elapsedTime)
                    
        //             this.server = response.data.server

        //             // console.log("Server", this.server)

        //             if (requestServerWaitTime > elapsedTime) {
        //                 setTimeout(this.requestServerInfo, requestServerWaitTime - elapsedTime); 
        //             } else {
        //                 this.requestServerInfo()
        //             }
                    
        //         })
        //         .catch((e) => {
        //             if (axios.isCancel(e)) {
        //                 console.log("Request cancelled");
        //             } else 
        //             { console.log('error', e) }
        //             this.requestServerInfo()
        //         })
        // },
        requestStatusInfo() {
            // Keeps requesting status
            lastStatusRequestTime = Date.now()
            axios.get(`${API_BASE}/status`)
                .then((response) => {
                    var elapsedTime = Date.now() - lastStatusRequestTime // ms
                    this.server = response.data.server

                    // console.log("Server", this.server)

                    if (requestStatusWaitTime > elapsedTime) {
                        setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime); 
                    } else {
                        this.requestStatusInfo()
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                    this.requestStatusInfo()
                })
        },
        requestOppoInfo() {
            // Getting opponent rank, lp and tag
            // Once per opponent change

            axios.get(`${API_BASE}/opInfo`)
                .then((response) => {
                    var op = response.data
                    if (op.rank !== "") {
                        this.oppoRank = op.rank + 1
                    }
                    this.oppoTag = op.tag
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

            lastTrackTime = Date.now()
            axios.get(`${API_BASE}/track`)
                .then((response) => {

                    var elapsedTime = Date.now() - lastTrackTime // milli
                    
                    this.processTrackInfo(response.data)
                    if (requestDataWaitTime > elapsedTime) {
                        setTimeout(this.requestTrackInfo, requestDataWaitTime - elapsedTime); 
                    } else {
                        this.requestTrackInfo()
                    }
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        // console.log("Request cancelled");
                    } else 
                    { 
                        console.log('error', e) 
                        this.requestTrackInfo()
                    }
                })
            
        },
        processTrackInfo(data) {

            if (data.positional_rectangles && data.positional_rectangles.OpponentName) {
                // Check if there is opponent
                var oppoName = data.positional_rectangles.OpponentName
                
                if ((!this.oppoName) || (this.oppoName.toLowerCase() != oppoName.toLowerCase())) {
                    // If there is no oppoName set or there is a change in the name
                    this.oppoName = oppoName
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
                this.startingDeckCode = data.deck_tracker.deckCode
                this.currentDeckCode = data.deck_tracker.currentDeckCode
                this.oppoGraveCode = data.deck_tracker.opGraveyardCode
                this.myGraveCode = data.deck_tracker.myPlayedCardsCode
                this.cardsInHandNum = data.deck_tracker.cardsInHandNum
                if (data.deck_tracker.deckCode) {
                    this.makeWindowVisible()
                }
            } else {
                if (this.startingDeckCode != null) {
                    // switching from game end
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

                window.showWindow()
                this.showOppo()
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
            window.ipcRenderer.send("game-end-trigger")
        }
    }

}

</script>

<style scoped>

    .invisible {
        display: none;
    }
    
    .loading {
        margin-top: 20px;
        font-size: 1.2em;
    }

    .errorText {
        margin-top: 20px;
        font-size: 1.2em;
    }

    #title {
        margin-top: 0px;
        margin-bottom: 40px;
    
    }

    #subtitle {
        margin-top: 80px;
        margin-bottom: 20px;
    }

    #history {
        /* margin-top: 40px; */
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 280px;
        /* min-width: 270px; */
        width: 100%;

        /* margin: 3px 3px 3px 3px; */

        /* font-size: 0.9em; */
    }

    #content {
        margin-top: 40px;
    }

    .footer {
        display: flex;
        height: 30px;
        position: fixed;
        bottom: 0px;
        width: 100%;
        text-align: center;
        align-content: center;
        justify-content: center;
        padding: 10px;
        background: var(--col-background);
    }

    .tabs {
        display: flex;
        position: sticky;
        top: 40px;
        width: calc(100% - 20px);
        max-width: 280px;
        
        justify-content: space-evenly;
        align-items: center;
        gap: 10px;
        padding: 10px 10px;
        
        z-index: 2;
        background: var(--col-background);
    }

    .tab-title-group {
        flex: 1 1 0;
        display: flex;
        background: var(--col-dark-grey);
        padding: 5px 0px;
        border-radius: 20px;
    }

    .tab-title {
        flex: 1 1 0;
        color: var(--col-lighter-grey);
        cursor: pointer;
        text-align: center;
        background: var(--col-dark-grey);
        padding: 0px 0px;
        border-radius: 20px;
    }

    .tab-title:hover {
        color: white;
        /* background: var(--col-grey); */
    }

    .tab-title.active {
        color: white;
    }

    .tab-content {
        max-width: 280px;
        width: 100%;
        text-align: center;
    }

    /* Styling Deck Content */
    .tab-content .icon-content {
        /* position: sticky;
        z-index: 2;
        top: 90px;
        background: var(--col-background); */
        padding: 0px 0px 5px 0px;
    }

    .tab-text {
        padding: 0px 0px 2px 0px;
    }



</style>