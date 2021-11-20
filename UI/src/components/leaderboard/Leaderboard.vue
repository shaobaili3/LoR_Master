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
                <div class="search-icon left" v-if="!isLoading"><i class="fa fa-search"></i></div>
                <div class="search-icon left loading" v-if="isLoading"><i class="fa fa-circle-notch fa-spin"></i></div>
                <input spellcheck="false" autocomplete='off' v-model="searchText"
                    id="search-input" type="text" :placeholder="isLoading ? $t('str.loading') : searchPlaceHolder " :disabled="isLoading">
                <div class="search-icon right" @click="clearSearch" v-if="searchText!=''"><span><i class="fas fa-times"></i></span></div>
            </div>

            <div class="flex info-help h-10">
                <div class="info-rank">{{$t('leaderboard.rank')}}</div>
                <div class="info-name">{{$t('leaderboard.name')}}</div>
                <div class="info-lp">{{$t('leaderboard.points')}}</div>
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
import LeaderboardPlayer from './LeaderboardPlayer.vue'

const REGION_ID = {
    NA: 0, EU: 1, AS: 2, SEA: 3
}
const REGION_SHORTS = ['NA', 'EU', 'AS', 'SEA']
const REGION_NAMES = ["americas", "europe", "asia", "sea"]

const requestLeaderboardWaitTime = 1000 //ms
var lastLeaderboardRequestTime

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
    props: {
        apiBase: {
            type: String,
            required: true
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
                return this.$t('search.leaderboard.numPlayer', {num: this.rawPlayers.length})
            } else {
                return this.$t('search.leaderboard.base')
            }
        }
    },
    components: { LeaderboardPlayer },
    methods: {
        clearSearch() {
            this.searchText = ""
            document.querySelector("#search-input").focus()
        },
        getLeaderboard(regionID) {

            // Return if using npm run serve
            // if (process.env.NODE_ENV == "development") { return }

            lastLeaderboardRequestTime = Date.now()

            this.isLoading = true

            var region = REGION_NAMES[regionID]

            if (this.request) this.cancelLeaderboard()
            const axiosSource = axios.CancelToken.source()
            this.request = { cancel: axiosSource.cancel, msg: "Loading..." }

            var api_link = `${this.apiBase}/leaderboard/${region}`

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
                    // if (!e.status) {
                    //     console.log("Network Error")
                    //     // return
                    // }

                    var elapsedTime = Date.now() - lastLeaderboardRequestTime // ms
                    if (elapsedTime > requestLeaderboardWaitTime) {
                        setTimeout(() => {this.getLeaderboard(regionID)}, 100);
                    } else {
                        setTimeout(() => {this.getLeaderboard(regionID)}, requestLeaderboardWaitTime - elapsedTime);
                    }
                    
                }
            })
        },

        cancelLeaderboard() {
            this.request.cancel()
        },

        switchRegion(regionID) {

            this.sendUserEvent({
                category: "Main Window Leaderboard",
                action: "Select Region",
                label: REGION_NAMES[regionID],
                value: null,
            })

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


<style lang="scss">

    .info-help {
        color: white;
        background-color: var(--col-light-grey);
        width: 100%;
        padding: 5px 0px;
        margin: 20px 0px 0px 0px;
        align-items: center;
        justify-content: space-around;
        border-radius: 5px;

        white-space: nowrap;
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

        top: 0px;

        color: var(--col-dark-white);

        &.left {
            left: 10px;
        }

        &.right {
            right: 10px;
            cursor: pointer;
        }
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