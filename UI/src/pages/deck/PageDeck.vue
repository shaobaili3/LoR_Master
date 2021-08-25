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
            <div class="tab-title" @click="showOppo" :class="{active: isShowOppo}">Opp.</div>
            <div class="tab-title" @click="showMy" :class="{active: isShowMy}">My</div>
            <!-- <div class="tab-title" @click="showCode" :class="{active: isShowCode}">Code</div> -->
        </div>

        <div id="history" class="tab-content" v-if="isShowOppo">
            
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

        <div class="tab-content" v-if="isShowMy">
            <deck-regions :deck="currentDeckCode"></deck-regions>
            <!-- <match-info-deck-detail :deck="myDeck.currentDeckCode"></match-info-deck-detail> -->
            <deck-detail-base :deck="currentDeckCode" :baseDeck="startingDeckCode"></deck-detail-base>
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

const requestDataWaitTime = 500; // ms

const TABS = {
    oppo: 0,
    my: 1,
    code: 2
}

export default {
    mounted() {
        // console.log(JSON.stringify(this.matchInfos))
        // this.getMatchInfo()
        // this.getSubData()
        console.log("Mounted")
        // this.requestData()
        this.requestTrackInfo()
        // this.requestOpponentHistory()
        // console.log("Test")
    },
    data() {
        return {
            rawDataString: null,
            matchInfos: [],
            request: null,
            
            matchTotalNum: 0,
            infoType: null,
            deckCode: null,
            titleType: null,
            currentTab: TABS.oppo,
            myDeck: null,
            currentDeckCode: null,
            startingDeckCode: null,
            oppoName: null,
            oppoRank: null,
            
            oppoTag: null,
        }
    },
    computed: {
        isLoading() {
            // console.log(this.myDeck)
            if (this.infoType == "deckCode" && this.deckCode != "") return false
            if (this.myDeck && this.myDeck.deckCode) return false
            if (this.matchInfos.length > 0) return false
            return (this.oppoName == null || this.oppoName == "" || this.matchInfos.length == 0)
            // return true
        },
        loadingText() {
            return 'Loading..'
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
                console.log(err.message)
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
        showOppo() {
            this.currentTab = TABS.oppo
        },
        showMy() {
            this.currentTab = TABS.my
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
            // http://192.168.20.4:6123/history/asia/J01/J01

            console.log("Request Opponent History for " + this.oppoName + "#" + this.oppoTag)
            
            axios.get(`http://127.0.0.1:6123/history/${this.server}/${this.oppoName}/${this.oppoTag}`)
                .then((response) => {
                    console.log(response.data)
                    this.processJsonData(response.data)
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })

        },
        async requestTrackInfo() {
            // http://192.168.20.4:6123/track

            console.log("Request Track Info")

            axios.get(`http://127.0.0.1:6123/track`)
                .then((response) => {
                    console.log(response.data)
                    
                    this.processTrackInfo(response.data)
                    this.requestTrackInfo()
                })
                .catch((e) => {
                    if (axios.isCancel(e)) {
                        console.log("Request cancelled");
                    } else 
                    { console.log('error', e) }
                })

            
        },
        processTrackInfo(data) {
            if (data.opponent_info) {
                var oppoInfo = data.opponent_info;
                if ((oppoInfo.name) && (oppoInfo.tag) && (oppoInfo.server)) {

                    console.log("Reading Opponent Info")

                    if ((!this.oppoName) || (this.oppoName.toLowerCase() != oppoInfo.name.toLowerCase())) {
                        // If there is no oppoName set or there is a change in the name
                        this.oppoName = oppoInfo.name
                        this.oppoTag = oppoInfo.tag
                        this.oppoRank = oppoInfo.rank
                        this.server = oppoInfo.server

                        this.requestOpponentHistory()
                    }
                }
                // else {

                //     console.log("Test Opponent Info")

                //     if (!this.oppoName || this.oppoName.toLowerCase() != "storm") {
                //         console.log(this.oppoName)
                //         this.oppoName = "Storm"
                //         this.oppoTag = "5961"
                //         this.server = "americas"

                //         this.requestOpponentHistory()
                //     }
                    
                // }
            }

            if (data.deck_tracker) {
                this.startingDeckCode = data.deck_tracker.deckCode
                this.currentDeckCode = data.deck_tracker.currentDeckCode
            }
        },
        processJsonData(data) {

            // Process New Data

            // if ((data.type == "deckCode" && data.deckCode != "" && data.deckCode != this.deckCode)) {
                // Changes Deck Code
                // Make window appear to display deck code
                // window.showWindow()
                // Switches to code tab
                // this.showCode()
            // } else 
            if (JSON.stringify(this.matchInfos) != JSON.stringify(data.matches)) {
                // Changes Match Info
                window.showWindow()
                this.showOppo()
            }
            
            // this.infoType = data.type // match or deckCode
            this.infoType = "match"
            // this.deckCode = data.deckCode
            // console.log(this.deckCode)

            // this.myDeck = data.myDeck
            // console.log(this.myDeck.currentDeckCode)

            // if ()
            this.matchTotalNum = 0;
            this.matchInfos = data.matches;

            // console.log("Match Information")
            for (const i in data.matches) {
                // this.matchTotalNum += match.matches
                this.matchTotalNum += data.matches[i].matches

                // when total matchNum bigger than 10, set it to 10 for better display.
                if (this.matchTotalNum > 10) {
                    this.matchTotalNum = 10
                }
            }
            // console.log(this.matchTotalNum)

            // this.oppoName = data.name;
            // this.oppoRank = data.rank;
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
        gap: 5px;
        /* padding: 0px; */
        margin: 10px 0px;
    }

    .tab-title {
        flex: 1 1 0;
        color: var(--col-lighter-grey);
        cursor: pointer;
        text-align: center;
        background: var(--col-dark-grey);
        padding: 5px 0px;
        border-radius: 20px;
    }

    .tab-title:hover {
        color: white
    }

    .tab-title.active {
        color: white;
    }

    .tab-content {
        max-width: 280px;
        width: 100%;
    }

</style>