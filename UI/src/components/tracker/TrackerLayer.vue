<template>
  <!-- No longer in use -->
  <div class="decklib">
    <div class="decks-container gap-1.5">
      <div
        class="deck-block p-2.5"
        @click="showDeck($event, id)"
        v-for="(deck, id) in decks"
        :key="id"
      >
        <div class="px-1 text-xs text-gray-200" v-if="deck.date">
          <span
            :class="{
              'text-gold-300': deck.date > new Date() - RecentDeckThresh,
            }"
            >{{ format(new Date(deck.date), "HH:mm") }} </span
          >{{ format(new Date(deck.date), " | yyyy-MM-dd") }}
        </div>
        <div class="decklib-deck-title w-full px-1 text-left">
          {{ deck.title }}
        </div>
        <deck-preview :deck="deck.code"> </deck-preview>
      </div>
    </div>

    <div class="layerpanel second" :class="{ expanded: showDeckIndex !== null }">
      <button class="btn btn-back" @click="onBackSecond">
        <span><i class="fas fa-caret-down"></i></span>
      </button>
      <deck-detail
        v-if="showDeckIndex !== null"
        :baseDeck="decks[showDeckIndex].code"
        :showCopy="true"
      ></deck-detail>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"
import "../../assets/scss/decklib.scss"
import DeckDetail from "../deck/DeckDetail.vue"

import { format, subDays } from "date-fns"

import { showDeckMixin } from "../mixins"

const RecentDeckThresh = 5 * 60 * 1000 // 5 minutes, for highlight recent imported decks

export default {
  components: { DeckPreview, DeckDetail },
  mixins: [showDeckMixin],
  emits: ["back"],
  props: {
    pinDeckId: Number,
  },
  created() {
    this.RecentDeckThresh = RecentDeckThresh
  },
  data() {
    return {
      decks: [],
      showDeckIndex: null,
    }
  },
  computed() {},
  mounted() {
    console.log(this.pinDeckId)
    this.initStore()
  },
  methods: {
    format: format,
    subDays: subDays,
    initStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send("request-store", "deck-lib")

        window.ipcRenderer.on("reply-store-deck-lib", (_event, val) => {
          if (val) {
            console.log("Got Deck Lib Store")
            this.decks = JSON.parse(val)
          }
        })
      } else {
        // Sample data
        this.decks = [
          {
            title: "Fizz Poppy",
            date: new Date(),
            code: "CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ",
          },
          {
            title: "Draven Sion",
            date: new Date() - 60000,
            code: "CECACAIDCQAQIBAQAMCQGAIJBUCACBBGE4WTIAYBAEBS4AIBAQAQCAYDB4CACAQDBEAQGBASAICQGBAGAMAQGCZDGM",
          },
          {
            title: "Thresh Aurelion Sol",
            date: new Date() - 600000,
            code: "CQBQCBIKV4AQEAIFFA2AKAYJC5KFMXDAAQAQCBIZAECASDIBAUCQ6AQDBFEVOAYBAQCTQAQDBERTGAYBAUAQ6HI",
          },
          {
            title: "Bandle Nox",
            date: new Date() - 6000000,
            code: "CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ",
          },
        ]
      }

      if (this.pinDeckId != null) {
        this.showDeckIndex = this.pinDeckId
      }
    },
    onBackSecond() {
      this.showDeckIndex = null
      this.$emit("showDeck", null, null)
    },
    showDeck(event, id) {
      if (!event.target.className.includes("trash")) {
        // Not deleting the deck
        // this.$emit('showDeck', deck)
        this.showDeckIndex = id
        this.$emit("showDeck", this.decks[id].code, id)
      }
    },
  },
}
</script>
