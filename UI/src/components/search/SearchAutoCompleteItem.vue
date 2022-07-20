<template>
  <div class="flex items-center">
    <div>
      {{ player.name }}
    </div>
    <div v-if="region && region != selectedRegion" class="pl-2 text-sm text-gray-300">
      <i class="fas" :class="getRegionFaGlobeClass(region)"></i>
      {{ region }}
    </div>
    <!-- <div class="pl-2 text-sm text-gray-300">
      {{ obscureTag }}
    </div> -->
    <div class="w-0 flex-1"></div>

    <div class="pl-4 text-sm text-gray-300" v-if="leaderboardInfo && leaderboardInfo.rank != null">
      <i class="fas fa-trophy pr-1"></i>{{ leaderboardInfo.rank + 1 }}
    </div>

    <div class="pl-4 text-sm text-gray-300" v-if="player.game_latest_rank_time">
      {{
        formatDistanceStrict(new Date(player.game_latest_rank_time), new Date(), {
          addSuffix: true,
          locale: dateFNSLocales[$i18n.locale],
        })
      }}
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"

import { getLeaderboardFromPlayer } from "../match/PlayerMatches.vue"
import { regionNameToShorts } from "../panels/PanelLeaderboard.vue"
import { getRegionFaGlobeClass } from "./SearchBookmark.vue"
import { formatDistanceStrict } from "date-fns"
import { dateFNSLocales } from "../../assets/data/messages"

const props = defineProps({
  selectedRegion: String,
  player: Object,
})

const leaderboardInfo = computed(() => {
  return getLeaderboardFromPlayer(
    regionNameToShorts(props.player.server),
    props.player.name,
    props.player.tag
  )
})

const region = computed(() => {
  return regionNameToShorts(props.player.server)
})

// const obscureTag = computed(() => {
//   return (
//     "# " + "• ".repeat(props.player.tag.length - 1) + props.player.tag[props.player.tag.length - 1]
//   )
// })
</script>
