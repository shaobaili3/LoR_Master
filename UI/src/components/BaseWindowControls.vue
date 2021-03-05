<template>
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
          return 'Rank ' + this.playerRank
      }
  },
  // components: {
  //   MainLayout
  // }
  methods: {
      hideApp() {
        window.minWindow()
      },
      closeApp() {
        window.closeWindow()
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

        /* position: fixed;  */
        top: 0px;
        left: 0px;

        /* flex-direction: column; */
        align-items: center;
        justify-content: flex-end;

        height: 20px;
        padding: 10px 0px;
        width: 100%;

        margin-left: 0px;
    }

    .menu-title {
        left: 0;
        margin-left: 16px;
        /* margin-right: auto; */
        color: white;
        font-size: 1.2em;
    }

    .menu-sub-title {
        left: 0;
        margin-left: 10px;
        margin-right: auto;
        color: rgba(255, 255, 255, 0.5);
    }

    .menu-item {
        display: flex;
        /* border: 1px var(--col-gold)enrod solid; */
        color: var(--col-gold);
        /* background-color:white; */
        -webkit-app-region: no-drag;

        width: 40px;
        height: 60px;
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