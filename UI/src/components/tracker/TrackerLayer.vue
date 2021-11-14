<template>
  <div class="decklib">
    <div class="decks-container gap-1.5 xxs:gap-2">
      <div class="deck-block p-1 xxs:p-2 xs:p-2.5 " @click="showDeck($event, id)" v-for="(deck, id) in decks" :key="id">
        <div class="decklib-deck-title">
          {{deck.title}}
        </div>
        <deck-preview 
          :deck="deck.code">
        </deck-preview>
      </div>
    </div>

    <div class="layerpanel second" :class="{expanded: showDeckIndex !== null}">
      <button class="btn btn-back" @click="onBackSecond">
        <span><i class="fas fa-caret-down"></i></span>
      </button>
      <deck-detail v-if="showDeckIndex !== null" :baseDeck="decks[showDeckIndex].code" :showCopy="true"></deck-detail>
    </div>
  </div>
</template>

<script>
import DeckPreview from '../deck/DeckPreview.vue'
import '../../assets/scss/decklib.scss'
import DeckDetail from '../deck/DeckDetail.vue'

import { showDeckMixin } from '../mixins'

export default {
  components: { DeckPreview, DeckDetail },
  mixins: [showDeckMixin],
  emits: ['back'],
  props: {
    pinDeckId: Number,
  },
  data() {
    return {
      decks: [],
      showDeckIndex: null,
    }
  },
  computed() {
  },
  mounted() {
    console.log(this.pinDeckId)
    this.initStore()
  },
  methods: {
    initStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send('request-store', 'deck-lib')

        window.ipcRenderer.on('reply-store', (event, key, val) => {
          console.log("Got store", key, val)

          if (key == 'deck-lib' && val) {
            // console.log("Deck Lib", val)
            this.decks = JSON.parse(val)
          }
        })
      } else {
        // Sample data
        this.decks = [
          {
            title: "Bandle Nox",
            code: 'CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ'
          },
          {
            title: "Draven Sion",
            code: 'CECACAIDCQAQIBAQAMCQGAIJBUCACBBGE4WTIAYBAEBS4AIBAQAQCAYDB4CACAQDBEAQGBASAICQGBAGAMAQGCZDGM'
          },
          {
            title: "Thresh Asol",
            code: 'CQBQCBIKV4AQEAIFFA2AKAYJC5KFMXDAAQAQCBIZAECASDIBAUCQ6AQDBFEVOAYBAQCTQAQDBERTGAYBAUAQ6HI'
          }, {
            title: "Bandle Nox",
            code: 'CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ'
          },
          {
            title: "Draven Sion",
            code: 'CECACAIDCQAQIBAQAMCQGAIJBUCACBBGE4WTIAYBAEBS4AIBAQAQCAYDB4CACAQDBEAQGBASAICQGBAGAMAQGCZDGM'
          },
          {
            title: "Thresh Asol",
            code: 'CQBQCBIKV4AQEAIFFA2AKAYJC5KFMXDAAQAQCBIZAECASDIBAUCQ6AQDBFEVOAYBAQCTQAQDBERTGAYBAUAQ6HI'
          },
          {
            title: "Bandle Nox",
            code: 'CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ'
          },
          {
            title: "Draven Sion",
            code: 'CECACAIDCQAQIBAQAMCQGAIJBUCACBBGE4WTIAYBAEBS4AIBAQAQCAYDB4CACAQDBEAQGBASAICQGBAGAMAQGCZDGM'
          },
          {
            title: "Thresh Asol",
            code: 'CQBQCBIKV4AQEAIFFA2AKAYJC5KFMXDAAQAQCBIZAECASDIBAUCQ6AQDBFEVOAYBAQCTQAQDBERTGAYBAUAQ6HI'
          }
        ]
      }

      if (this.pinDeckId != null) {
        this.showDeckIndex = this.pinDeckId
      }
    },
    onBackSecond() {
      this.showDeckIndex = null
      this.$emit('showDeck', null, null)
    },
    showDeck(event, id) {
      if (!event.target.className.includes('trash')) {
        // Not deleting the deck
        // this.$emit('showDeck', deck)
        this.showDeckIndex = id
        this.$emit('showDeck', this.decks[id].code, id)
      }
    },
  }
}
</script>