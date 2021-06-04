<template>
    <base-window-controls :canClose="false" :canShrink="true" :playerName="playerName" :playerRank="playerRank" :titleType="infoType" :deck="deckCode"></base-window-controls>
    
    <div id="content">

        <div class="loading" :class="{invisible: !isLoading}">
            {{loadingText}}
        </div> 

        <div class="errorText" v-if="isInvalidDeckCode && !showMatch">Invalid Deck Code</div>
        <!-- <button @click="requestData">Test Request</button> -->

        <!-- <div id="history-stats"> -->
            <!-- <div>10-game win rate: 90%</div> -->
            <!-- {{playerName}} -->
        <!-- </div> -->

        <!-- <div id="search-container">
            <div id="search-icon"><i class="fa fa-search"></i></div>
            <input id="search-input" type="text" placeholder="Search...">
        </div> -->

        <!-- <div id="opponent">
            {{playerName}}
        </div> -->

        <div id="history" v-if="showMatch">
            
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

        <deck-regions v-if="!showMatch" :deck="deckCode"></deck-regions>
        <!-- <match-info-deck-preview v-if="!showMatch" :deck="deckCode" :won="true"></match-info-deck-preview> -->
        <match-info-deck-detail v-if="!showMatch" :deck="deckCode"></match-info-deck-detail>

        <div class="footer"></div>

    </div>
</template>


<script>

// import WindowControl from '../components/BaseWindowControl.vue'
import MatchInfo from '../components/MatchInfo.vue'
import axios from 'axios'
import BaseWindowControls from '../components/BaseWindowControls.vue'
import MatchInfoDeckDetail from '../components/MatchInfoDeckDetail.vue'
import DeckRegions from '../components/DeckRegions.vue'
// import MatchInfoDeckPreview from '../components/MatchInfoDeckPreview.vue'
import DeckEncoder from '../modules/runeterra/DeckEncoder'

const requestDataWaitTime = 200 // ms

export default {
    mounted() {
        // console.log(JSON.stringify(this.matchInfos))
        // this.getMatchInfo()
        // this.getSubData()
        console.log("Mounted")
        this.requestData()
        // console.log("Test")
    },
    data() {
        return {
            rawDataString: null,
            matchInfos: [],
            request: null,
            playerName: null,
            playerRank: null,
            matchTotalNum: 0,
            infoType: null,
            deckCode: null,
            titleType: null
        }
    },
    computed: {
        isLoading() {
            if (this.infoType == "deckCode" && this.deckCode != "") return false
            return (this.playerName == null || this.playerName == "" || this.matchInfos.length == 0)
            // return true
        },
        loadingText() {
            return 'Loading..'
        },
        showMatch() {
            if (this.infoType == "deckCode") {
                return false
            }
            return true
        },
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
        // MatchInfoDeckPreview,
    },
    methods: {
        getMatchInfo() {

            // const APILink = "https://run.mocky.io/v3/1b944261-e5c2-4071-bf22-a8c5e509edeb"
            const APILink = "https://run.mocky.io/v3/ed898fe9-570b-476b-824d-a8fd93c4d331"            
            
            if (this.request) this.cancelLeaderboard()
            const axiosSource = axios.CancelToken.source()
            this.request = { cancel: axiosSource.cancel, msg: "Loading..." };

            // var APILink = test_api_links[regionID]
            this.isLoading = true;

            axios.get(APILink, {cancelToken: axiosSource.token} )
            .then((data) => {
                var d = data.data
                // Testing 6 Champs
                // d.matches[0].deckCode = "CMBQCAQAAMAQIAAHBAAQAAIGBEFRIGRCE4BACAIAEQAQIAAJAMAQEAAGAEBQACYEAEAAYFRKFU"
                
                // Testing singleton
                d.matches[0].deckCode = "CMAAABQBAMDA6AQEAQFA4BADAQCAYEQZBEAQIAIIBIKBWHBEFY3QYAQGBEFA2EQUFAWC4LZQHI6AYAYJBEIR2JZKGA4ESVSY2YA5SAI"
                d.matches[1].deckCode = "CMBACAQAAMEACAABAYEQWFA2EITQEAIBAASAEBAAA4EQIAIBAEPACAQAAYAQGAALAQAQADAWFIWQ"
                this.processJsonData(data.data)
            })
            .catch((e) => {
                if (axios.isCancel(e)) {
                    console.log("Request cancelled");
                } else 
                { console.log('error', e) }
            })
        },
        async getSubData() {
            if (window.sock)
            for await (const [topic, msg] of window.sock) {
                // console.log("Received Sub:", topic.toString(), " message:", msg.toString())
                // this.playerName = msg.toString()
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
        async requestData() {

            if (window.request) {
                await window.request.send("0")
                // console.log("Requested data")
                const [result] = await window.request.receive()
                // this.playerName = result.toString()
                
                // console.log("Received data")
                // console.log(result.toString())
                
                this.processRawData(result)
                await this.requestDataAgain()
                this.requestData()

            } else {
                this.getMatchInfo()
            }            
        },
        processRawData(raw) {
            var rawString = raw.toString('utf8')
            if (this.rawDataString == rawString) return

            console.log("Old:", this.rawDataString)
            console.log("New:", rawString)
            
            this.rawDataString = rawString
            var data = JSON.parse(rawString)
            // console.log("Processing Received Data:", raw.toString('utf8'))
            this.processJsonData(data)
        },
        processJsonData(data) {

            if ((data.type == "deckCode" && data.deckCode != "") || 
            !(data.name == null || data.name == "" || data.matches.length == 0)) {
                window.showWindow()
                }
            
            this.infoType = data.type // match or deckCode
            this.deckCode = data.deckCode
            // console.log(this.deckCode)

            // if ()
            this.matchTotalNum = 0;
            this.matchInfos = data.matches;

            // console.log("Match Information")
            for (const i in data.matches) {
                // this.matchTotalNum += match.matches
                this.matchTotalNum += data.matches[i].matches
            }
            // console.log(this.matchTotalNum)

            this.playerName = data.name;
            this.playerRank = data.rank;
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

</style>