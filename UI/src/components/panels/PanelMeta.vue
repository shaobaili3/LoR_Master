<template>
  <div class="flex h-full justify-center px-2">
    <div class="w-0 max-w-4xl flex-1">
      <div class="flex h-full flex-col sm:px-0">
        <h1 class="title pb-4 pt-1 text-left text-3xl sm:pt-0">
          {{ $t("str.meta") }}
          <h2 class="hidden pl-4 text-base text-gray-300 sm:inline" v-if="!IS_ELECTRON">
            {{ $t("meta.subtitle") }}
          </h2>
        </h1>

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
          class="h-0 flex-1"
        >
          <template v-slot="{ item, index, active }">
            <DynamicScrollerItem
              :item="item"
              :active="active"
              :size-dependencies="[item.expanded]"
              :data-index="index"
            >
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
  if (factionNames) {
    factionNames = factionNames.map((id) => regionNames[id]).sort()
  } else return null
  var champNames = getChamps(code)
  if (champNames) {
    if (champNames.length == 0) {
      champNames = ["No-Champion"]
    } else {
      champNames = champNames
        .slice(0, 2)
        .map((champ) => champ.name)
        .sort()
    }
  } else return null

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
