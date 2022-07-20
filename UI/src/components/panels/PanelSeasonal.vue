<template>
  <div class="flex h-full justify-center px-2">
    <div class="w-0 max-w-5xl flex-1">
      <div class="flex h-full flex-col sm:px-0">
        <h1 class="title pb-4 pt-1 text-left text-3xl sm:pt-0">
          {{ $t("str.seasonal") }}
        </h1>

        <MetaFilter
          class="sticky top-0 z-[5] bg-gray-900"
          @bind-filter="bindFilter"
          @refresh="
            () => {
              fetch()
            }
          "
          ><div
            v-if="data && data.time"
            class="absolute top-[16px] right-12 pb-2 text-right text-xs text-gray-300 transition-colors hover:text-gray-100"
          >
            {{ $t("str.lastUpdated") }}
            {{
              formatDistanceStrict(new Date(data.time), new Date(), {
                addSuffix: true,
                locale: dateFNSLocales[$i18n.locale],
              })
            }}
          </div>
        </MetaFilter>

        <!-- Select sorting function -->
        <div
          v-if="filteredMeta && filteredMeta.length != 0"
          class="items-center pl-4 pb-3 text-left text-sm sm:flex"
        >
          <div class="pb-2 sm:pb-0">
            <span class="mr-2 text-gold-300">{{ $t("str.sort") }}</span>
            <button
              v-for="(rule, index) in sortRules"
              class="ml-1.5 rounded px-2 py-1 hover:bg-gray-600"
              :class="{ 'bg-gray-600': sortRuleID == index }"
              :key="rule"
              @click="
                () => {
                  if (sortRuleID != index) {
                    sortRuleID = index
                    isSortAscending = false
                  } else {
                    isSortAscending = !isSortAscending
                  }
                }
              "
            >
              {{ $t(`meta.sort.${rule}`) }}
              <span v-if="sortRuleID == index"
                ><i
                  class="fad pl-1"
                  :class="{ 'fa-sort-up': isSortAscending, 'fa-sort-down': !isSortAscending }"
                ></i
              ></span>
            </button>
          </div>

          <span class="ml-1.5 mr-2 hidden text-gray-300 sm:block">|</span>

          <div class="pb-2 sm:pb-0">
            <button
              class="mr-1.5 cursor-pointer rounded py-1 px-2 hover:bg-gray-600"
              :class="{ 'bg-gray-600': regionOption == index + 1 }"
              v-for="(option, index) in ['NA', 'EU', 'APAC']"
              :key="option"
              @click="
                () => {
                  regionOption = index + 1
                  fetch()
                }
              "
            >
              {{ option }}
            </button>
          </div>

          <span class="mr-2 hidden text-gray-300 sm:block">|</span>

          <span class="text-gray-300 transition-colors hover:text-white"
            >{{ $t("matches.game", { num: data.match_num }) }} · {{ data.version }}</span
          >
        </div>

        <div v-if="loading" class="pt-4 pb-5 text-2xl">
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
                <MetaGroup
                  @click="metaGroupOnClick(item._id)"
                  :group="item"
                  :index="index"
                  :sortRuleID="sortRuleID"
                ></MetaGroup>
              </div>
            </DynamicScrollerItem>
          </template>
        </DynamicScroller>

        <div v-if="!loading && (!filteredMeta || filteredMeta.length == 0)">
          {{ $t("str.noDetail") }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getDecodedDeck } from "../../modules/getDecodedDeck"
import MetaGroup from "../meta/MetaGroup.vue"
import { formatDistanceStrict, formatDuration } from "date-fns"

import { useMetaStore, timeOptionsUrl, regionOptionsUrl } from "../../store/StoreMeta"

import { ref, onMounted, computed } from "vue"
import MetaFilter from "../meta/MetaFilter.vue"
import { dateFNSLocales } from "../../assets/data/messages"

import { useRequest } from "../../composibles/request"

const timeOption = ref(0)
const regionOption = ref(1)

const requestURL = computed(() => {
  return `https://lormaster.azurewebsites.net/smeta${regionOptionsUrl[regionOption.value]}`
})

const { data, loading, duration, error, fetch, cancel } = useRequest(requestURL)

// const store = useMetaStore()

// const fetchMetaGroups = store.fetchMetaGroups

onMounted(() => {
  // fetchMetaGroups()
  fetch()
})

const sortRules = ["playRate", "winRate"]
var isSortAscending = ref(false)
var sortRuleID = ref(0)

const filter = ref([])

function bindFilter(newFilter) {
  filter.value = newFilter
}

const filteredMeta = computed(() => {
  if (!data.value || !data.value.data) return null

  const sortFn = (a, b) => {
    // Sort by play rate
    if (sortRuleID.value == 0) {
      return isSortAscending.value ? -1 : 1
    }
    // if a < b return -1;
    if (a.win_rate > b.win_rate) return isSortAscending.value ? 1 : -1
    return isSortAscending.value ? -1 : 1
  }

  if (filter.value.length > 0)
    // Loop through all meta group items
    return data.value.data
      .filter((item) => {
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
      .concat()
      .sort(sortFn)

  return data.value.data.concat().sort(sortFn)
})

function metaGroupOnClick(id) {
  const item = data.value.data.find((item) => item._id == id)
  if (item) {
    item.expanded = !item.expanded
  }
  // data.data[index].expanded = !data.data[index].expanded
  // console.log(data.data[index].expanded)
}
</script>
