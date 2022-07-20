<template>
  <div class="flex h-full justify-center overflow-y-auto">
    <div class="w-0 max-w-5xl flex-1">
      <div class="flex h-full flex-col px-2 sm:px-0">
        <p class="pt-3 pb-5 text-left text-3xl">{{ title }}</p>
        <p v-if="error" class="text-left">{{ $t("str.invalidDeck") }}</p>
        <div class="block h-0 flex-1 md:flex">
          <div class="flex w-full flex-col md:w-1/4">
            <div
              class="flex h-0 max-h-96 w-full flex-1 justify-center overflow-y-auto sm:max-h-full sm:overflow-y-visible md:justify-start"
            >
              <deck-detail class="max-w-[250px]" :base-deck="code" :show-add="true"></deck-detail>
            </div>
          </div>
          <div class="flex w-full flex-col px-4 text-left md:w-3/4" v-if="isValid">
            <div class="h-0 flex-1">
              <!-- Loading -->
              <div v-if="loadingStats || store.archetypeLoading" class="pb-4 text-2xl">
                <span><i class="fas fa-circle-notch fa-spin"></i></span>
                <span class="pl-2">{{ $t("str.loading") }}</span>
              </div>

              <div v-if="noInfo">
                <div class="pb-3 text-3xl">{{ $t("str.noDetail") }}</div>
              </div>

              <!-- Meta -->
              <div v-if="!store.archetypeLoading && deckStats" class="pb-4">
                <div class="pt-4 pb-3 text-3xl sm:pt-0">
                  {{ $t("deckCode.archetypeStats") }}
                </div>
                <meta-group :no-detail="true" :selfExpand="true" :group="deckStats"></meta-group>
                <div class="pt-4 pb-3 text-3xl">
                  {{ $t("deckCode.archetypeMatchups") }}
                </div>
                <meta-matchup
                  v-if="!metaStore.isMetaLoading"
                  :matchups="deckStats.matchup"
                ></meta-matchup>
                <div class="text-2xl" v-if="metaStore.isMetaLoading">
                  <span><i class="fas fa-circle-notch fa-spin"></i></span>
                  <span class="pl-2">{{ $t("str.loading") }}</span>
                </div>
              </div>

              <!-- Mulligan -->

              <div v-if="keeps || swaps" class="pb-6">
                <div class="pb-3 text-3xl">
                  {{ $t("deckCode.mulliganGuide") }}
                </div>
                <div class="block w-full sm:flex">
                  <div class="w-full sm:w-1/2" v-if="keeps">
                    <div class="pb-2 text-xl">{{ $t("deckCode.keep") }}</div>
                    <div class="flex w-full items-center" v-for="keep in keeps" :key="keep.code">
                      <card-preview class="flex-1" :code="keep.code"></card-preview>
                      <div class="px-4">+{{ keep.rate }}%</div>
                    </div>
                  </div>
                  <div class="w-full sm:w-1/2" v-if="swaps">
                    <div class="pb-2 text-xl">
                      {{ $t("deckCode.mulligan") }}
                    </div>
                    <div class="flex w-full items-center" v-for="swap in swaps" :key="swap.code">
                      <card-preview class="flex-1" :code="swap.code"></card-preview>
                      <div class="px-4">-{{ swap.rate }}%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import DeckEncoder from "../../modules/runeterra/DeckEncoder"
import CardPreview from "../deck/CardPreview.vue"
import DeckDetail from "../deck/DeckDetail.vue"

import MetaGroup from "../meta/MetaGroup.vue"
import MetaMatchup from "../meta/MetaMatchup.vue"
import { useMetaStore } from "../../store/StoreMeta"
import { getDeckID } from "./PanelMeta.vue"
import { useBaseStore } from "../../store/StoreBase"

import { useArchetypeStore } from "../../store/StoreArchetype"

let error = ref("")
let title = ref("Deck Detail")
let isValid = ref(false)
let loadingStats = ref(false)
let deckID = ref("")

const store = useArchetypeStore()
const metaStore = useMetaStore()

const props = defineProps({
  code: String,
})

onMounted(() => {
  // console.log("PANEL CODE:", props.code)
  metaStore.fetchMetaGroups()
  processDeck()
})

const deckStats = computed(() => {
  if (store.archetypeDetails) {
    if (deckID.value in store.archetypeDetails) {
      let group = store.archetypeDetails[deckID.value]
      let feature = group.decks.find((deck) => {
        return deck.deck_code == props.code
      })
      let newGroup = { ...group }
      newGroup.feature = feature
      return newGroup
    }
  }

  return null
})

const noInfo = computed(() => {
  return !(loadingStats.value || store.archetypeLoading) && !deckStats.value
})

function processDeck() {
  const baseStore = useBaseStore()
  var deck
  try {
    deck = DeckEncoder.decode(props.code)
  } catch (err) {
    console.log(err)
    error.value = err
  }
  isValid.value = true
  deckID.value = getDeckID(props.code)
  console.log(deckID.value)
  store.fetchArchetypeDetail(deckID.value)
  let champNames = deck.reduce((names, card) => {
    let info = baseStore.sets.find((info) => info.cardCode == card.code)
    if (info.rarityRef === "Champion") {
      names.push(info.name)
    }
    return names
  }, [])
  title.value = champNames.join(" ")
}
</script>
