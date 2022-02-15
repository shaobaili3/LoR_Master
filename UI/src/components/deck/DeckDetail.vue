<template>
  <div
    class="w-full flex-col"
    :class="{
      'flex h-full': fixedHeight,
      block: !fixedHeight,
    }"
  >
    <div
      class="w-full bg-gray-900 px-1 text-white"
      :class="{ 'flex-1 overflow-y-scroll': fixedHeight }"
      v-if="cards.length > 0"
    >
      <card-preview
        v-for="card in cards"
        :key="card.name + card.count"
        :name="card.name"
        :cost="card.cost"
        :count="hideNum ? null : card.count"
        :code="card.code"
        :type="card.type"
        :supertype="card.supertype"
        :set="card.set"
        :typeRef="card.typeRef"
        @mouseenter="onCardMouseEnter(card)"
        @mouseleave="onCardMouseLeave(card)"
        >{{ card.name }}</card-preview
      >
    </div>
    <!-- Action buttons -->
    <div
      class="flex w-full items-center justify-end whitespace-nowrap bg-gray-900 p-2 text-sm text-white 2xs:text-base"
      v-if="showCopy && this.baseDeck && this.cards.length > 0"
    >
      <!-- Detail -->
      <div
        class="ml-2 cursor-pointer text-gold-300"
        v-if="showURL"
        @click="openURL(deckDetailLink)"
      >
        <span class="fas fa-analytics pr-1"></span>{{ $t("str.detail") }}
      </div>
      <div class="w-0 flex-1"></div>
      <!-- Save -->
      <div class="ml-2 cursor-pointer" v-if="showAdd" @click="addToDeckLib">
        <span class="fa-star pr-1" :class="{ fal: this.saved, fas: !this.saved }"></span
        >{{ this.saved ? this.$t("decklib.saved") : this.$t("decklib.save") }}
      </div>

      <!-- Copt -->
      <div class="tooltip ml-2 cursor-pointer" @click="copyDeckcode">
        <span
          class="fa-copy pr-1"
          :class="{ 'fa-exclamation-triangle': !isFull, fal: this.copied, fas: !this.copied }"
        ></span
        >{{ this.copied ? this.$t("str.copied") : this.$t("str.copy") }}
        <div class="tooltiptext top-end" v-if="!isFull">
          {{ $t("tooltips.incompleteDeck") }}
        </div>
      </div>
    </div>

    <div class="py-4 text-center text-xs italic text-gray-200" v-if="!cards || cards.length == 0">
      {{ $t("str.nothing") }}
    </div>
  </div>
</template>

<script>
import DeckEncoder from "../../modules/runeterra/DeckEncoder"
import CardPreview from "./CardPreview.vue"

import { useDeckLibStore } from "../../store/StoreDeckLib"
import { mapActions } from "pinia"

import { copyToClipboard } from "../../pages/home/Home.vue"

const fadeTimeout = 1250

export default {
  components: {
    CardPreview,
  },
  mounted() {},
  data() {
    return {
      copied: false,
      saved: false,
    }
  },
  props: {
    deck: String,
    baseDeck: String,
    showCopy: {
      type: Boolean,
      default: true,
    },
    showURL: {
      type: Boolean,
      default: false,
    },
    showAdd: {
      type: Boolean,
      default: false,
    },
    fixedHeight: {
      type: Boolean,
      default: false,
    },
    extra: {
      type: Array,
      default: () => [],
    },
    hideNum: {
      type: Boolean,
      default: false,
    },
    fullHeight: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    // locale(newLoacle, oldLocale) {
    //     this.loadSetsJson(newLoacle)
    // }
  },
  computed: {
    deckDetailLink() {
      return "/code?code=" + this.baseDeck
      // return "https://lor.mobalytics.gg/decks/code/" + this.baseDeck
    },
    cards() {
      var cards = []

      if (this.sets == null) return cards

      var deck = null
      if (this.deck)
        try {
          deck = DeckEncoder.decode(this.deck)
        } catch (err) {
          console.log(err)
          // return cards
        }

      var baseDeck = null
      if (this.baseDeck)
        try {
          baseDeck = DeckEncoder.decode(this.baseDeck)
        } catch (err) {
          console.log(err)
          // return cards
        }

      // Append extra played cards to baseDeck
      if (baseDeck && this.extra) {
        baseDeck = baseDeck.concat(this.extra)
      }

      if (baseDeck) {
        // make sure cards not in current Deck are shown
        // console.log("baseDeck", baseDeck)
        // console.log("extra", this.extra)
        for (var j in baseDeck) {
          // Loop through base deck
          var cardCode = baseDeck[j].code
          // Get full information from the sets collection
          var card = this.sets.find((card) => card.cardCode == cardCode)
          var cardCount = baseDeck[j].count
          var baseCount = baseDeck[j].count

          // Append extra played cards to playedDeck as well?
          // deck = deck.concat(this.extra)

          if (deck) {
            // make sure currentDeck exist

            // Finding the same card in current deck
            var currentCard = deck.find((card) => card.code == cardCode)

            // Get the current card copy count
            if (currentCard) {
              cardCount = currentCard.count
            } else {
              cardCount = 0
            }
          }

          if (card) {
            var typeRef = ""
            if (card.supertype != "" || card.rarityRef == "Champion") {
              typeRef = "Champion"
            } else if (card.spellSpeedRef != "") {
              typeRef = "Spell"
            } else if (card.keywordRefs && card.keywordRefs.includes("LandmarkVisualOnly")) {
              typeRef = "Landmark"
            } else {
              typeRef = "Unit"
            }

            cards.push({
              code: cardCode,
              name: card.name,
              count: cardCount,
              baseCount: baseCount,
              cost: card.cost,
              type: card.type,
              typeRef: typeRef,
              supertype: card.supertype,
              set: card.set,
            })
          } else if (cardCode && cardCount) {
            cards.push({
              code: cardCode,
              // name: `?`.repeat(Math.floor( 2 + Math.random() * 4)) + `${Math.random() > 0.35 ? ' ': ''}` + `?`.repeat(Math.floor( 2 + Math.random() * 4)),
              name: "???",
              count: cardCount,
              baseCount: baseCount,
              cost: "?",
              type: "Unknown",
              typeRef: "Unknown",
              supertype: null,
              set: "1",
            })
          }
        }
      }
      // console.log(cards)
      return cards.sort(function (a, b) {
        if (a.type === "Unknown") {
          return 1
        }
        if (a.supertype == b.supertype) {
          if (a.type == b.type) {
            if (a.cost == b.cost) {
              return a.code > b.code ? 1 : -1
            }
            return a.cost > b.cost ? 1 : -1
          }
          return a.type > b.type ? 1 : -1
        }
        return a.supertype < b.supertype ? 1 : -1
      })
    },
    isFull() {
      return (
        this.cards.reduce((prev, card) => {
          return prev + card.baseCount
        }, 0) == 40
      )
    },
    currentCount() {
      if (!this.cards) return 0
      return this.cards.reduce((prev, card) => {
        return prev + card.count
      }, 0)
    },
  },
  emits: ["showDetail", "card"],
  methods: {
    ...mapActions(useDeckLibStore, ["deckLibPaste"]),
    onCardMouseEnter(card) {
      if (card) {
        card.all = this.currentCount
        this.$emit("card", card)
      }
    },
    onCardMouseLeave(card) {
      this.$emit("card", null)
    },
    addToDeckLib() {
      if (this.deckLibPaste(this.baseDeck)) {
        this.saved = true
        setTimeout(() => {
          this.saved = false
        }, fadeTimeout)
      }
    },
    copyDeckcode() {
      copyToClipboard(this.baseDeck)
      this.copied = true
      setTimeout(() => {
        this.copied = false
      }, fadeTimeout)
    },
    openURL(url) {
      this.$emitter.emit("showDeckDetail", this.baseDeck)
      this.$router.push(url)
    },
  },
}
</script>

<style></style>
