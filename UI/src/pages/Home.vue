<template>
    <base-window-controls :playerName="playerName" :playerRank="playerRank"></base-window-controls>
    
    <div id="content">

        <div class="loading" :class="{invisible: playerName == null ? false : true}">
            Loading..
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
                :deck="match.deck"
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

export default {
    mounted() {
        // console.log(JSON.stringify(this.matchInfos))
        // this.getMatchInfo()
        this.getSubData()
        this.requestData()
        // console.log("Test")
    },
    data() {
        return {
            matchInfos: [],
            request: null,
            playerName: null,
            playerRank: null,
        }
    },
    computed: {
    },
    components: { 
        BaseWindowControls,
        MatchInfo,
    },
    methods: {
        getMatchInfo() {

            // for await (const [topic, msg] of window.sock) {
            //     console.log("received a message related to:", topic.toString(), "containing message:", msg.toString())
            //     // window.testData = msg.toString()
            //     // console.log(mainWindow)
            // }

            // console.log("Get Match Info")
            // Version with Name and Opponent Deck
            // const APILink = "https://run.mocky.io/v3/ed5ffaec-c040-4a62-839c-e52966cae1d6"
            
            // winrate
            // const APILink = "https://run.mocky.io/v3/febc2c8b-4437-4dea-92f0-8c3384a8adf5"
            
            // Name, winrate, extra player and match infos
            const APILink = "https://run.mocky.io/v3/1b944261-e5c2-4071-bf22-a8c5e509edeb"
            
            
            if (this.request) this.cancelLeaderboard()

            const axiosSource = axios.CancelToken.source()
            this.request = { cancel: axiosSource.cancel, msg: "Loading..." };

            // var APILink = test_api_links[regionID]

            this.isLoading = true;

            axios.get(APILink, {cancelToken: axiosSource.token} )
            .then((data) => {
                // Testing Shurima expansion
                // data.data.matches[0].deck = "CECQMBAHAMNBYJRTLUAQCAAWAEBQADQBAQAAGAICAAEQGAQCAABAQAQBAAETGAIEA44QA";
                this.matchInfos = data.data.matches;
                this.playerName = data.data.name;
                this.playerRank = data.data.rank;
                // console.log(this.matchInfos);
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
        async requestData() {
            
            await window.request.send("0")
            console.log("Requested data")
            const [result] = await window.request.receive()
            // this.playerName = result.toString()
            this.processRawData(result)
            
        },
        processRawData(raw) {
            var data = JSON.parse(raw.toString())
            console.log("Processing Received Data:", data)

            this.matchInfos = data.matches;
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