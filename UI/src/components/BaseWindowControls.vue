<template>
    <div id="menu-bg"></div>
    <div id="menu" class="">
        <div class="window-title" v-if="titleType=='window'">
            {{title}}
        </div>
        <div class="menu-title" v-if="titleType=='match'">
            {{playerName}}
        </div>
        <div class="menu-title-deck" v-if="titleType=='deckCode'">Deck Info</div>
        <div class="menu-sub-title" v-if="titleType=='match' && playerRank">
            <i class="fas fa-trophy"></i> {{playerRank}}
        </div>
        <div class="menu-fill"></div>
        <div v-if="canMin" class="menu-item" @click="minApp()">
            <span><i class="fas fa-minus"></i></span>
        </div>
        <div v-if="canShrink" class="menu-item" @click="shrinkToggle()">
            <span v-if="!isWindowMin"><i class="fas fa-compress-alt"></i></span>
            <span v-if="isWindowMin"><i class="fas fa-expand-alt"></i></span>
            
        </div>
        <div v-if="canClose" class="menu-item" @click="closeApp()">
            <span><i class="fas fa-times"></i></span>
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
        title: String,
        playerName: String,
        playerRank: Number,
        titleType: String,
        canShrink: {
            type: Boolean,
            default: false,
        },
        canMin: {
            type: Boolean,
            default: true,
        },
        canClose: {
            type: Boolean,
            default: true,
        }
    },
    mounted() {
        window.addEventListener("resize", this.checkIsMin);
    },
    unmounted() {
        window.removeEventListener("resize", this.checkIsMin);
    },
    computed: {
    },
  // components: {
  //   MainLayout
  // }
    methods: {
        shrinkToggle() {
            window.toggleShrinkWindow() // Defined in appsrc > preload.js
        },
        minApp() {
            window.minWindow() // Defined in appsrc > preload.js
            //   console.log("Closing App")
        },
        closeApp() {
            window.hideWindow()
        },
        checkIsMin() {
            if (window.isMin)
                this.isWindowMin = window.isMin()
        }
    },
    data() {
        return {
            isWindowMin: false
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

    .window-title {
        color: white;
        position: absolute;
        left: 12px;
    }

    .menu-title {
        left: 0;
        margin-left: 16px;
        /* margin-right: auto; */
        color: white;
        font-size: 1.0em;

        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .menu-sub-title {
        left: 0;
        margin-left: 10px;
        /* margin-right: auto; */
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9em;

        /* direction: rtl; */

        white-space: nowrap;
        /* overflow: scroll; */
        /* text-overflow: hidden; */
    }

    .menu-fill {
        width: 0px;
        left: 0;
        margin-left: 0px;
        margin-right: auto;
    }

    .menu-title-deck {
        left: 0;
        margin-left: 16px;
        margin-right: auto;
        color: white;
        font-size: 1.0em;
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