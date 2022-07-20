<template>
  <div class="flex">
    <div class="flex flex-col items-start pr-4">
      <div>Day: {{ stats.active.day }}</div>
      <div>Week: {{ stats.active.week }}</div>
      <div>Month: {{ stats.active.month }}</div>
      <div>All: {{ stats.active.all }}</div>
    </div>

    <BarChart :chartData="statsSummary" :options="charOptions"></BarChart>
    <LineChart :chartData="statsDays" :options="charOptions"></LineChart>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { BarChart, LineChart } from "vue-chart-3"

const props = defineProps({
  stats: Object,
  statsDays: Array,
})

const statsSummary = computed(() => {
  if (props.stats) {
    var stat = props.stats.active
    return {
      labels: ["Day", "Week", "Month", "All"],
      color: "#fff",
      datasets: [
        {
          label: "Stats Summary",
          data: [stat.day, stat.week, stat.month, stat.all],
          // backgroundColor: ["#77CEFF", "#0079AF", "#123E6B", "#97B0C4", "#A5C8ED"],
          backgroundColor: "rgb(75, 192, 192)",
          fill: false,
          borderColor: "rgb(75, 192, 192)",
        },
      ],
    }
  }
  return null
})

const statsDays = computed(() => {
  if (props.statsDays) {
    // var stat = props.stats.active
    var len = props.statsDays.length
    return {
      labels: [...Array(len).keys()],
      color: "#fff",
      datasets: [
        {
          label: `Stats Days (${len})`,
          data: props.statsDays.slice().reverse(),
          backgroundColor: "rgb(75, 192, 192)",
          fill: false,
          borderColor: "rgb(75, 192, 192)",
        },
      ],
    }
  }
  return null
})

const charOptions = {
  // plugins: {
  //   legend: {
  //     labels: {
  //       color: "white",
  //     },
  //   },
  // },
  // scales: {
  //   y: {
  //     ticks: {
  //       color: "white",
  //     },
  //   },
  //   x: {
  //     ticks: {
  //       color: "white",
  //     },
  //   },
  // },
}
</script>
