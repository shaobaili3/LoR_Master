<template>

  <div class="left-nav-btn mobile-btn" @click="expandLeftNav">
    <span><i class="fas fa-list"></i></span>
  </div>
  <div class="left-nav overflow-y-scroll" :class="{'expanded': leftNavExpanded}">
    <div class="left-nav-btn logo no-click" v-if="!IS_ELECTRON" @mouseenter="showAds">
      <picture>
        <source srcset="@/assets/images/logo/logo.webp" type="image/webp">
        <source srcset="@/assets/images/logo/logo.png" type="image/png">
        <img class="logo" height="50px" src="@/assets/images/logo/logo.png" alt="">
      </picture>
    </div>
    <button class="left-nav-btn tooltip" v-if="IS_ELECTRON"
      :class="{
        selected: currentPage == PANELS.my,
        disabled: !lorRunning
      }" 
      @click="handleProfileClick"
      :disabled="!lorRunning"
    >
      <span class="icon-default"
        v-if="!localHistoryLoading"><i class="fas fa-user-circle"></i></span>
      <span class="icon-default icon-hover"
        v-if="localHistoryLoading"><i class="fas fa-redo-alt fa-spin-fast"></i></span>
      <span class="icon-hover"
        v-if="lorRunning && !localHistoryLoading && !(!hasLocalInfo || localPlayerInfo.server != 'sea') "><i class="fas fa-check"></i></span>
      <span class="icon-hover"
        v-if="lorRunning && !localHistoryLoading && (!hasLocalInfo || localPlayerInfo.server != 'sea')"><i class="fas fa-redo-alt"></i></span>
      
      <div v-if="!lorRunning || !localPlayerInfo.playerId"
        class="tooltiptext right" >{{$t('tooltips.lorlogin')}}</div>
      <div v-if="lorRunning && localPlayerInfo.playerId && !hasLocalInfo"
        class="tooltiptext right" >{{$t('str.error.playerNoHistory')}}</div>
    </button>
    <button class="left-nav-btn" 
      :class="{selected: currentPage == PANELS.search}" 
      @click="setCurrentPage(PANELS.search)">
      <span><i class="fas fa-search"></i></span>
    </button>
    <button class="left-nav-btn" 
      :class="{selected: currentPage == PANELS.leaderboard}" 
      @click="setCurrentPage(PANELS.leaderboard)">
      <span><i class="fas fa-trophy"></i></span>
    </button>
    <button class="left-nav-btn" v-if="IS_ELECTRON || IS_DEV "
      :class="{selected: currentPage == PANELS.decklib}" 
      @click="setCurrentPage(PANELS.decklib)">
      <span><i class="fas fa-star"></i></span>
    </button>
    <button class="left-nav-btn" 
      :class="{selected: currentPage == PANELS.meta}" 
      @click="setCurrentPage(PANELS.meta)">
      <span><i class="fas fa-trees"></i></span>
    </button>
    <button class="left-nav-btn hidden sm:flex"
      :class="{'text-gold-200 light-gold': isOpenBookshelf}"
      @click="toggleBookshelf()">
      <span><i class="fas fa-books"></i></span>
    </button>
    <!-- Divider -->
    <div class=" flex-1 "></div> 
    <button class="left-nav-btn text-gray-300 gray" 
      :class="{selected: currentPage == PANELS.contact}" 
      @click="setCurrentPage(PANELS.contact)">
      <span><i class="fas fa-comment-alt-smile"></i></span>
    </button>
    <button class="left-nav-btn text-gray-300 gray" 
      :class="{
        selected: currentPage == PANELS.settings,
        ' mb-14 ': IS_ELECTRON,
        ' mb-5 ': !IS_ELECTRON 
      }" 
      @click="setCurrentPage(PANELS.settings)">
      <span><i class="fas fa-cog"></i></span>
    </button>
  </div>

  <div class="menu-content hidden sm:grid absolute left-[98px] top-6 bottom-auto z-[120]"
    :class="{'hide': !isOpenBookshelf}"
    @mouseleave="toggleBookshelf()"
  >
    <div class="card" @click="openURL('https://masteringruneterra.com/')">
      <img src="https://masteringruneterra.com/wp-content/uploads/2021/09/MasteringRuneterraWebsiteLogo-300x129.webp">
    </div>
    <div class="card square" @click="openURL('https://runeterraccg.com/')">
      <img src="https://runeterraccg.com/wp-content/uploads/2020/05/RuneterraCCG.com-Square-Logo.png">
    </div>
    
    <div class="card square" @click="openURL('https://www.swimstrim.com/')">
      <img src="https://www.swimstrim.com/packs/media/images/logo-8b7cd382.png">
    </div>
    <div class="card sqaure" @click="openURL(lorNewsURL)">
      <img src="https://images.contentstack.io/v3/assets/blt0eb2a2986b796d29/blt8ba1ec1b0013e362/5ea53af4ae23d30cd1dfb3e4/lor-logo.png">
    </div>
    <div class="card square" @click="openURL('https://runeterra.ar/')">
      <img src="https://cdnruneterra.ar/assets/img/logo_ar_black.png">
    </div>
  </div>
  
  <base-window-controls v-if="IS_ELECTRON" :title="''" :titleType="'window'"></base-window-controls>
  
  <base-top-nav v-if="!IS_ELECTRON"></base-top-nav>

  <div v-if="!IS_ELECTRON" class="mt-[-23px] text-center w-auto min-w-0 pl-4 absolute transition-spacing z-10 invisible md:visible" 
    :class="{'ml-[-300px]': isAdHidden && isAdClosed, 'ml-20': !(isAdHidden && isAdClosed)}">
    <div class="ad overflow-hidden relative block w-[300px] h-[250px] transition-opacity bg-gray-800 rounded-lg"
      @mouseleave="hideAds"
    >
      <button class="absolute top-1 right-1 text-white" @click="closeAds">
        <i class="p-2 fas fa-times"></i>
      </button>
      <div class="w-full h-full">
        <p class="text-lg py-5">Have you tried our <a class="text-xl text-gold-400 cursor-pointer" href="https://lormaster.com" target="_blank"><br>LoR Master Tracker</a> yet?</p>
        <a class="text-xl text-gold-400 cursor-pointer" href="https://lormaster.com" target="_blank"><img src="../../assets/images/promo/tracker.png" alt="" srcset=""></a>
      </div>
    </div>
  </div>
  
  <div class="content" :class="{fullheight: !IS_ELECTRON}" @click="shrinkLeftNav">
    <div class="main-content-container" v-if="currentPage == PANELS.my" @scroll="shrinkLeftNav">
      <player-matches 
        @search="searchPlayer($event)"
        :playerName="localPlayerInfo.name"
        :playerRegion="localPlayerInfo.server"
        :playerRank="localPlayerInfo.rank"
        :playerLP="localPlayerInfo.lp"
        :playerTag="localPlayerInfo.tag"
        :matches="localMatches"
      >
      </player-matches>
    </div>

    <div class="main-content-container search" v-if="currentPage == PANELS.search" @scroll="handleContentScroll">
      <panel-search ref="panelSearch"></panel-search>
    </div>

    <div class="main-content-container leaderboard" v-if="currentPage == PANELS.leaderboard" @scroll="handleContentScroll">
      <leaderboard @search="searchPlayer($event)"></leaderboard>
    </div>

    <div class="main-content-container deck-library" v-if="currentPage == PANELS.decklib" @scroll="handleContentScroll">
      <panel-deck-lib ref="deckLib"></panel-deck-lib>
    </div>

    <div class="main-content-container wide deck-code" v-if="currentPage == PANELS.deckcode" @scroll="handleContentScroll">
      <panel-deck-code :code="pageDeckCode"></panel-deck-code>
    </div>

    <div class="main-content-container meta" v-if="currentPage == PANELS.meta" @scroll="handleContentScroll">
      <panel-meta></panel-meta>
    </div>

    <div class="main-content-container contact" v-if="currentPage == PANELS.contact" @scroll="handleContentScroll">
      <contact-info></contact-info>
    </div>

    <div class="main-content-container settings" v-if="currentPage == PANELS.settings" @scroll="handleContentScroll">
      <panel-settings></panel-settings>
    </div>
  </div>

  <div class="deck-content-container" :class="{hide: !isShowDeck, fullheight: !IS_ELECTRON}">
    <div class="deck-content-top-bar">
      <button class="collapse-btn" @click="hideDeck"><span><i class="fas fa-chevron-right"></i></span></button>
      <deck-regions :deck="deckCode" :fixedWidth="false"></deck-regions>
    </div>
    <div class="deck-content-detail" :fixedHeight="!IS_ELECTRON">
      <deck-detail :baseDeck="deckCode" :fixedHeight="true" :showURL="true"></deck-detail>
    </div>
  </div>

  <div class="bottom-bar" v-if="IS_ELECTRON">
    <div class="left">
      <div class="app-name url" @click="openURL('https://www.lormaster.com')">{{ $t("appName") }}</div>
      <div v-if="!localApiEnabled && lorRunning && IS_ELECTRON" class="api-warning warning"><small><i class="fas fa-exclamation-triangle"></i>{{ $t("str.error.localApiError")}}</small></div>
    </div>
    <div class="right">
      <!-- <div class="version download tooltip" v-if="!isUpdatedVersion" @click="openURL(downloadUrl)">
        <span class="tooltiptext">
          <i class="fas fa-arrow-to-bottom"></i> {{remoteVersion}}
        </span>
        <i class="fas fa-exclamation-triangle"></i> {{version}}</div> -->
      <div class="version tooltip"
      :class="{download: updateDownloaded}"
      @click="installDownloadedUpdate()"
      >
        <span class="tooltiptext top-bottom-right">
          <span v-if="isUpdatedVersion"><i class="fas fa-check"></i></span>{{versionTooltip}}
        </span>
        <i class="fas" :class="{'fa-redo-alt': updateDownloaded}"></i>
        {{versionText}}</div>
    </div>
  </div>

  <div class="pop-clipboard" v-if="clipboardDeck">
    <div class="pop-title">{{$t('str.clipboard')}}</div>
    <deck-preview :deck="clipboardDeck" @click="processPaste"></deck-preview>
  </div>
</template>

<script>

// Styles

import '../../assets/scss/tooltips.scss'
import '../../assets/scss/home.scss'
import '../../assets/scss/transitions.scss'

import BaseWindowControls from '../../components/base/BaseWindowControls.vue'
import axios from 'axios'
import DeckRegions from '../../components/deck/DeckRegions.vue'
import Leaderboard from '../../components/leaderboard/Leaderboard.vue'
import PlayerMatches from '../../components/match/PlayerMatches.vue'
import DeckDetail from '../../components/deck/DeckDetail.vue'

import ContactInfo from '../../components/base/ContactInfo.vue'

import { mapActions } from 'vuex'
import PanelSearch from '../../components/panels/PanelSearch.vue'
import PanelDeckLib from '../../components/panels/PanelDeckLib.vue'
import DeckPreview from '../../components/deck/DeckPreview.vue'

import '../../assets/scss/responsive.scss'
import BaseTopNav from '../../components/base/BaseTopNav.vue'

const requestDataWaitTime = 400 //ms
const requestHistoryWaitTime = 100 //ms
const requestStatusWaitTime = 1000 //ms
const inputNameListLength = 10;

// IS_ELECTRON & IS_DEV defined in template.js

import { locales as cardLocales, localeNames as cardLocaleNames} from '../template'
import PanelDeckCode from '../../components/panels/PanelDeckCode.vue'
import PanelMeta from '../../components/panels/PanelMeta.vue'

import {
  REGION_ID, REGION_SHORTS, REGION_NAMES
} from "../../components/leaderboard/Leaderboard.vue"
import PanelSettings from '../../components/panels/PanelSettings.vue'

// import ua from 'universal-analytics'

// const portNum = "26531"
// const API_BASE = `http://127.0.0.1:${portNum}`

let cancelToken, localCancleToken
var lastStatusRequestTime
var requestHistoryTimeout, prevHistoryRequest

const regionNames = {
  'NA': 'americas',
  'EU': 'europe',
  'AS': 'asia',
}

const regionShort = {
  'americas': 'NA',
  'europe' : 'EU',
  'asia' : 'AS',
}

const PANELS = {
  my: 0,
  search: 1,
  leaderboard: 2,
  decklib: 3,
  deckcode: 4,
  meta: 5,
  contact: 6,
  settings: 7,
}

function setCookie(name, value, expDay, expHour, expMin) {
  let date = new Date();
  date.setTime(date.getTime() + (expDay * 24 * 60 * 60 * 1000) + (expHour * 60 * 60 * 1000) + (expMin * 60 * 1000));
  const expires = "expires=" + date.toUTCString();
  document.cookie = name + "=" + value + "; " + expires + "; path=/";
}

function getCookie(name) {
  const cname = name + "=";
  const decoded = decodeURIComponent(document.cookie); //to be careful
  const arr = decoded .split('; ');
  let res;
  arr.forEach(val => {
      if (val.indexOf(cname) === 0) res = val.substring(name.length);
  })
  return res;
}

export default {
  components: {
    BaseWindowControls,
    DeckRegions,
    Leaderboard,
    PlayerMatches,
    DeckDetail,
    ContactInfo,
    PanelSearch,
    PanelDeckLib,
    DeckPreview,
    BaseTopNav,
    PanelDeckCode,
    PanelMeta,
    PanelSettings
},
  data() {
    return {
      // rawDataString: null,
      
      regions: REGION_SHORTS,

      isShowDeck: false,
      deckCode: null,

      isOpenBookshelf: false,

      version: "",
      remoteVersion: "",
      downloadUrl: null,
      updateProcess: 0,
      updateDownloaded: false,

      currentPage: PANELS.leaderboard,
      pageDeckCode: null,

      PANELS: PANELS,

      lorRunning: null,
      localApiEnabled: true,
      localMatches: [],
      localPlayerInfo: {}, // playerId, server, language, rank, lp
      localHistoryLoading: false,
      localHistoryWaiting: false,

      

      clipboardDeck: null,
      leftNavExpanded: false,

      isAdHidden: true,
      isAdClosed: true,

      scrollTops: {},

      cardLocales: cardLocales,
      cardLocaleNames: cardLocaleNames,
    }
  },
  computed: {
    isUpdatedVersion() {
      return this.version == this.remoteVersion
    },
    hasLocalInfo() {
      return this.localMatches && this.localMatches.length > 0
    },
    versionText(){
      if (this.updateDownloaded) {
        return "Restart"
      }
      return this.version
    },
    versionTooltip() {
      if (this.isUpdatedVersion) { 
        return "Updated"
      } else if (this.updateDownloaded) {
        return "Update on next start" 
      } else if (this.updateProcess > 0) {
        return `Downloading... ${this.updateProcess}%`
      } else if (this.remoteVersion) {
        return `Latest: ${this.remoteVersion}`
      }
      return this.$t('str.loading') 
    },
    lorNewsURL() {
      return `https://playruneterra.com/${this.locale.replace('_', '-')}/news`
    }
  },
  mounted() {
    console.log("Page Home Mounted")
    console.log("Node Environment:", process.env.NODE_ENV)
    console.log("$store.state.locale", this.locale)

    console.log("Is Electron:", this.IS_ELECTRON)

    // Advertisements
    // setTimeout(() => {
    //   this.showAds()
    // }, 15 * 60 * 1000);
    
    // console.log(this.user)

    this.processWindowLocation()
    this.initEventBusses()

    try {

      // var test = 'Hello'
      
      this.requestStatusInfo()

      if (!this.IS_ELECTRON) {
        let myStorage = window.localStorage;
        let locale = myStorage.getItem('ui-locale')
        let cardLocale = myStorage.getItem('card-locale')
        if (locale && this.$i18n.availableLocales.includes(locale)) {
          this.$i18n.locale = locale
          console.log("Change ui locale to", locale)
        }
        if (cardLocale && this.cardLocales.includes(cardLocale)) {
          this.changeLocale(cardLocale)
          console.log("Change card locale to", cardLocale)
        }
        return
      }
      
      this.handleGameEnd()
      this.requestVersionData()
      this.initStore()
      this.initChangeLocale()
      this.initDeckPaste()
      
    } catch (error) {
      console.log(error)
    }
    
    
  },
  methods: {

    ...mapActions([
      'changeLocale'
    ]),

    ...mapActions('deckLibData', ['deckLibPaste']),

    initEventBusses() {
      this.$emitter.on('showDeck', (e) => 
      {
        this.showDeck(e)
      }) // deckCode
      this.$emitter.on('showDeckDetail', (e) => 
      {
        this.showDeckDetail(e)
      }) // deckCode
    },

    processWindowLocation() {
      let search = window.location.search
      var params = new URLSearchParams(search)
      if (params.has('code')) {
        this.showDeckDetail(params.get('code'))
      } else if (window.location.search.includes('/meta')) {
        this.setCurrentPage(PANELS.meta)
      } else if (window.location.search.includes('/search')) {
        this.setCurrentPage(PANELS.search)
      }
    },

    showDeckDetail(code) {
      this.pageDeckCode = code
      this.setCurrentPage(PANELS.deckcode)
      this.hideDeck()
    },

    toggleBookshelf() {
      // this.$refs.bookshelfContent.classList.toggle('hide')
      this.isOpenBookshelf = !this.isOpenBookshelf
    },

    handleContentScroll(event) {
      this.shrinkLeftNav()

      let tar = event.target

      let id = tar.toString()
      let oldSt = null
      if (this.scrollTops && this.scrollTops[id] && this.scrollTops[id].scrollTop) {
        oldSt = this.scrollTops[id].scrollTop 
      }

      const speedThresh = 25;
      const heightThresh = 180;
      
      let st = tar.scrollTop
      if (oldSt && st - oldSt > speedThresh && st > heightThresh) {
        // Scrolling down
        tar.classList.add('scrollDown')
        tar.classList.remove('scrollUp')
      } else if (oldSt && oldSt - st > speedThresh) {
        // Scrolling Up
        tar.classList.add('scrollUp')
        tar.classList.remove('scrollDown')
      }
      this.scrollTops[id] = {scrollTop: st}
      
    },

    showAds() { this.isAdHidden = false },

    hideAds() { this.isAdHidden = true },

    openAds() { this.isAdClosed = false },

    closeAds() {
      this.isAdClosed = true
      this.hideAds()
    },

    expandLeftNav() { this.leftNavExpanded = true },

    shrinkLeftNav() { this.leftNavExpanded = false },

    initStore() {
      window.ipcRenderer.send('request-store', 'ui-locale')

      window.ipcRenderer.on('reply-store', (event, key, val) => {        
        if (key == 'ui-locale' && val) {
          this.$i18n.locale = val
          console.log("Change locale to", val)
        }
      })
    },

    initDeckPaste() {
      window.ipcRenderer.on('handle-clipboard-deck', (event, deckCode) => {
        console.log("handle-clipboard-deck")

        this.clipboardDeck = deckCode
      })
    },

    processPaste() {
      this.deckLibPaste(this.clipboardDeck)
      this.setCurrentPage(PANELS.decklib)
      this.clipboardDeck = null
      // this.$nextTick(() => {
      //   let lib = this.$refs.deckLib
      //   if (lib) {
      //     console.log("handled-paste")
      //     lib.processPaste(this.clipboardDeck)
      //     this.clipboardDeck = null
      //   }
      // })
    },

    // Change Locale
    initChangeLocale() {

      window.ipcRenderer.on('to-change-locale', (event, newLocale) => {
        this.$i18n.locale = newLocale
        console.log("Changing locale to", newLocale)
      })
    },

    

    handleProfileClick() {
      if (!this.hasLocalInfo || (this.currentPage == PANELS.my && this.localPlayerInfo.server != 'sea')) {
        this.requestLocalHistory()
      }
      this.setCurrentPage(PANELS.my)
    },

    // Page Switch
    setCurrentPage(page) {

      var pagekeys = Object.keys(PANELS)
      var label = "From [" + pagekeys[this.currentPage] + "] to [" + pagekeys[page] +"]"

      this.sendUserEvent({
        category: "Main Window",
        action: "Change Tab",
        label: label,
        value: null,
      })
      this.currentPage = page
    },
    searchPlayer(data) {
      
      this.sendUserEvent({
        category: "Main Window Search",
        action: "Leaderboard Search",
        label: data.region + ": " + data.name + "#" + data.tag,
        value: null,
      })

      console.log("Search Player", data)

      if (data.tag) {
        // Only player with tag can be clicked 
        this.setCurrentPage(PANELS.search)
        this.$nextTick(() => {
          // Wait until the panel search mounts
          // console.log(this.$refs)
          this.$refs.panelSearch.searchPlayer(data)
        })
      }
    },

    clearInfo() {
      this.playerName = ""
      this.playerTag = ""
      this.playerRank = null
      this.playerLP = null
      this.playerRegion = null
      this.matches = []
    },
    openURL(url) {
      if (window.openExternal) {
        window.openExternal(url)
      } else {
        window.open(url);
      }
    },
    installDownloadedUpdate() {
      if (this.updateDownloaded) {
        console.log("Trigger Intall Update")
        window.ipcRenderer.send("install-update")
      } else {
        console.log("Download not finished")
      }
    },
    handleGameEnd() {
      window.ipcRenderer.on('game-end-handle', (event) => {
        console.log("Game Ended: Requesting local history")
        this.requestLocalHistory()
      })
    },
    requestVersionData() {

      console.log("Request Version Data")
      window.ipcRenderer.on('app-version', (event, arg) => {
        console.log("Current Version is:", arg)
        // window.appVersion = arg
        this.version = arg
      })

      window.ipcRenderer.on('checking-for-update', (event) => {
        console.log("Checking For Update")
        this.updateDownloaded = false // Reset Update downloaded
      })

      window.ipcRenderer.on('update-available', (event, info) => {
        // console.log(info)
        // window.appVersionLatest = info.version
        
        console.log("Latest Version is:", info.version)
        this.remoteVersion = info.version
      })

      window.ipcRenderer.on('update-not-available', (event, arg) => {
        console.log("Version is Latest")
        this.remoteVersion = this.version
      })

      window.ipcRenderer.on('download-process', (event, arg) => {
        console.log(arg)
        if (Math.floor(arg.percent) < 100)
          this.updateProcess = Math.floor(arg.percent)
      })

      window.ipcRenderer.on('update-downloaded', (event, arg) => {
        console.log(arg)
        console.log("Update Downloaded!")
        this.updateDownloaded = true
      })

      window.ipcRenderer.send("check-update")
      
    },
    requestStatusInfo() {
      // Keeps requesting status

      if (!this.IS_ELECTRON) {
        return
      }
      
      // DevLocal
      // if (process.env.NODE_ENV == "development") {
      //   console.log("Request Status Data")
      //   const testRegion = 'sea'
      //   // const testRegion = 'americas'
      //   const testStatus = `{"language": "zh-TW", "lorRunning": true, "playerId": "FlyingFish#1111","port": "21337","server": "${testRegion}"}`
      //   this.processStatusInfo(JSON.parse(testStatus))
      //   return
      // } 

      lastStatusRequestTime = Date.now()
      axios.get(`${this.apiBase}/status`)
        .then((response) => {
          this.processStatusInfo(response.data)
          var elapsedTime = Date.now() - lastStatusRequestTime // ms
          if (requestStatusWaitTime > elapsedTime) {
            setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime); 
          } else {
            setTimeout(this.requestStatusInfo, 100);
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else { 
            console.log('error', e)
            var elapsedTime = Date.now() - lastStatusRequestTime // ms
            if (elapsedTime > requestStatusWaitTime) {
              setTimeout(this.requestStatusInfo, 100)
            } else {
              setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime);
            }
          }
        })
    },
    initAnalytics(uid) {
      if (window.ipcRenderer) { window.ipcRenderer.send('user-init', uid) }
    },
    processStatusInfo(data) {
      var updateLocalPlayer = false
      if (this.localPlayerInfo.playerId != data.playerId) {
        // there is a change in player ID
        updateLocalPlayer = true

        if (data.playerId) {
          try {
            this.initAnalytics(data.playerId)
            // window.ipcRenderer.send('user-init', data.playerId)
          } catch (error) {
            console.log(error)
          }
        }
      }

      if (data.playerId != "") {

        this.localPlayerInfo.playerId = data.playerId
        var nameid = data.playerId.split('#')
        var oldName = this.localPlayerInfo.name
        var oldTag = this.localPlayerInfo.tag
        
        this.localPlayerInfo.name = nameid[0]
        this.localPlayerInfo.tag = nameid[1]

        if (this.localMatches.length <= 0) {
          // if the matches are still empty
          // updateLocalPlayer = true
        }

      } else {
        this.localPlayerInfo.playerId = null
        this.localPlayerInfo.name = null
        this.localPlayerInfo.tag = null

        this.localMatches = []
      }

      this.localPlayerInfo.server = data.server
      this.localPlayerInfo.language = data.language

      if (updateLocalPlayer) {
        this.requestLocalHistory()
      }
      
      if (data.language) {
        var newLocale = data.language.replace('-', '_').toLowerCase()
        if (this.locale != newLocale) {
          console.log("Switch Locale", this.locale, newLocale)
          this.changeLocale(newLocale)
        }
      }
      // console.log(this.locale)

      this.lorRunning = data.lorRunning
      this.localApiEnabled = data.isLocalApiEnable
    },
    requestLocalHistory() {

      console.log("Request Local History")

      // DevLocal
      // if (process.env.NODE_ENV == "development") {

      //   // const testData = require('../../assets/data/testLocalHistoryData')
      //   const testData = require('../../assets/data/testLocalData')['flyingfish#0000']

      //   // this.playerName = "FlyingFish"
      //   // this.playerRegion = "americas"
      //   // this.processSearchHistory(testData)

      //   // pass
      //   // this.processLocalHistory(testData['flyingfish#0000'])
      //   this.localHistoryLoading = true
      //   setTimeout(() => {
      //     this.localHistoryLoading = false
      //     Math.random() > 0.5 ? this.processLocalHistory(testData) : this.processLocalHistory([])
      //   }, 1000)
        

      //   return
      // }

      if (this.localHistoryLoading) {
        // Don't do anything if there is already a local search request
        return
      }

      // Now ready for a new request
      //Check if there are any previous pending requests
      if (typeof localCancleToken != typeof undefined) {
        localCancleToken.cancel("Operation canceled due to new request.")
      }
      
      //Save the cancel token for the current request
      localCancleToken = axios.CancelToken.source()
      
      var server = this.localPlayerInfo.server
      var name = this.localPlayerInfo.name
      var tag = this.localPlayerInfo.tag

      if (!(server && name && tag)) {
        // Checks to see if there is all the information
        // Don't do anything if not enough data
        return
      }

      let apiLink;
      if (server === 'sea') {
        apiLink = `${this.apiBase}/local`
      } else {
        apiLink = `${this.API_WEB}/search/${server}/${name}/${tag}`
      }

      console.log("Request Local History", apiLink)
      this.localHistoryLoading = true

      this.sendUserEvent({
        category: "Main Window Requests",
        action: "Request Local History",
        label: "URL: " + apiLink,
        value: null,
      })

      const requestLocalHistoryStartTime = Date.now()

      axios.get(apiLink,
          { cancelToken: localCancleToken.token }) // Pass the cancel token
        .then((response) => {
          this.localHistoryLoading = false

          if (response.data == "Error") {
            console.log("Local History Search Error")
          } else {

            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Got Local History Result [Success]",
              label: "URL: " + apiLink,
              value: Date.now() - requestLocalHistoryStartTime,
            })

            if (server === 'sea') {
              let key = (name + '#' + tag).toLowerCase()
              // console.log('Current key', key)
              this.processLocalHistory(response.data[key])
            } else {
              this.processLocalHistory(response.data)
            }
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else {
            console.log('error', e)
            this.localHistoryLoading = false
            this.sendUserEvent({
              category: "Main Window Requests",
              action: "Got Local History Result [Fail]",
              label: "URL: " + apiLink,
              value: Date.now() - requestLocalHistoryStartTime,
            })
          }
          
        })
    },
    showDeck(deck) {
      if (this.deckCode == deck && this.isShowDeck == true) {
        this.isShowDeck = false
      } else {
        this.deckCode = deck
        this.isShowDeck = true
      }
      this.sendUserEvent({
        category: "Main Window Deck",
        action: this.isShowDeck ? "Show Deck" : "Hide Deck",
        label: deck,
        value: null,
      })
      
    },
    hideDeck() {

      this.sendUserEvent({
        category: "Main Window Deck",
        action: "Hide Deck (Collapse Button)",
        label: null,
        value: null,
      })

      this.isShowDeck = false
    },
    processHistory(data, playerName, playerServer) {
      console.log("Process History!", playerName, playerServer)
      // console.log(data)

      var matchInfo = {
        matches: [],
        rank: null,
        lp: null
      }

      if (!data) return matchInfo

      if (playerServer == 'sea') {
        // sea players only have local data
        for (let match of data) {
          let opponentName, opponentRank, opponentLp, opponentTag, opponentDeck, 
            deck, rounds, win, time, order;

          matchInfo.rank = match.playerRank // Currently no value
          matchInfo.lp = match.playerLp // Currently no value

          opponentName = match.opponentName
          opponentTag = null // Cannot get
          opponentRank = match.opponentRank // Currently no value
          opponentLp = match.opponentLp // Currently no value
          opponentDeck = match.deck_tracker.opGraveyardCode
          deck = match.deck_tracker.deckCode
          rounds = null // Cannot get
          win = match.localPlayerWon
          time = match.startTime
          order = null // Cannot get

          let badges = [] // Currently no value

          let details = {
            openHand: match.deck_tracker.openHand,
            replacedHand: match.deck_tracker.replacedHand,
            timeline: match.deck_tracker.timeline,
            startTime: match.startTime,
            endTime: match.endTime,
          }
          
          matchInfo.matches.push({
            opponentName: opponentName,
            deck: deck,
            region: regionShort[this.localPlayerInfo.server],
            opponentDeck: opponentDeck,
            opponentRank: opponentRank,
            opponentLp: opponentLp,
            opponentTag: opponentTag,
            rounds: rounds,
            win: win,
            time: time,
            badges: badges,
            details: details,
          })
        }
      } else {
        // Processing for normal Data
        for (var key in data) {

          var match = data[key]
          if (!match) continue // Skip if null history

          var isFirstPlayer = match.player_info[0].name.toLowerCase() == playerName.toLowerCase()
          var player, playerGame, opponent, opponentGame
          var info = match.info
          var details = null
          
          if (match.local && match.local.deck_tracker) {
            details = {
              openHand: match.local.deck_tracker.openHand,
              replacedHand: match.local.deck_tracker.replacedHand,
              timeline: match.local.deck_tracker.timeline,
              startTime: match.local.startTime,
              endTime: match.local.endTime,
            }
          }

          var opponentName, opponentRank, opponentLp, opponentTag, opponentDeck, 
            deck, rounds, win, time, order;
          
          if (isFirstPlayer) {
            playerGame = info.players[0]
            opponentGame = info.players[1]

            player = match.player_info[0]
            opponent = match.player_info[1]
          } else {
            playerGame = info.players[1]
            opponentGame = info.players[0]

            player = match.player_info[1]
            opponent = match.player_info[0]
          }

          if (!playerGame || !opponentGame || !player || !opponent) continue;

          opponentName = opponent.name
          
          if (opponent.rank !== "") {
            opponentRank = opponent.rank + 1 // rank starts from 0
          } else {
            opponentRank = "" // ranks can be empty
          }
          
          opponentLp = opponent.lp
          opponentTag = opponent.tag

          if (!matchInfo.rank && player.rank !== "") {
            matchInfo.rank = player.rank + 1 // player.rank starts from 0
          }
          
          if (!matchInfo.lp) matchInfo.lp = player.lp
          
          deck = playerGame.deck_code
          opponentDeck = opponentGame.deck_code
          order = playerGame.order_of_play
          win = playerGame.game_outcome == "win"
          rounds = info.total_turn_count
          var badges = []
          if (info.game_mode) badges.push(info.game_mode.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))
          if (info.game_type) badges.push(info.game_type.replace(/([A-Z])/g, ' $1').trim().replace("Lobby", ""))

          time = info.game_start_time_utc

          matchInfo.matches.push({
            opponentName: opponentName,
            deck: deck,
            region: regionShort[playerServer],
            opponentDeck: opponentDeck,
            opponentRank: opponentRank,
            opponentLp: opponentLp,
            opponentTag: opponentTag,
            rounds: rounds,
            win: win,
            time: time,
            badges: badges,
            details: details,
          })
        }

      }

      return matchInfo
    },
    processLocalHistory(data) {
      var info = this.processHistory(data, this.localPlayerInfo.name, this.localPlayerInfo.server)
      this.localMatches = info.matches
      this.localPlayerInfo.rank = info.rank
      this.localPlayerInfo.lp = info.lp
    },
  },

}

</script>