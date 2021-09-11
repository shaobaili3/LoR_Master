<template>
    <base-window-controls :canClose="false" :canShrink="true" :playerName="oppoName" :playerRank="oppoRank" :titleType="infoType" :deck="deckCode"></base-window-controls>
    
    <div id="content">

        <div class="loading" :class="{invisible: !isLoading}">
            {{loadingText}}
        </div> 

        <div class="errorText" v-if="isInvalidDeckCode && isShowCode">Invalid Deck Code</div>
        <!-- <button @click="requestData">Test Request</button> -->

        <!-- <div id="history-stats"> -->
            <!-- <div>10-game win rate: 90%</div> -->
            <!-- {{oppoName}} -->
        <!-- </div> -->

        <!-- <div id="search-container">
            <div id="search-icon"><i class="fa fa-search"></i></div>
            <input id="search-input" type="text" placeholder="Search...">
        </div> -->

        <!-- <div id="opponent">
            {{oppoName}}
        </div> -->

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
            <!-- <div class="tab-title" @click="showCode" :class="{active: isShowCode}">Code</div> -->
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

        <div class="footer"></div>

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
const portNum = "63312"

const TABS = {
    oppo: 0,
    my: 1,
    code: 2,
    oppog: 3,
    myg: 4,
}

var lastTrackTime, lastServerRequestTime;

export default {
    mounted() {
        // console.log(JSON.stringify(this.matchInfos))
        // this.getMatchInfo()
        // this.getSubData()
        // console.log("Mounted")
        // this.requestData()
        this.infoType = "match"

        this.requestTrackInfo()
        this.requestServerInfo()
        // this.requestOpponentHistory()
        // console.log("Test")
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

            currentDeckCode: null,
            startingDeckCode: null,
            oppoGraveCode: null,
            myGraveCode: null,
            oppoName: null,
            oppoRank: null,
            oppoTag: null,
        }
    },
    computed: {
        isLoading() {
            if (this.infoType == "deckCode" && this.deckCode != "") return false
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
    components: { 
        BaseWindowControls,
        MatchInfo,
        MatchInfoDeckDetail,
        DeckRegions,
        DeckDetailBase,
        // MatchInfoDeckPreview,
    },
    methods: {
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
        requestDataAgain() {
            return new Promise(resolve => {
                setTimeout(() => {
                    resolve('Requesting new Data')
                }, requestDataWaitTime);
            })
        },
        async requestOpponentHistory() {
            // http://192.168.20.4:${portNum}/history/asia/J01/J01

            console.log("Request Opponent History for " + this.oppoName + "#" + this.oppoTag)
            
            axios.get(`http://127.0.0.1:${portNum}/history/${this.server}/${this.oppoName}/${this.oppoTag}`)
                .then((response) => {
                    console.log("Opponent Data", response.data)
                    this.processJsonData(response.data)
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })

        },
        async requestServerInfo() {
            lastServerRequestTime = Date.now()
            
            axios.get(`http://127.0.0.1:${portNum}/process`)
                .then((response) => {
                    // console.log(response.data)

                    var elapsedTime = Date.now() - lastServerRequestTime // milli
                    // console.log("Elapsed ", elapsedTime)
                    
                    this.server = response.data.server

                    // console.log("Server", this.server)

                    if (requestServerWaitTime > elapsedTime) {
                        setTimeout(this.requestServerInfo, requestServerWaitTime - elapsedTime); 
                    } else {
                        this.requestServerInfo()
                    }
                    
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                    this.requestServerInfo()
                })
            
        },
        async requestTrackInfo() {
            // http://192.168.20.4:${portNum}/track

            // console.log("Request Track Info")

            lastTrackTime = Date.now()

            axios.get(`http://127.0.0.1:${portNum}/track`)
                .then((response) => {
                    // console.log(response.data)

                    var elapsedTime = Date.now() - lastTrackTime // milli
                    // console.log("Elapsed ", elapsedTime)
                    
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
                    { console.log('error', e) }
                    this.requestTrackInfo()
                })

            
        },
        processTrackInfo(data) {

            // console.log("Processing Tracker Info")
            // console.log(data)
            
            if (data.opponent_info) {
                var oppoInfo = data.opponent_info;
                if ((oppoInfo.name) && (oppoInfo.tag)) {
                    // console.log("Reading Opponent Info")
                    if ((!this.oppoName) || (this.oppoName.toLowerCase() != oppoInfo.name.toLowerCase())) {
                        // If there is no oppoName set or there is a change in the name
                        this.oppoName = oppoInfo.name
                        this.oppoTag = oppoInfo.tag
                        this.oppoRank = oppoInfo.rank
                        this.requestOpponentHistory()
                    }
                }
                else {
                    this.oppoName = null
                    this.oppoTag = null
                    this.oppoRank = null
                    this.matchTotalNum = 0
                    this.matchInfos = []
                }

                // if (oppoInfo.name) {
                    // this.oppoName = oppoInfo.name
                    // console.log(this.oppoName)
                    // this.makeWindowVisible()
                // }
            } else {
                this.oppoName = null
                this.oppoTag = null
                this.oppoRank = null
                this.matchTotalNum = 0
                this.matchInfos = []
            }

            if (data.deck_tracker) {
                this.startingDeckCode = data.deck_tracker.deckCode
                this.currentDeckCode = data.deck_tracker.currentDeckCode
                this.oppoGraveCode = data.deck_tracker.opGraveyardCode
                this.myGraveCode = data.deck_tracker.myPlayedCardsCode
                // if (data.deck_tracker.deckCode) {
                //     this.makeWindowVisible()
                // }
            } else {
                this.startingDeckCode = null
                this.currentDeckCode = null
                this.myGraveCode = null
                this.oppoGraveCode = null
            }
        },
        processJsonData(data) {

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
        height: 50px;
    }

    .tabs {
        width: calc(100% - 20px);
        max-width: 280px;
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        gap: 10px;
        /* padding: 0px; */
        margin: 10px 0px;
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

    .tab-text {
        padding: 0px 0px 2px 0px;
    }



</style>