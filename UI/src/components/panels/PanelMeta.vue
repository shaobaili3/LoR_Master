<template>
  <div class="flex justify-center h-full px-4">
    <div class="flex-1 w-0 max-w-4xl">
      <div class="flex flex-col h-full px-2 sm:px-0">
        <p class="pt-3 pb-5 text-3xl text-left title">{{ $t("str.meta") }}</p>

        <MetaFilter class="sticky top-0 z-[5] bg-gray-900" @bind-filter="bindFilter"></MetaFilter>

        <div v-if="store.isMetaLoading" class="pb-5 text-2xl">
          <i class="fas fa-circle-notch fa-spin"></i>
          {{ $t("str.loading") }}
        </div>

        <!-- <p v-if="metaGroups" class="pb-2 text-left sub-title">{{$t("matches.games", {num: totalGames})}}</p> -->
        <DynamicScroller
          :items="filteredMeta"
          :min-item-size="90"
          key-field="_id"
          v-if="filteredMeta && filteredMeta.length > 0"
          class="flex-1 h-0"
        >
          <template v-slot="{ item, index, active }">
            <DynamicScrollerItem :item="item" :active="active" :size-dependencies="[item.expanded]" :data-index="index">
              <div class="py-1 pb-4">
                <MetaGroup @click="metaGroupOnClick(item._id)" :group="item"></MetaGroup>
              </div>
            </DynamicScrollerItem>
          </template>
        </DynamicScroller>

        <div v-if="!store.isMetaLoading && (!filteredMeta || filteredMeta.length == 0)">
          {{ $t("str.noDetail") }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DeckEncoder from "../../modules/runeterra/DeckEncoder"
import { useBaseStore } from "../../store/StoreBase"
import { regionNames, regionRefID } from "./PanelDeckCode.vue"
import { championCards } from "../../assets/data/champion"

export const getDecodedDeck = (code) => {
  var deck = null
  if (code) {
    try {
      deck = DeckEncoder.decode(code)
    } catch (error) {
      console.log(error)
      return null
    }
  }
  return deck
}

export const getFactions = (code) => {
  const baseStore = useBaseStore()
  var cards = getDecodedDeck(code)
  if (!cards) return null

  var factionIDs = []
  for (var j in cards) {
    var cardCode = cards[j].code
    var card = baseStore.sets_en[cardCode]
    if (card) {
      if (card.regions && card.regions.length == 1) {
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]

        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }
  return factionIDs
}

export const getChamps = (code) => {
  const baseStore = useBaseStore()
  var deck = getDecodedDeck(code)
  if (!deck) return null

  var champs = []
  for (var j in deck) {
    let cardCode = deck[j].code
    if (championCards.champObj[cardCode] != null) {
      var card = baseStore.sets_en[cardCode]
      if (card) {
        let champ = {
          count: deck[j].count,
          code: cardCode,
          name: card.name,
        }
        champs.push(champ)
      }
    }
  }
  champs = champs.sort((a, b) => (a.count > b.count ? -1 : 1))
  return champs
}

export const getDeckID = (code) => {
  var factionNames = getFactions(code)
    .map((id) => regionNames[id])
    .sort()
  var champNames = getChamps(code)
    .slice(0, 2)
    .map((champ) => champ.name)
    .sort()
  if (getChamps.length == 0) {
    champNames = ["No-Champion"]
  }
  var IDString = factionNames.join(" ") + " " + champNames.join(" ")
  return IDString
}
</script>

<script setup>
import MetaGroup from "../meta/MetaGroup.vue"

import { useMetaStore } from "../../store/StoreMeta"

import { ref, onMounted, computed } from "vue"
import MetaFilter from "../meta/MetaFilter.vue"

const store = useMetaStore()

const fetchMetaGroups = store.fetchMetaGroups

onMounted(() => {
  fetchMetaGroups()
})

const filter = ref([])

function bindFilter(newFilter) {
  filter.value = newFilter
}

const filteredMeta = computed(() => {
  if (!store.metaGroups) return null
  if (filter.value.length > 0)
    // Loop through all meta group items
    return store.metaGroups.filter((item) => {
      // Loop through all filter items
      for (let i = 0; i < filter.value.length; i++) {
        const filterItem = filter.value[i]
        // Check if it is part of ID (Factions & Champ names)
        if (!item._id.toLowerCase().includes(filterItem.replace(/\s+/g, "").toLowerCase())) {
          // Check if it is a filter for card name
          if (!item.decks) return false
          let isCard = false
          // Loop through all decks under this group
          for (let j = 0; j < item.decks.length; j++) {
            let deck = item.decks[j]
            let cards = getDecodedDeck(deck.deck_code)
            if (!cards) continue // Something went wrong with the deck code

            // Loop through all cards
            for (let k = 0; k < cards.length; k++) {
              var cardCode = cards[k].code
              if (filterItem == cardCode) {
                isCard = true
                break
              }
              // var card = baseStore.sets_en[cardCode]
              // if (card.name.includes(filterItem)) {
              //   console.log(card.name)
              //   isCardName = true
              // }
            }
          }
          if (!isCard) return false
        }
      }
      return true
    })

  return store.metaGroups
})

function metaGroupOnClick(id) {
  const item = store.metaGroups.find((item) => item._id == id)
  if (item) {
    item.expanded = !item.expanded
  }
  // store.metaGroups[index].expanded = !store.metaGroups[index].expanded
  // console.log(store.metaGroups[index].expanded)
}
</script>
