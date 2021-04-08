<template>
    <div id="menu-bg"></div>
    <div id="menu" class="">
        <div class="menu-title">
            <!-- <slot></slot> -->
            {{playerName}}
        </div>
        <div class="menu-sub-title">
            <!-- <slot></slot> -->
            {{playerRankString}}
        </div>
        <div class="menu-item" @click="hideApp()">
            <span><i class="fa fa-minus"></i></span>
        </div>
        <div class="menu-item" @click="closeApp()">
            <span><i class="fa fa-times"></i></span>
        </div>
        
        <!-- <router-link to="/" class="menu-item"> -->
            <!-- <span><i class="fa fa-home"></i></span> -->
        <!-- </router-link> -->
        <!-- <router-link to="/leaderboard" class="menu-item"> -->
            <!-- <span><i class="fa fa-trophy"></i></span> -->
        <!-- </router-link> -->
        <!-- <router-link to="/profile" class="menu-item">
            <span><i class="fa fa-user"></i></span>
        </router-link> -->
    </div>
</template>

<script>

export default {
    props: {
        playerName: String,
        playerRank: Number,
    },
    computed: {
        playerRankString() {
            if (this.playerRank)
                return 'Rank ' + this.playerRank
            return ''
        }
    },
  // components: {
  //   MainLayout
  // }
    methods: {
        hideApp() {
            window.minWindow() // Defined in appsrc > preload.js
        },
        closeApp() {
            window.closeWindow() // Defined in appsrc > preload.js
            //   console.log("Closing App")
        }
    }
}
</script>

<style scoped>

    #menu {
        -webkit-app-region: drag;

        cursor: default;

        display: flex;

        position: fixed; 
        top: 0px;
        left: 0px;

        /* flex-direction: column; */
        align-items: baseline;
        justify-content: flex-end;

        height: 18px;
        padding: 10px 0px 15px 0px;
        width: 100%;

        margin-left: 0px;
        margin-top: 2px;
        background-color: var(--col-background);
        z-index: 3;
    }

    #menu-bg {

        cursor: default;
        position: fixed; 
        top: 0px;
        left: 0px;

        height: 20px;
        padding: 10px 0px 15px 0px;
        width: 100%;

        margin-left: 0px;
        margin-top: 0px;
        background-color: var(--col-background);
        z-index: 2;
    }

    .menu-title {
        left: 0;
        margin-left: 16px;
        /* margin-right: auto; */
        color: white;
        font-size: 1.0em;
    }

    .menu-sub-title {
        left: 0;
        margin-left: 10px;
        margin-right: auto;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9em;
    }

    .menu-item {
        display: flex;
        /* border: 1px var(--col-gold)enrod solid; */
        color: var(--col-gold);
        /* background-color:white; */
        -webkit-app-region: no-drag;

        width: 40px;
        /* height: 60px; */
        align-items: center;
        justify-content: center;

        font-size: 1em;

        /* border-radius: 0px 10px 0px 0px; */

        /* margin: 10px 0px 10px 0px; */
        /* border-right: 2px solid transparent; */
    }

    .menu-item:hover {
        /* border-right: 2px solid var(--col-gold); */
        color: white;
        cursor: pointer;
    }
    
</style>