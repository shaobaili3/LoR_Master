<template>
  <div class="flex h-full justify-center">
    <div class="w-0 max-w-xl flex-1 lg:max-w-4xl">
      <div class="decklib flex h-full flex-col px-2 sm:px-0">
        <modal-warning ref="warningModal"></modal-warning>
        <div class="title pb-4 text-left text-3xl">
          {{ $t("decklib.title") }}
        </div>
        <div class="btn-container">
          <div class="input-bar-container">
            <input
              spellcheck="false"
              autocomplete="off"
              class="h-12 w-full rounded-3xl bg-gray-800 pl-12 pr-5 placeholder-gray-300 outline-none transition-colors focus:bg-gray-700"
              @paste="onPaste"
              v-model="codeText"
              :placeholder="$t('decklib.placeholder')"
            />
            <!-- <div class="icon inside left">
              <span><i class="fas fa-paste"></i></span>
            </div> -->
            <i class="fas fa-paste pointer-events-none absolute left-5 top-4 text-gray-200"></i>
          </div>
          <div class="error-message">
            {{ error }}
          </div>
        </div>
        <div v-if="!decks || decks.length == 0">
          <span class="py-4 text-sm italic text-gray-200">{{ $t("str.nothing") }}</span>
          <i18n-t keypath="decklib.noDecks" tag="div" class="py-4 text-white">
            <i class="fas fa-star px-1"></i>
          </i18n-t>
        </div>
        <div class="flex h-0 flex-1 overflow-y-auto px-2">
          <!-- Decks -->
          <div class="decks-container h-fit gap-4">
            <div
              class="deck-block cursor-pointer bg-gray-700 p-2.5 transition-colors hover:bg-gray-800"
              @click="showDeck($event, deck.code)"
              v-for="(deck, id) in decks"
              :key="id"
            >
              <div class="decklib-deck-title px-2 py-1 text-left" :title="deck.title">
                {{ deck.title }}
                <span v-if="deck.date" class="block text-xs font-light text-gray-200">{{
                  format(new Date(deck.date), "HH:mm | yyyy-MM-dd")
                }}</span>
              </div>
              <div @click.stop="onClickDelete(id)" class="btn-delete btn">
                <span><i class="fas fa-trash"></i></span>
              </div>
              <div class="version">
                <deck-preview class="gap-1 py-2 text-base" :click-to-show="false" :deck="deck.code">
                </deck-preview>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "../../assets/scss/decklib.scss"
import DeckPreview from "../deck/DeckPreview.vue"

import { showDeckMixin } from "../mixins"

import ModalWarning from "../modals/ModalWarning.vue"
import { format, subDays } from "date-fns"
import { mapActions, mapState } from "pinia"

import { useDeckLibStore } from "../../store/StoreDeckLib"

export default {
  components: { DeckPreview, ModalWarning },
  mixins: [showDeckMixin],
  data() {
    return {
      codeText: "",
    }
  },
  computed: {
    ...mapState(useDeckLibStore, ["decks", "loaded", "error", "pasteBuffer"]),
  },
  mounted() {
    this.initStore()
    if (this.pasteBuffer) {
      this.processPaste(this.pasteBuffer)
      this.pasteBuffer = null
    }
  },
  methods: {
    ...mapActions(useDeckLibStore, ["initStore", "processPaste", "handleDelete"]),
    format: format,
    subDays: subDays,
    showDeck(event, deck) {
      if (!event.target.className.includes("btn-delete")) {
        // Not deleting the deck
        this.$emitter.emit("showDeck", deck)
      }
    },
    onPaste(event) {
      event.preventDefault()
      let pasteContent = (event.clipboardData || window.clipboardData).getData("text")
      this.processPaste(pasteContent)
    },
    onClickDelete(id) {
      // this.$refs.warningModal.showPanel(
      //   [
      //     () => {
      //       console.log("Confirm Delete")
      //       this.handleDelete(id)
      //     },
      //     () => {
      //       console.log("Nothing happens")
      //     },
      //   ],
      //   `${this.$t("str.delete")} ${this.decks[id].title}`
      // )
      this.handleDelete(id)
    },
  },
}
</script>
