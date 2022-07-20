<template>
  <div class="pl-1 text-xl">
    {{ $t("leaderboard.ladderHighlight").toUpperCase() }}
    <span class="pl-2 text-sm text-gold-400">{{ REGION_SHORTS[activeRegionID] }}</span>
  </div>
  <!-- Options -->
  <div class="flex pt-2 pl-1 text-sm">
    <button
      class="cursor-pointer rounded-md py-1 px-2 hover:bg-gray-600"
      :class="{ 'bg-gray-600': timeOption == 0 }"
      @click="
        () => {
          timeOption = 0
        }
      "
    >
      {{ formatDuration({ days: 1 }, { locale: dateFNSLocales[$i18n.locale] }) }}
    </button>
    <button
      class="ml-2 cursor-pointer rounded-md py-1 px-2 hover:bg-gray-600"
      :class="{ 'bg-gray-600': timeOption == 1 }"
      @click="
        () => {
          timeOption = 1
        }
      "
    >
      {{ formatDuration({ days: 3 }, { locale: dateFNSLocales[$i18n.locale] }) }}
    </button>
  </div>
  <!-- Headings -->
  <div class="grid h-12 grid-cols-12 items-center text-sm">
    <div class="col-span-3 overflow-hidden text-ellipsis whitespace-nowrap pl-4">
      {{ $t("leaderboard.name") }}
    </div>
    <div class="col-span-2 flex justify-center">{{ $t("leaderboard.rank") }}</div>
    <div class="col-span-2 flex justify-center">{{ $t("leaderboard.points") }}</div>
    <div class="col-span-5 flex justify-center">{{ $t("leaderboard.recent") }}</div>
  </div>
  <div
    v-if="highlightOneDay && highlightOneDay.length > 0"
    class="h-0 flex-1 overflow-auto rounded-md"
  >
    <div
      v-for="player in highlightOneDay"
      class="grid h-14 cursor-pointer grid-cols-12 items-center bg-gray-800 hover:bg-gray-600"
      :key="player.rank"
      @click="emits('searchPlayer', player)"
    >
      <div class="col-span-3 overflow-hidden text-ellipsis whitespace-nowrap pl-4">
        {{ player.name }}
      </div>
      <div class="col-span-2 flex items-center justify-center gap-1">
        <div class="flex flex-1 items-center justify-center text-center">
          <!-- <span class="text-xs"
            >{{ player.rank + parseInt(timeOption ? player.rank_3_change : player.rank_change) + 1
            }}<i class="fas fa-arrow-right pr-1 pl-1"></i
          ></span> -->
          {{ player.rank + 1 }}
        </div>
        <!-- <div class="flex-1 whitespace-nowrap text-sm text-green-300">
                <i class="fas fa-caret-up pr-1"></i>{{ player.rank_change }}
              </div> -->
      </div>
      <div class="col-span-2 flex items-center justify-center gap-1">
        <div class="flex-1 text-center">{{ player.lp }}</div>
        <div class="flex-1 whitespace-nowrap text-sm text-green-300">
          <i class="fas fa-caret-up pr-1"></i
          >{{ timeOption ? player.lp_3_change : player.lp_change }}
        </div>
      </div>
      <div class="col-span-5 flex justify-center">
        <deck-preview
          class="gap-0.5 p-1 py-2.5 text-xs hover:bg-gray-800 sm:gap-1 sm:p-2"
          v-if="player.deck_code"
          @click.stop
          :deck="player.deck_code"
          :fixed-width="true"
          :size="1"
        ></deck-preview>
      </div>
    </div>
  </div>
  <div v-else class="h-0 flex-1 overflow-auto rounded-md bg-gray-800"></div>
</template>

<script setup>
import DeckPreview from "../deck/DeckPreview.vue"
import { ref, computed } from "vue"
import { useLeaderboardStore } from "../../store/StoreLeaderboard"

import { REGION_SHORTS } from "../panels/PanelLeaderboard.vue"

import { formatDuration } from "date-fns"
import { dateFNSLocales } from "../../assets/data/messages"

const emits = defineEmits(["searchPlayer"])

const store = useLeaderboardStore()

const props = defineProps({
  activeRegionID: Number,
})

// const typeOptions = ["Points", "Rank"]
const timeOptions = ["1day", "3days"]

const timeOption = ref(1)
const typeOption = ref(0)

const highlightOneDay = computed(() => {
  if (!store.leaderboard || !store.leaderboard[props.activeRegionID]) {
    return null
  }
  return store.leaderboard[props.activeRegionID]
    .concat()
    .sort((a, b) => {
      // a < b -> -1
      // return b.rank_change - a.rank_change
      // return b.lp_change - a.lp_change
      return timeOption.value ? b.lp_3_change - a.lp_3_change : b.lp_change - a.lp_change
    })
    .slice(0, 10)
})
</script>
