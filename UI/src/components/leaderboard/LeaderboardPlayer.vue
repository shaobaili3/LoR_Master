<template>
  <div>
    <!-- Normal -->
    <div
      class="group relative grid h-16 cursor-pointer grid-cols-12 items-center transition-colors duration-150 hover:bg-gray-600 sm:mr-1"
      :class="{
        'bg-gray-800': !selected,
        'bg-gray-700': selected,
        'rounded-t-md': rank == '1',
      }"
      v-if="!isSearch"
    >
      <div class="z-[1]">
        <div v-if="rank == '1'"><i class="fas fa-crown text-yellow-500"></i></div>
        <div v-else-if="rank == '2'">
          <i class="fas fa-crown text-zinc-200"></i>
        </div>
        <div v-else-if="rank == '3'">
          <i class="fas fa-crown text-red-300"></i>
        </div>
        <div v-else>
          {{ rank }}
        </div>
      </div>
      <div
        class="z[1] col-span-5 overflow-hidden text-ellipsis whitespace-nowrap pl-2 sm:col-span-3"
      >
        {{ name }}
      </div>
      <div class="col-span-2 sm:col-span-1">{{ lp }}</div>
      <div class="hidden sm:col-span-2 sm:block">
        <div
          v-if="lastRankTime"
          class="text-sm text-white"
          :class="{
            'text-opacity-70': Date.now() - new Date(lastRankTime) > 1000 * 60 * 60 * 24,
            'text-opacity-40': Date.now() - new Date(lastRankTime) > 1000 * 60 * 60 * 24 * 7,
          }"
        >
          {{ lastRank }}
        </div>
      </div>
      <div class="hidden sm:col-span-2 sm:block">
        <div
          v-if="winRate != null"
          :style="{
            color: winRateToSimpleColor(winRate) /*0.6 + 0.4 * winRate*/,
          }"
        >
          {{ $t("matches.winRate", { num: (winRate * 100).toFixed(0) }) }}
        </div>
      </div>

      <div class="col-span-4 flex justify-center sm:col-span-3">
        <deck-preview
          class="gap-0.5 p-1 py-2.5 text-xs hover:bg-gray-800 sm:gap-1 sm:p-2"
          v-if="deck"
          @click.stop
          :deck="deck"
          :fixed-width="true"
          :size="1"
        ></deck-preview>
      </div>
    </div>
    <!-- Search text -->
    <div
      v-if="isSearch"
      class="relative flex h-16 cursor-pointer items-center justify-center rounded-b-md hover:bg-gray-600 sm:mr-1"
      :class="{
        'bg-gray-800': !selected,
        'bg-gray-700': selected,
      }"
    >
      <i class="fas fa-search pr-2"></i> {{ $t("search.leaderboard.base") }} "{{ name }}"
      <span class="absolute right-0 px-2 text-gray-200" v-if="selected">↵ Enter</span>
    </div>
  </div>
</template>

<script setup>
import { winRateToSimpleColor } from "../../modules/utils/colorUtils"
</script>

<script>
import DeckPreview from "../deck/DeckPreview.vue"
import { format, formatDistanceStrict } from "date-fns"

import { dateFNSLocales } from "../../assets/data/messages"

export default {
  components: { DeckPreview },
  props: {
    rank: String,
    name: String,
    lp: Number,
    deck: String,
    winRate: Number,
    lastRankTime: String,
    selected: Boolean,
    isSearch: Boolean,
  },
  computed: {
    lastRank() {
      // return format(new Date(this.lastRankTime), "HH:mm | yyyy-MM-dd")
      return formatDistanceStrict(new Date(this.lastRankTime), new Date(), {
        addSuffix: true,
        locale: dateFNSLocales[this.$i18n.locale],
      })
    },
    isChampion() {
      return this.rank == 1
    },
  },
}
</script>

<style>
.info {
  color: white;
  width: 100%;
  padding: 5px 0px;
  margin: 0px 0px;
  align-items: center;
  justify-content: space-around;
  border-radius: 5px;

  cursor: pointer;
}

.info:hover {
  background-color: var(--col-light-grey);

  /* box-shadow: 0px 0px 10px 2px var(--col-gold); */
}

.info.champion {
  /* color: rgb(126, 15, 15); */
  /* background-color: var(--col-gold); */

  box-shadow: inset 0px 0px 0px 2px var(--col-gold);
}

.info.champion:hover {
  /* color: var(--col-background); */
  /* background-color: rgb(250, 200, 34); */
  background: linear-gradient(60deg, var(--col-dark-gold), var(--col-gold));
  box-shadow: none;
  /* box-shadow: 0px 0px 10px 2px var(--col-gold); */
  /* font-weight: 600; */
}

.info-rank {
  width: 9.6%;
  text-align: center;
}

.info-name {
  width: 53.8%;
  text-align: left;
}

.info-lp {
  width: 9.6%;
  text-align: center;
}

a {
  text-decoration: none;
}
</style>
