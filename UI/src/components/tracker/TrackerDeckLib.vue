<template>
  <div>
    <div
      class="sticky top-0 z-10 bg-gray-900 py-2 px-2 text-left text-xs text-gray-200 2xs:text-sm"
    >
      <i class="fas fa-star px-1"></i>{{ $t("decklib.title") }}
    </div>
    <div v-for="(deck, index) in decks" :key="deck.date" @click="expandDeck(index)">
      <!-- {{ deck }} -->
      <div class="mx-1 mb-1.5 bg-gray-800 pb-1.5 2xs:mb-2">
        <!-- Title -->
        <div
          class="overflow-x-hidden text-ellipsis whitespace-nowrap px-2 pt-2 pb-1 text-sm text-gray-100"
        >
          {{ deck.title }}
        </div>
        <!-- Date -->
        <div class="px-2 pb-1 text-xs text-gray-200">
          {{ format(new Date(deck.date), "HH:mm | yyyy-MM-dd") }}
        </div>

        <div class="px-2">
          <DeckPreview
            class="w-full gap-0.5 py-1 text-xs hover:bg-white/10 2xs:gap-1 2xs:py-1.5 2xs:text-sm"
            :deck="deck.code"
          ></DeckPreview>
        </div>
      </div>
      <transition name="height">
        <DeckDetail v-if="deck.expanded" :baseDeck="deck.code"></DeckDetail>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { useDeckLibStore } from "../../store/StoreDeckLib"

import { ref, onMounted } from "vue"
import DeckPreview from "../deck/DeckPreview.vue"
import DeckDetail from "../deck/DeckDetail.vue"
import { format } from "date-fns"

const decks = ref([])

function expandDeck(index) {
  const deckLibStore = useDeckLibStore()
  deckLibStore.decks[index].expanded = !deckLibStore.decks[index].expanded
}

onMounted(async () => {
  const deckLibStore = useDeckLibStore()
  await deckLibStore.initStore()
  decks.value = deckLibStore.decks
})
</script>
