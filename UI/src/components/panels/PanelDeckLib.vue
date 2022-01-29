<template>
  <div class="decklib">
    <modal-warning ref="warningModal"></modal-warning>
    <div class="title">{{ $t("decklib.title") }}</div>
    <div class="btn-container">
      <!-- <button class="btn btn-add">
        <span><i class="fas fa-plus"></i></span>
      </button> -->
      <div class="input-bar-container">
        <input spellcheck="false" autocomplete="off" class="search-bar" @paste="onPaste" v-model="codeText" :placeholder="$t('decklib.placeholder')" />
        <div class="icon inside left">
          <span><i class="fas fa-paste"></i></span>
        </div>
      </div>
      <div class="error-message">
        {{ error }}
      </div>
    </div>
    <div class="decks-container gap-4">
      <div class="deck-block p-2.5" @click="showDeck($event, deck.code)" v-for="(deck, id) in decks" :key="id">
        <div class="decklib-deck-title text-left py-1 px-2" :title="deck.title">
          {{ deck.title }} <span v-if="deck.date" class="block text-xs font-light text-gray-200">{{ format(new Date(deck.date), "HH:mm | yyyy-MM-dd") }}</span>
        </div>
        <div @click.stop="onClickDelete(id)" class="btn-delete btn">
          <span><i class="fas fa-trash"></i></span>
        </div>
        <div class="version tooltip">
          <span class="tooltiptext top pointer-events-none max-w-full overflow-x-hidden overflow-ellipsis">
            {{ deck.code }}
          </span>
          <deck-preview :click-to-show="false" :deck="deck.code"> </deck-preview>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const IS_ELECTRON = window.ipcRenderer !== undefined
import "../../assets/scss/decklib.scss"
import DeckPreview from "../deck/DeckPreview.vue"

import { showDeckMixin } from "../mixins"


import ModalWarning from "../modals/ModalWarning.vue"
import { format, subDays } from "date-fns"
import { mapActions, mapState } from 'pinia'

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
  emits: ["pasted"],
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
      this.$refs.warningModal.showPanel(
        [
          () => {
            console.log("Confirm Delete")
            this.handleDelete(id)
          },
          () => {
            console.log("Nothing happens")
          },
        ],
        `${this.$t("str.delete")} ${this.decks[id].title}`
      )
    },
  },
}
</script>
