<template>
  <div class="flex h-full flex-col">
    <div class="pb-4 pl-8 text-left text-3xl">Test Page</div>
    <div class="flex justify-center">
      <div>
        <input
          class="w-[800px] rounded bg-gray-700 p-2 placeholder-gray-300"
          type="text"
          v-model="testURL"
          name=""
          id=""
        />
        <div class="flex justify-end py-2">
          <div class="p-2" v-if="testError">{{ testError }}</div>
          <div class="p-2">{{ testLoading ? "Loading..." : "Done" }}</div>
          <div class="p-2" v-if="!testLoading">{{ testDuration / 1000 }} s</div>
          <button class="rounded bg-gray-700 p-2" @click="sendTestRequest()">Retry Request</button>
        </div>
      </div>
    </div>
    <div class="block h-0 flex-1 pl-8">
      <div class="pb-4 text-left text-2xl">Stats</div>
      <!-- Range for days -->

      <div class="flex items-center gap-2 pb-2">
        <span>Days:</span>
        <input
          type="text"
          v-model="range"
          @change="newRange"
          class="w-[50px] rounded bg-gray-700 p-2"
        />
      </div>
      <div v-if="!statsLoading">
        <div v-if="statsError">{{ statsError }}</div>

        <StatsSummary v-if="stats" :stats="stats" :statsDays="statsDays"></StatsSummary>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue"
import axios from "axios"

import Tooltip from "../base/Tooltip.vue"

import { DoughnutChart, LineChart } from "vue-chart-3"
import { useRequest } from "../../composibles/request"
import StatsSummary from "../stats/StatsSummary.vue"

import { useBaseStore } from "../../store/StoreBase"

const range = ref(7)

const baseStore = useBaseStore()

const testData = {
  labels: ["Paris", "Nîmes", "Toulon", "Perpignan", "Autre"],
  color: "#fff",
  datasets: [
    {
      label: "My First Dataset",
      data: [30, 40, 60, 70, 5],
      // backgroundColor: ["#77CEFF", "#0079AF", "#123E6B", "#97B0C4", "#A5C8ED"],
      backgroundColor: "rgb(75, 192, 192)",
      fill: false,
      borderColor: "rgb(75, 192, 192)",
    },
  ],
}

const testURL = ref(baseStore.API_WEB + "/match/americas/Kevor24/NA1")

const {
  loading: testLoading,
  duration: testDuration,
  fetch: sendTestRequest,
  error: testError,
} = useRequest(testURL)

const {
  loading: statsLoading,
  fetch: sendStatsRequest,
  error: statsError,
  data: stats,
} = useRequest(baseStore.API_WEB)

const rangeAPI = computed(() => {
  return `${baseStore.API_WEB}/status/${range.value}`
})

const { fetch: fetchStatusDays, error: statsDaysError, data: statsDays } = useRequest(rangeAPI)

function newRange() {
  if (range.value > 50) {
    range.value = 50
  }
  fetchStatusDays()
}

onMounted(() => {
  sendStatsRequest()
  fetchStatusDays()
})
</script>
