<template>
    <base-window-controls :playerName="playerName" :playerRank="playerRank"></base-window-controls>
    
    <div id="content">

        <div class="loading" :class="{invisible: !isLoading}">
            {{loadingText}}
        </div> 
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

        <div id="history">
            
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

        <div class="footer"></div>

    </div>
</template>


<script>

// import WindowControl from '../components/BaseWindowControl.vue'
import MatchInfo from '../components/MatchInfo.vue'
import axios from 'axios'
import BaseWindowControls from '../components/BaseWindowControls.vue'

const requestDataWaitTime = 1000 // ms

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
            matchInfos: [],
            request: null,
            playerName: null,
            playerRank: null,
            matchTotalNum: 0
        }
    },
    computed: {
        isLoading() {
            return (this.playerName == null || this.playerName == "" || this.matchInfos.length == 0)
            // return true
        },
        loadingText() {
            return 'Loading..'
        }
    },
    components: { 
        BaseWindowControls,
        MatchInfo,
    },
    methods: {
        getMatchInfo() {

            // const APILink = "https://run.mocky.io/v3/1b944261-e5c2-4071-bf22-a8c5e509edeb"
            const APILink = "https://run.mocky.io/v3/32d5b3e2-fd92-49a4-90eb-13a2b027d8e3"
            
            if (this.request) this.cancelLeaderboard()
            const axiosSource = axios.CancelToken.source()
            this.request = { cancel: axiosSource.cancel, msg: "Loading..." };

            // var APILink = test_api_links[regionID]
            this.isLoading = true;

            axios.get(APILink, {cancelToken: axiosSource.token} )
            .then((data) => {
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
                console.log("Requested data")
                const [result] = await window.request.receive()
                // this.playerName = result.toString()
                
                console.log("Received data")
                // console.log(result.toString())
                
                this.processRawData(result)
                await this.requestDataAgain()
                this.requestData()

            } else {
                this.getMatchInfo()
            }            
        },
        processRawData(raw) {
            var data = JSON.parse(raw.toString('utf8'))
            console.log("Processing Received Data:", raw.toString('utf8'))
            this.processJsonData(data)
        },
        processJsonData(data) {
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
        width: 300px;
    }

    #content {
        margin-top: 40px;
    }

    .footer {
        height: 50px;
    }

</style>