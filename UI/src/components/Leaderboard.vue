<template>
    <!-- <div id="content"> -->

        <!-- <h1 id="title">LoR Master Leaderboard</h1> -->

        <div class="sticky-top">

            <div id="btn-group-regions" class="flex">
                <button id="btn-na" class="btn" :class="{active: activeRegion == 0}" @click="switchRegion(regions.NA)">NA</button>
                <button id="btn-eu" class="btn" :class="{active: activeRegion == 1}"  @click="switchRegion(regions.EU,)">EU</button>
                <button id="btn-as" class="btn" :class="{active: activeRegion == 2}" @click="switchRegion(regions.AS)">AS</button>
                <button id="btn-sea" class="btn" :class="{active: activeRegion == 3}" @click="switchRegion(regions.SEA)">SEA</button>
            </div>

            <div id="search-container">
                <div class="search-icon" v-if="!isLoading"><i class="fa fa-search"></i></div>
                <div class="search-icon loading" v-if="isLoading"><i class="fa fa-circle-notch fa-spin"></i></div>
                <input v-model="searchText"
                    id="search-input" type="text" :placeholder="isLoading ? 'Loading...' : searchPlaceHolder " :disabled="isLoading">
            </div>

            <div class="flex info-help">
                <div class="info-rank">Rank</div>
                <div class="info-name">Name</div>
                <div class="info-lp">Points</div>
            </div>

        </div>

        <div id="ladder">
            
            <leaderboard-player v-for="(player, index) in filteredPlayers" 
                @click="searchPlayer(player)"  
                :key="index" 
                :rank="player.rank + 1" 
                :name="player.name" 
                :lp="player.lp">
            </leaderboard-player>
        </div>

    <!-- </div> -->
</template>

<script>
// const axios = require('axios')
import axios from 'axios'
import LeaderboardPlayer from '../components/LeaderboardPlayer.vue'

const portNum = "26531"
const REGION_ID = {
    NA: 0, EU: 1, AS: 2, SEA: 3
}
const REGION_SHORTS = ['NA', 'EU', 'AS', 'SEA']
const REGION_NAMES = ["americas", "europe", "asia", "sea"]

export default {
    mounted() {
        this.getLeaderboard(this.activeRegion)
    },
    data() {
        return {
            rawPlayers: [],
            activeRegion: 0,
            regions: REGION_ID,
            request: null,
            isLoading: false,
            searchText: "",
            signedIn: false,
            dataStartTime: 0,
        }
    },
    emits: {
        search: ({ region, name, tag }) => {
            if (region && name && tag) {
                return true
            } else {
                console.warn('Invalid submit event payload!')
                return false
            }
        },
    },
    computed: {
        filteredPlayers() {
            if (this.searchText) {
                var searchText = this.searchText
                var filteredPlayers = []
                var prefilteredPlayer = this.rawPlayers
                for (var i = 0; i < prefilteredPlayer.length; i++) {
                    if (prefilteredPlayer[i].name.toLowerCase().indexOf(searchText.toLowerCase()) !== -1) {
                        filteredPlayers.push(prefilteredPlayer[i])
                    }
                }
                // return this.players[this.activeRegion].filter(function(player) {
                //     return player.name.toLowerCase().indexOf(searchText.toLowerCase()) !== -1
                // })

                return filteredPlayers
            }
            return this.rawPlayers;
        },
        searchPlaceHolder() {
            if (this.rawPlayers) {
                return "Search "+ this.rawPlayers.length +" players"
            } else {
                return "Search"
            }
        },
    },
    components: { LeaderboardPlayer },
    methods: {
        getLeaderboard(regionID) {

            this.isLoading = true

            var region = REGION_NAMES[regionID]

            if (this.request) this.cancelLeaderboard()
            const axiosSource = axios.CancelToken.source()
            this.request = { cancel: axiosSource.cancel, msg: "Loading..." }

            var api_link = `http://127.0.0.1:${portNum}/leaderboard/${region}`

            axios.get(api_link, {cancelToken: axiosSource.token} )
            .then((res) => {
                this.rawPlayers = res.data
                this.isLoading = false
            })
            .catch((e) => {
                if (axios.isCancel(e)) {
                    console.log("Request cancelled")
                } else 
                { 
                    console.log('error', e) 
                    this.getLeaderboard(regionID)
                }
            })
        },

        cancelLeaderboard() {
            this.request.cancel()
        },

        switchRegion(regionID) {

            if (this.activeRegion != regionID) {
                
                this.getLeaderboard(regionID)
                this.activeRegion = regionID
                
            }

        },

        searchPlayer(player) {
            // console.log("In leaderboard", player)
            var data = player;
            data.region = REGION_SHORTS[this.activeRegion]
            this.$emit('search', data)
        },
    }

}
</script>

<style scoped>

    .info-help {
        color: white;
        background-color: var(--col-light-grey);
        width: 100%;
        height: 30px;
        padding: 5px 0px;
        margin: 20px 0px 0px 0px;
        align-items: center;
        justify-content: space-around;
        border-radius: 5px;
    }

    .info-rank {
        width: 9.6%;
        text-align: center;
    }

    .info-name {
        width: 53.8%;
        text-align: left;
    }

    .info-lp {
        width: 9.6%;
        text-align: center;
    }

    /* Search */
    
    .sticky-top {
        position: sticky;
        top: 0;
        background: var(--col-background);
        padding-bottom: 5px;
    }

    #search-container {
        position: relative;
        margin-top: 15px;
        /* width: 420px; */
        height: 50px;
    
    }

    #search-input {
        color: white;
        
        font-size: 16px;

        width: 100%;
        height: 100%;
        
        border: none;
        background-color: var(--col-darker-grey);
        padding: 20px 20px 20px 50px;
        border-radius: 40px;
        box-sizing: border-box;
    }

    #search-input:focus {
        outline: none;
        background-color: var(--col-dark-grey);
        /* box-shadow: 0px 0px 10px 2px var(--col-gold); */
    }

    .search-icon {
        position: absolute;
        width: 36px;
        height: 50px;
        line-height: 50px;
        vertical-align: middle;

        left: 10px;
        color: var(--col-dark-white);
    }


    #btn-menu {
        /* display: block; */
        display: none;
        position: relative;
        top: 0px;
        left: 0px;;
    }

    #container {
        color: white;
    }

    #content {
        display: flex;
        flex-direction: column;

        width: 100%;

        align-items: center;
    }

    #title {
        margin-top: 0px;
        margin-bottom: 40px;
    }

    #btn-group-regions {
        border-radius: 5px;
    }

    #btn-group-regions .btn {
        background-color: transparent;
        color: var(--col-gold);

        width: 60px;
        height: 32px;

        font-size: 16px;

        cursor: pointer;

        border: 0px;
        border-bottom: 2px transparent solid;
    }

    #btn-group-regions .btn:hover {
        border-bottom: 2px var(--col-gold) solid;
    }

    #btn-group-regions .btn:focus {
        outline: 0px;
    }

    #btn-group-regions .btn.active {
        color: white;
        border-bottom: 2px var(--col-gold) solid;
    }


    /* Ladder  */
    #ladder {        
        
        margin-bottom: 25px;
        /* color: white; */
        display: flex;
        flex-direction: column;
        /* width: 520px; */
        gap: 5px;

        
    }

    /* @media only screen and (max-width: 768px) {
        #ladder {
            width: 400px;
        }
    } */

</style>