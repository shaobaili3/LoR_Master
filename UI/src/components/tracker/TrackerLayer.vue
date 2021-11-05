<template>
  <div class="decklib">
    <button class="btn btn-back" @click="onBack">
      <span><i class="fas fa-caret-down"></i></span>
    </button>
    <div class="decks-container">
      <div class="deck-block" @click="showDeck($event, id)" v-for="(deck, id) in decks" :key="id">
        <div class="decklib-deck-title">
          {{deck.title}}
        </div>
        <div @click="handleDelete(id)" class="btn-delete btn"><span><i class="fas fa-trash"></i></span></div>
        <deck-preview 
          :deck="deck.code">
        </deck-preview>
      </div>
    </div>

    <div class="layerpanel second" :class="{expanded: showDeckIndex !== null}">
      <button class="btn btn-back" @click="onBackSecond">
        <span><i class="fas fa-caret-down"></i></span>
      </button>
      <deck-detail v-if="showDeckIndex !== null" :baseDeck="decks[showDeckIndex].code" :showCopy="false"></deck-detail>
    </div>
  </div>
</template>

<script>
import DeckPreview from '../deck/DeckPreview.vue'
import '../../assets/scss/decklib.scss'
import DeckDetail from '../deck/DeckDetail.vue'

export default {
  components: { DeckPreview, DeckDetail },
  emits: ['back'],
  data() {
    return {
      decks: [],
      showDeckIndex: null,
    }
  },
  mounted() {
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
          }
        ]
      }
    },
    onBack() {
      console.log("Go back!")
      this.$emit('back')
    },
    onBackSecond() {
      this.showDeckIndex = null
    },
    showDeck(event, id) {
      if (!event.target.className.includes('trash')) {
        // Not deleting the deck
        // this.$emit('showDeck', deck)
        this.showDeckIndex = id
      }
    },
  }
}
</script>