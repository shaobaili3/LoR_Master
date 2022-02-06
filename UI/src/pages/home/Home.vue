<template>
  <div class="left-nav-btn mobile-btn" @click="expandLeftNav">
    <span><i class="fas fa-list"></i></span>
  </div>
  <div class="overflow-y-scroll left-nav no-scrollbar" :class="{ expanded: leftNavExpanded }">
    <div class="left-nav-btn logo no-click" v-if="!IS_ELECTRON" @mouseenter="showAds">
      <picture>
        <source srcset="@/assets/images/logo/logo.webp" type="image/webp" />
        <source srcset="@/assets/images/logo/logo.png" type="image/png" />
        <img class="logo" height="50px" src="@/assets/images/logo/logo.png" alt="" />
      </picture>
    </div>
    <router-link
      :to="{ name: 'profile' }"
      class="left-nav-btn"
      v-if="IS_ELECTRON || IS_DEV"
      :class="{ selected: $route.name == 'profile', disabled: !lorRunning }"
      @click="setCurrentPage(PANELS.my)"
      :disabled="!lorRunning"
    >
      <span><i class="fas fa-user-circle"></i></span>
    </router-link>
    <router-link
      :to="{ name: 'search' }"
      class="left-nav-btn"
      :class="{ selected: $route.name == 'search' }"
      @click="setCurrentPage(PANELS.search)"
    >
      <span><i class="fas fa-search"></i></span>
    </router-link>
    <router-link
      :to="{ name: 'leaderboard' }"
      class="left-nav-btn"
      :class="{ selected: $route.name == 'leaderboard' }"
      @click="setCurrentPage(PANELS.leaderboard)"
    >
      <span><i class="fas fa-trophy"></i></span>
    </router-link>
    <router-link
      :to="{ name: 'decklib' }"
      class="left-nav-btn"
      v-if="IS_ELECTRON || IS_DEV"
      :class="{ selected: $route.name == 'decklib' }"
      @click="setCurrentPage(PANELS.decklib)"
    >
      <span><i class="fas fa-star"></i></span>
    </router-link>
    <router-link
      :to="{ name: 'meta' }"
      class="left-nav-btn"
      :class="{ selected: $route.name == 'meta' }"
      @click="setCurrentPage(PANELS.meta)"
    >
      <span><i class="fas fa-trees"></i></span>
    </router-link>
    <button class="hidden left-nav-btn sm:flex" :class="{ 'text-gold-200 light-gold': isOpenBookshelf }" @click="toggleBookshelf()">
      <span><i class="fas fa-books"></i></span>
    </button>
    <router-link v-if="IS_DEV" :to="{ name: 'test' }" class="left-nav-btn" :class="{ selected: $route.name == 'test' }">
      <span><i class="fas fa-wrench"></i></span>
    </router-link>
    <!-- Divider -->
    <div class="flex-1"></div>
    <router-link
      :to="{ name: 'contact' }"
      class="text-gray-300 left-nav-btn gray"
      :class="{ selected: $route.name == 'contact' }"
      @click="setCurrentPage(PANELS.contact)"
    >
      <span><i class="fas fa-comment-alt-smile"></i></span>
    </router-link>
    <router-link
      :to="{ name: 'settings' }"
      class="text-gray-300 left-nav-btn gray"
      :class="{
        selected: $route.name == 'settings',
        ' mb-14 ': IS_ELECTRON,
        ' mb-5 ': !IS_ELECTRON,
      }"
      @click="setCurrentPage(PANELS.settings)"
    >
      <span><i class="fas fa-cog"></i></span>
    </router-link>
  </div>

  <div
    class="absolute top-0 left-0 z-10 block w-screen h-screen bg-gray-900/50 sm:hidden"
    v-if="leftNavExpanded"
    @click="shrinkLeftNav"
  ></div>

  <div
    class="menu-content hidden sm:grid absolute left-[98px] top-6 bottom-auto z-[120]"
    :class="{ hide: !isOpenBookshelf }"
    @mouseleave="toggleBookshelf()"
  >
    <div class="card" @click="openURL('https://masteringruneterra.com/')">
      <img src="https://masteringruneterra.com/wp-content/uploads/2021/09/MasteringRuneterraWebsiteLogo-300x129.webp" />
    </div>
    <div class="card square" @click="openURL('https://runeterraccg.com/')">
      <img src="https://runeterraccg.com/wp-content/uploads/2020/05/RuneterraCCG.com-Square-Logo.png" />
    </div>

    <div class="card square" @click="openURL('https://www.swimstrim.com/')">
      <img src="https://www.swimstrim.com/packs/media/images/logo-8b7cd382.png" />
    </div>
    <div class="card sqaure" @click="openURL(lorNewsURL)">
      <img src="https://images.contentstack.io/v3/assets/blt0eb2a2986b796d29/blt8ba1ec1b0013e362/5ea53af4ae23d30cd1dfb3e4/lor-logo.png" />
    </div>
    <div class="card square" @click="openURL('https://runeterra.ar/')">
      <img src="https://cdnruneterra.ar/assets/img/logo_ar_black.png" />
    </div>
  </div>

  <base-window-controls v-if="IS_ELECTRON" :title="''" :titleType="'window'"></base-window-controls>

  <base-top-nav v-if="!IS_ELECTRON"></base-top-nav>

  <!-- Ads -->
  <!-- <div v-if="!IS_ELECTRON" class="mt-[-23px] text-center w-auto min-w-0 pl-4 absolute transition-spacing z-10 invisible md:visible" :class="{ 'ml-[-300px]': isAdHidden && isAdClosed, 'ml-20': !(isAdHidden && isAdClosed) }">
    <div class="ad overflow-hidden relative block w-[300px] h-[250px] transition-opacity bg-gray-800 rounded-lg" @mouseleave="hideAds">
      <button class="absolute text-white top-1 right-1" @click="closeAds">
        <i class="p-2 fas fa-times"></i>
      </button>
      <div class="w-full h-full">
        <p class="py-5 text-lg">
          Have you tried our <a class="text-xl cursor-pointer text-gold-400" href="https://lormaster.com" target="_blank"><br />LoR Master Tracker</a> yet?
        </p>
        <a class="text-xl cursor-pointer text-gold-400" href="https://lormaster.com" target="_blank"><img src="../../assets/images/promo/tracker.png" alt="" srcset="" /></a>
      </div>
    </div>
  </div> -->

  <div
    class="block text-center text-white pt-nav sm:pl-20"
    :class="{ 'h-main-electron': IS_ELECTRON, 'h-main-web': !IS_ELECTRON }"
    @click="shrinkLeftNav"
  >
    <div class="h-full" @scroll="handleContentScroll">
      <router-view :key="$route.fullPath"></router-view>
    </div>
  </div>

  <div class="deck-content-container" :class="{ hide: !isShowDeck, fullheight: !IS_ELECTRON }">
    <div class="deck-content-top-bar">
      <button class="collapse-btn" @click="hideDeck">
        <span><i class="fas fa-chevron-right"></i></span>
      </button>
      <deck-regions :deck="deckCode" :fixedWidth="false"></deck-regions>
    </div>
    <div class="deck-content-detail" :fixedHeight="!IS_ELECTRON">
      <deck-detail :baseDeck="deckCode" :fixedHeight="true" :showURL="true" :showAdd="true"></deck-detail>
    </div>
  </div>

  <div class="bg-gray-900/50 z-[5] absolute top-0 left-0 block sm:hidden w-screen h-screen" v-if="isShowDeck" @click="hideDeck"></div>

  <div class="bottom-bar" v-if="IS_ELECTRON">
    <div class="left">
      <div class="app-name url" @click="openURL('https://www.lormaster.com')">{{ $t("appName") }}</div>
      <div v-if="!localApiEnabled && lorRunning && IS_ELECTRON" class="api-warning warning">
        <small><i class="fas fa-exclamation-triangle"></i>{{ $t("str.error.localApiError") }}</small>
      </div>
    </div>
    <div class="right">
      <!-- <div class="version download tooltip" v-if="!isUpdatedVersion" @click="openURL(downloadUrl)">
        <span class="tooltiptext">
          <i class="fas fa-arrow-to-bottom"></i> {{remoteVersion}}
        </span>
        <i class="fas fa-exclamation-triangle"></i> {{version}}</div> -->
      <div class="version tooltip" :class="{ download: updateDownloaded }" @click="installDownloadedUpdate()">
        <span class="tooltiptext top-bottom-right">
          <span v-if="isUpdatedVersion"><i class="fas fa-check"></i></span>{{ versionTooltip }}
        </span>
        <i class="fas" :class="{ 'fa-redo-alt': updateDownloaded }"></i>
        {{ versionText }}
      </div>
    </div>
  </div>

  <div class="fixed z-20 flex flex-col items-start justify-center px-4 py-2 bg-gray-700 rounded-md bottom-16 right-4" v-if="clipboardDeck">
    <i class="absolute w-4 h-4 text-gray-200 cursor-pointer top-4 right-4 fas fa-times" @click="onCloseFastClipboard"></i>
    <div class="text-lg text-white">{{ $t("str.clipboard") }}</div>
    <div class="text-sm text-gray-200">
      {{ $t("decklib.saveTo") }}
    </div>
    <deck-preview :deck="clipboardDeck" @click="processPaste"></deck-preview>
  </div>
</template>

<script>
// Styles

import "../../assets/scss/tooltips.scss"
import "../../assets/scss/home.scss"
import "../../assets/scss/transitions.scss"

import BaseWindowControls from "../../components/base/BaseWindowControls.vue"
import BaseTopNav from "../../components/base/BaseTopNav.vue"

import DeckRegions from "../../components/deck/DeckRegions.vue"
import DeckPreview from "../../components/deck/DeckPreview.vue"
import DeckDetail from "../../components/deck/DeckDetail.vue"

import { useBaseStore } from "../../store/StoreBase"
import { useDeckLibStore } from "../../store/StoreDeckLib"
import { useStatusStore } from "../../store/StoreStatus"
import { mapState, mapActions } from "pinia"

import "../../assets/scss/responsive.scss"

const requestDataWaitTime = 400 //ms
const requestHistoryWaitTime = 100 //ms

const inputNameListLength = 10

// IS_ELECTRON & IS_DEV defined in template.js

import { locales as cardLocales, localeNames as cardLocaleNames } from "../template"

import { REGION_ID, REGION_SHORTS, REGION_NAMES } from "../../components/panels/PanelLeaderboard.vue"

// import ua from 'universal-analytics'

// const portNum = "26531"
// const API_BASE = `http://127.0.0.1:${portNum}`

let cancelToken, localCancleToken
var requestHistoryTimeout, prevHistoryRequest

const regionNames = {
  NA: "americas",
  EU: "europe",
  AS: "asia",
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
  let date = new Date()
  date.setTime(date.getTime() + expDay * 24 * 60 * 60 * 1000 + expHour * 60 * 60 * 1000 + expMin * 60 * 1000)
  const expires = "expires=" + date.toUTCString()
  document.cookie = name + "=" + value + "; " + expires + "; path=/"
}

function getCookie(name) {
  const cname = name + "="
  const decoded = decodeURIComponent(document.cookie) //to be careful
  const arr = decoded.split("; ")
  let res
  arr.forEach((val) => {
    if (val.indexOf(cname) === 0) res = val.substring(name.length)
  })
  return res
}

export default {
  components: {
    BaseWindowControls,
    DeckRegions,
    DeckDetail,
    DeckPreview,
    BaseTopNav,
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
    ...mapState(useStatusStore, ["localApiEnabled", "localPlayerID", "localServer", "lorRunning"]),

    isUpdatedVersion() {
      return this.version == this.remoteVersion
    },
    hasLocalInfo() {
      return this.localMatches && this.localMatches.length > 0
    },
    versionText() {
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
      return this.$t("str.loading")
    },
    lorNewsURL() {
      return `https://playruneterra.com/${this.locale.replace("_", "-")}/news`
    },
  },
  mounted() {
    console.log("Page Home Mounted")
    console.log(`Current Route: ${this.$route.name}, ${window.location.pathname}`)

    if (window.location.search[1] === "/") {
      var decoded = window.location.search
        .slice(1)
        .split("&")
        .map(function (s) {
          return s.replace(/~and~/g, "&")
        })
        .join("?")
      this.$router.replace(window.location.pathname.slice(0, -1) + decoded + window.location.hash)
    } else if (!this.$route.name && window.location.pathname == "/index.html") {
      this.$router.push({ name: "leaderboard" })
    }

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

      const statusStore = useStatusStore()
      statusStore.requestStatusInfo()

      if (!this.IS_ELECTRON) {
        let myStorage = window.localStorage
        let locale = myStorage.getItem("ui-locale")
        let cardLocale = myStorage.getItem("card-locale")
        if (locale && this.$i18n.availableLocales.includes(locale)) {
          if (this.$i18n) this.$i18n.locale = locale
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
    ...mapActions(useBaseStore, ["changeLocale"]),

    ...mapActions(useDeckLibStore, ["deckLibPaste"]),

    onCloseFastClipboard() {
      const copyToClipboard = (str) => {
        const el = document.createElement("textarea") // Create a <textarea> element
        el.value = str // Set its value to the string that you want copied
        el.setAttribute("readonly", "") // Make it readonly to be tamper-proof
        el.style.position = "absolute"
        el.style.left = "-9999px" // Move outside the screen to make it invisible
        document.body.appendChild(el) // Append the <textarea> element to the HTML document
        const selected =
          document.getSelection().rangeCount > 0 // Check if there is any content selected previously
            ? document.getSelection().getRangeAt(0) // Store selection if found
            : false // Mark as false to know no selection existed before
        el.select() // Select the <textarea> content
        document.execCommand("copy") // Copy - only works as a result of a user action (e.g. click events)
        document.body.removeChild(el) // Remove the <textarea> element
        if (selected) {
          // If a selection existed before copying
          document.getSelection().removeAllRanges() // Unselect everything on the HTML document
          document.getSelection().addRange(selected) // Restore the original selection
        }
      }

      copyToClipboard(this.clipboardDeck)
      this.clipboardDeck = null
    },

    initEventBusses() {
      this.$emitter.on("showDeck", (e) => {
        this.showDeck(e)
      }) // deckCode
      this.$emitter.on("showDeckDetail", (e) => {
        this.showDeckDetail(e)
      }) // deckCode
    },

    processWindowLocation() {
      let search = window.location.search
      var params = new URLSearchParams(search)
      if (params.has("code")) {
        this.$router.push({
          name: "code",
          query: { code: params.get("code") },
        })
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

      const speedThresh = 25
      const heightThresh = 180

      let st = tar.scrollTop
      if (oldSt && st - oldSt > speedThresh && st > heightThresh) {
        // Scrolling down
        tar.classList.add("scrollDown")
        tar.classList.remove("scrollUp")
      } else if (oldSt && oldSt - st > speedThresh) {
        // Scrolling Up
        tar.classList.add("scrollUp")
        tar.classList.remove("scrollDown")
      }
      this.scrollTops[id] = { scrollTop: st }
    },

    showAds() {
      this.isAdHidden = false
    },

    hideAds() {
      this.isAdHidden = true
    },

    openAds() {
      this.isAdClosed = false
    },

    closeAds() {
      this.isAdClosed = true
      this.hideAds()
    },

    expandLeftNav() {
      this.leftNavExpanded = true
    },

    shrinkLeftNav() {
      this.leftNavExpanded = false
    },

    initStore() {
      window.ipcRenderer.send("request-store", "ui-locale")

      window.ipcRenderer.on("reply-store", (event, key, val) => {
        if (key == "ui-locale" && val) {
          if (this.$i18n) this.$i18n.locale = val
          console.log("Change locale to", val)
        }
      })
    },

    initDeckPaste() {
      window.ipcRenderer.on("handle-clipboard-deck", (event, deckCode) => {
        console.log("handle-clipboard-deck")

        this.clipboardDeck = deckCode
      })
    },

    processPaste() {
      this.deckLibPaste(this.clipboardDeck)
      this.$router.push({ name: "decklib" })
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
      window.ipcRenderer.on("to-change-locale", (event, newLocale) => {
        if (this.$i18n) this.$i18n.locale = newLocale
        console.log("Changing locale to", newLocale)
      })
    },

    handleProfileClick() {
      // if (!this.hasLocalInfo || (this.currentPage == PANELS.my && this.localPlayerInfo.server != "sea")) {
      //   this.requestLocalHistory()
      // }
      this.setCurrentPage(PANELS.my)
    },

    // Page Switch
    setCurrentPage(page) {
      var pagekeys = Object.keys(PANELS)
      var label = "From [" + pagekeys[this.currentPage] + "] to [" + pagekeys[page] + "]"

      this.sendUserEvent({
        category: "Main Window",
        action: "Change Tab",
        label: label,
        value: null,
      })
      // TODO proper push history
      // this.$router.push("/login")
      // this.currentPage = page
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
        // Only player with tag can be clicked=
        this.$router.push({
          name: "search",
          query: data,
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
        window.open(url)
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
      window.ipcRenderer.on("game-end-handle", (event) => {
        console.log("Game Ended: Requesting local history")
        this.requestLocalHistory()
      })
    },
    requestVersionData() {
      console.log("Request Version Data")
      window.ipcRenderer.on("app-version", (event, arg) => {
        console.log("Current Version is:", arg)
        // window.appVersion = arg
        this.version = arg
      })

      window.ipcRenderer.on("checking-for-update", (event) => {
        console.log("Checking For Update")
        this.updateDownloaded = false // Reset Update downloaded
      })

      window.ipcRenderer.on("update-available", (event, info) => {
        // console.log(info)
        // window.appVersionLatest = info.version

        console.log("Latest Version is:", info.version)
        this.remoteVersion = info.version
      })

      window.ipcRenderer.on("update-not-available", (event, arg) => {
        console.log("Version is Latest")
        this.remoteVersion = this.version
      })

      window.ipcRenderer.on("download-process", (event, arg) => {
        console.log(arg)
        if (Math.floor(arg.percent) < 100) this.updateProcess = Math.floor(arg.percent)
      })

      window.ipcRenderer.on("update-downloaded", (event, arg) => {
        console.log(arg)
        console.log("Update Downloaded!")
        this.updateDownloaded = true
      })

      window.ipcRenderer.send("check-update")
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
  },
}
</script>
