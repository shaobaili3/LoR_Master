<template>
    <base-window-controls :playerName="playerName" :playerRank="playerRank"></base-window-controls>
    <div id="content">

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
        this.getMatchInfo()
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
        }
    }

}

// Retrieve remote BrowserWindow
// const {BrowserWindow} = require('electron').remote

// function init() {
//     // Minimize task
//     document.getElementById("min-btn").addEventListener("click", (e) => {
//         var window = BrowserWindow.getFocusedWindow();
//         window.minimize();
//     });

//     // Maximize window
//     document.getElementById("max-btn").addEventListener("click", (e) => {
//         var window = BrowserWindow.getFocusedWindow();
//         if(window.isMaximized()){
//             window.unmaximize();
//         }else{
//             window.maximize();
//         }
//     });

//     // Close app
//     document.getElementById("close-btn").addEventListener("click", (e) => {
//         var window = BrowserWindow.getFocusedWindow();
//         window.close();
//     });
// };

// document.onreadystatechange =  () => {
//     if (document.readyState == "complete") {
//         init();
//     }
// };

// const match1Info = {
//     opponentName: "Bike",
//     round: 25,
//     deck: "CICACAQAAEBACAA2FUBQGAAFBIFQGAYJENKVMAQBAEAASBIDBEBCMSC4MQAQCAIACU", 
//     oppdeck: "CIBQEAIABENAEAYAAUFASAYJBERTSVCVKZLWAZAAAEAQCAAH",
//     won: true
// }

// const match2Info = {
//     opponentName: "Ace",
//     round: 25,
//     deck: "CICACAQAAEBACAA2FUBQGAAFBIFQGAYJENKVMAQBAEAASBIDBEBCMSC4MQAQCAIACU", 
//     oppdeck: "CIBQEAIABENAEAYAAUFASAYJBERTSVCVKZLWAZAAAEAQCAAH",
//     won: false
// }

// const match3Info = {
//     opponentName: "Cat",
//     round: 15,
//     deck: "CICACAQAAEBACAA2FUBQGAAFBIFQGAYJENKVMAQBAEAASBIDBEBCMSC4MQAQCAIACU", 
//     oppdeck: "CIBQEAIABENAEAYAAUFASAYJBERTSVCVKZLWAZAAAEAQCAAH",
//     won: false
// }

</script>

<style scoped>

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

    .footer {
        height: 50px;
    }

    /* @media only screen and (max-width: 768px) {
        #history {
            width: 400px;
        }
    } */

</style>