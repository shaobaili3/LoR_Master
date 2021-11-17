<template>
  <div class="decklib">
    <modal-warning ref="warningModal"></modal-warning>
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
    <div class="decks-container gap-4">
      <div class="deck-block p-2.5" @click="showDeck($event, deck.code)" v-for="(deck, id) in decks" :key="id">
        <div class="decklib-deck-title text-left" :title="deck.title">
          {{deck.title}} <span v-if="deck.date" class="block text-xs font-light text-gray-200">{{format(new Date(deck.date), "HH:mm | yyyy-MM-dd")}}</span>
        </div>
        <div @click.stop="onClickDelete(id)" class="btn-delete btn"><span><i class="fas fa-trash"></i></span></div>
        <div class="version tooltip">
          <span class="tooltiptext top pointer-events-none max-w-full overflow-x-hidden overflow-ellipsis">
            {{deck.code}}
          </span>
          <deck-preview 
            :deck="deck.code">
          </deck-preview>
        </div>
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
import ModalWarning from '../modals/ModalWarning.vue'
import { format, subDays } from 'date-fns'

export default {
  components: { DeckPreview, ModalWarning },
  mixins: [showDeckMixin],
  data() {
    return {
      decks: [],
      error: "",
      codeText: "",
      loaded: false,
      pasteBuffer: null,
    }
  },
  emits: ['pasted'],
  mounted() {
    this.initStore()
  },
  methods: {
    format: format,
    subDays: subDays,
    initStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send('request-store', 'deck-lib')

        window.ipcRenderer.on('reply-store', (event, key, val) => {
          console.log("Got Store:", key)

          if (key == 'deck-lib' && val) {
            console.log("Load Deck Lib")
            this.decks = JSON.parse(val)
            this.loaded = true
            if (this.pasteBuffer) {
              console.log("Process pasteBuffer")
              this.processPaste(this.pasteBuffer)
            }
          }
        })
      } else {
        
        // Sample data
        this.decks = [
          {
            title: "Bandle Nox",
            date: Date.now() - 10,
            code: 'CQBACAIDG4EAKCQBOSCADGABUYA2OANPAHBACAYBAIDC4AICAMEQIBIKFGQADQABYYAQCAIDAMGQ'
          },
          {
            title: "Draven Sion",
            date: Date.now() - 30000,
            code: 'CECACAIDCQAQIBAQAMCQGAIJBUCACBBGE4WTIAYBAEBS4AIBAQAQCAYDB4CACAQDBEAQGBASAICQGBAGAMAQGCZDGM'
          },
          {
            title: "Thresh Asol",
            date: Date.now() - 12394123,
            code: 'CQBQCBIKV4AQEAIFFA2AKAYJC5KFMXDAAQAQCBIZAECASDIBAUCQ6AQDBFEVOAYBAQCTQAQDBERTGAYBAUAQ6HI'
          }
        ]

        this.loaded = true
      }
    },
    showDeck(event, deck) {
      if (!event.target.className.includes('btn-delete')) {
        // Not deleting the deck
        this.$emit('showDeck', deck)
      }
    },
    updateStore() {
      if (window.ipcRenderer) {
        window.ipcRenderer.send('save-store', 'deck-lib', JSON.stringify(this.decks, null, '\t'))
      }
    },
    onPaste(event) {
      event.preventDefault();
      let pasteContent = (event.clipboardData || window.clipboardData).getData('text');
      this.processPaste(pasteContent)
    },
    processPaste(deckCode) {
      console.log("Process Paste")

      if (!this.loaded) {
        console.log("Save Paste")
        this.pasteBuffer = deckCode
        return
      }

      try {
        let deck = DeckEncoder.decode(deckCode)
        let champNames = deck.reduce((names, card) => {
          let info = this.sets.find(info => info.cardCode == card.code)
          if (info.rarityRef === "Champion") {
            names.push(info.name)
          }
          return names
        }, [])
        let i = 0;
        let newTitle = champNames.join(' ')
        while (this.decks.findIndex((item) => item.title == newTitle) != -1 && i < 1000) {
          i+= 1;
          newTitle = `#${i} ` + champNames.join(' ');
          console.log(newTitle)
        }
        this.decks.unshift({
          title: newTitle,
          date: new Date(),
          code: deckCode,
        })
        this.updateStore()
        this.$emit('pasted')
      } catch (error) {
        console.log(error)
        this.error = this.$t('str.invalidDeck')
        setTimeout(() => {
          this.error = ""
        }, 2000)
      }
    },
    onClickDelete(id) {
      this.$refs.warningModal.showPanel([
      () => {
        console.log("Confirm Delete")
        this.handleDelete(id)
      },
      () => {
        console.log("Nothing happens")
      },
      ], `${this.$t('str.delete')},${this.decks[id].title}`)
    },
    handleDelete(id) {
      this.decks.splice(id, 1)
      this.updateStore()
    }
  }
}
</script>