<template>
  <div class="decklib">
    <div class="title">{{$t('decklib.title')}}</div>
    <div class="btn-container">
      <!-- <button class="btn btn-add">
        <span><i class="fas fa-plus"></i></span>
      </button> -->
      <div class="input-bar-container"> 
        <input
          spellcheck="false"
          autocomplete="off"
          class="search-bar"
          @paste="onPaste"
          v-model="codeText"
          :placeholder="$t('decklib.placeholder')"
        />
        <div class="icon inside left">
          <span><i class="fas fa-paste"></i></span>
        </div>
      </div>
      <div class="error-message">
        {{error}}
      </div>
    </div>
    <div class="decks-container">
      <div class="deck-block" @click="showDeck($event, deck.code)" v-for="(deck, id) in decks" :key="id">
        <div class="decklib-deck-title">
          {{deck.title}}
        </div>
        <div @click="handleDelete(id)" class="btn-delete btn"><span><i class="fas fa-trash"></i></span></div>
        <deck-preview 
          :deck="deck.code">
        </deck-preview>
      </div>
    </div>
  </div>
</template>

<script>
const IS_ELECTRON = window.ipcRenderer !== undefined
import '../../assets/scss/decklib.scss'
import DeckPreview from '../deck/DeckPreview.vue'

import {showDeckMixin} from '../mixins'

import DeckEncoder from '../../modules/runeterra/DeckEncoder'

export default {
  components: { DeckPreview },
  mixins: [showDeckMixin],
  data() {
    return {
      decks: [],
      error: "",
      codeText: "",
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
            console.log("Deck Lib", val)
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
    showDeck(event, deck) {
      if (!event.target.className.includes('trash')) {
        // Not deleting the deck
        this.$emit('showDeck', deck)
      }
    },
    updateStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send('save-store', 'deck-lib', JSON.stringify(this.decks, null, '\t'))
      }
    },
    onPaste() {
      
      setTimeout(() => {
        let pasteContent = this.codeText

        try {
          let deck = DeckEncoder.decode(pasteContent)
          let champNames = deck.reduce((names, card) => {
            let info = this.sets.find(info => info.cardCode == card.code)
            if (info.rarityRef === "Champion") {
              names.push(info.name)
            }
            return names
          }, [])

          // console.log("Champ names",champNames)
          this.decks.unshift({
            title: champNames.join(' '),
            code: pasteContent,
          })
          this.updateStore()
        } catch (error) {
          console.log(error)
          this.error = this.$t('str.invalidDeck')
          setTimeout(() => {
          this.error = ""
        }, 2000)
        }
        
        this.codeText = ""
        
      }, 100)
      
    },
    handleDelete(id) {
      this.decks.splice(id, 1)
      this.updateStore()
    }
  }
}
</script>