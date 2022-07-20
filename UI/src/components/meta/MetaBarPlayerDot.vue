<template>
  <Tooltip>
    <div
      class="absolute top-1/2 h-2 w-2 -translate-y-1/2 rounded-full"
      :style="{
        backgroundColor: winRateToColor(player.win_rate),
        left: player.win_rate * 100 + '%',
      }"
      @click="routePlayerProfile(player)"
    ></div>
    <template #float="props">
      <div
        class="pointer-events-none z-50 ml-2 w-fit min-w-[10rem] rounded-lg bg-gray-700 py-2 pl-2 pr-2 text-left"
        :class="{
          block: props.visible,
          hidden: !props.visible,
        }"
      >
        <p class="text-sm text-gray-200">
          <span class="pre-info">
            <i
              class="fas"
              :class="player.server === 'sea' ? 'fa-globe-asia' : 'fa-globe-' + player.server"
            ></i>
          </span>
          {{ $t("str.regions." + player.server) }}
        </p>
        <p class="text-xl">{{ player.riot_id.split("#")[0] }}</p>
        <p class="text-gray-200">
          {{ $t("matches.games", { num: player.count }) }}
        </p>
        <p
          :style="{
            color: winRateToColor(player.win_rate),
          }"
        >
          {{
            $t("matches.winRate", {
              num: (player.win_rate * 100).toFixed(1),
            })
          }}
        </p>
      </div>
    </template>
  </Tooltip>
</template>

<script setup>
import { winRateToColor } from "../../modules/utils/colorUtils"
import { regionNameToShorts } from "../panels/PanelLeaderboard.vue"

import { router } from "../../pages/home/main"
import Tooltip from "../base/Tooltip.vue"

function routePlayerProfile(player) {
  var splited = player.riot_id.split("#")
  router.push({
    path: "/search",
    query: {
      name: splited[0],
      tag: splited[1],
      region: regionNameToShorts(player.server),
    },
  })
}

defineProps({
  player: Object,
})
</script>
