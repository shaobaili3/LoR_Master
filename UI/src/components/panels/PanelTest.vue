<template>
  <div class="pt-5 pl-5">
    <input
      class="w-[800px] rounded bg-gray-700 p-2 placeholder-gray-300"
      type="text"
      v-model="testURL"
      name=""
      id=""
    />
    <div class="p-2">{{ isLoading ? "Loading..." : "Done" }}</div>
    <div class="p-2">{{ requestDuration / 1000 }} s</div>
    <button class="rounded bg-gray-700 p-2" @click="sendRequest()">Retry Request</button>

    <button class="rounded bg-gray-700 p-2">Test</button>
    <!-- <div class="flex w-10/12 m-auto mt-5">
      <div
        class="w-[1%] h-12"
        :class="{ ' border-white border-2 ': item == -1 }"
        :style="{ backgroundColor: winRateToColor(item / items100.length) }"
        v-for="item in items100"
        :key="item"
      ></div>
    </div> -->

    <div class="m-auto mt-10 flex w-10/12">
      <div
        class="group relative h-12 w-[5%]"
        :class="{ ' border-2 border-white ': item == -1 }"
        :id="item / 20"
        :style="{ backgroundColor: winRateToSimpleColor(item / 100) }"
        v-for="item in [...Array(100).keys()]"
        :key="item"
      >
        <div
          class="absolute left-0 -bottom-2 z-10 hidden translate-y-full whitespace-nowrap text-white group-hover:block"
        >
          {{ `${((item / 100) * 100).toFixed(0)}% | ${winRateToSimpleColor(item / 100)}` }}
        </div>
      </div>
    </div>

    <div class="m-auto mt-10 flex w-10/12">
      <div
        class="group relative h-12 w-[5%]"
        :class="{ ' border-2 border-white ': item == -1 }"
        :id="item / 20"
        :style="{ backgroundColor: winRateToColor(item / 100) }"
        v-for="item in [...Array(100).keys()]"
        :key="item"
      >
        <div
          class="absolute left-0 -bottom-2 z-10 hidden translate-y-full whitespace-nowrap text-white group-hover:block"
        >
          {{ `${((item / 100) * 100).toFixed(0)}%` }}
        </div>
      </div>
    </div>

    <div class="m-auto mt-10 flex w-10/12">
      <div
        class="group relative h-12"
        v-for="(item, index) in winrateGradientV2"
        :key="index"
        :style="{
          width:
            (index < winrateGradientV2.length - 1
              ? winrateGradientV2[index + 1][1] - item[1]
              : 1 - item[1]) *
              100 +
            '%',
          backgroundColor: '#' + item[0],
        }"
      >
        <div
          class="absolute left-0 -bottom-2 z-10 hidden translate-y-full whitespace-nowrap text-white group-hover:block"
        >
          {{ `${(item[1] * 100).toFixed(0)}% | ${item[0]}` }}
        </div>
      </div>
    </div>

    <div class="flex justify-center">
      <Tooltip>
        <div class="mt-5 w-fit text-gold-400" :class="{ 'bg-gray-600': isLoading }">Hello!</div>
        <template #float="floatProps">
          <div
            class="transition-opacity"
            :class="{ 'opacity-100': floatProps.visible, 'opacity-0': !floatProps.visible }"
          >
            Tooltip
          </div>
        </template>
      </Tooltip>

      <div
        class="mt-5 w-fit text-gold-400"
        :class="{ 'bg-white': isLoading }"
        v-tooltip="{
          content: '123',
          tag: 'div',
          class: 'p-2 bg-gray-800 text-white',
        }"
      >
        Hello!
      </div>
    </div>

    <!-- <div class="max-w-[200px]">
      <img class="drop-shadow" src="https://dd.b.pvp.net/latest/set5/en_us/img/cards/05BC093.png" />
    </div> -->

    <div class="flex gap-5">
      <div class="wrapper bg-gray-600 text-xs">
        <img class="container" src="/img/05IO004-cropped.885281bf.png" alt="" />
        <img class="container" src="/img/5.533e93f8.svg" alt="" />
        <img class="container" src="/img/10.cdb6bdc9.svg" alt="" />
        <img class="container" src="/img/05BC058-cropped.ba6ed14d.png" alt="" />
      </div>

      <div class="wrapper bg-gray-600 text-sm">
        <img class="container" src="/img/05IO004-cropped.885281bf.png" alt="" />
        <img class="container" src="/img/5.533e93f8.svg" alt="" />
        <img class="container" src="/img/10.cdb6bdc9.svg" alt="" />
        <img class="container" src="/img/05BC058-cropped.ba6ed14d.png" alt="" />
      </div>

      <div class="wrapper bg-gray-600 text-base">
        <img class="container" src="/img/05IO004-cropped.885281bf.png" alt="" />
        <img class="container" src="/img/5.533e93f8.svg" alt="" />
        <img class="container" src="/img/10.cdb6bdc9.svg" alt="" />
        <img class="container" src="/img/05BC058-cropped.ba6ed14d.png" alt="" />
      </div>

      <div class="wrapper bg-gray-600 text-lg">
        <img class="container" src="/img/05IO004-cropped.885281bf.png" alt="" />
        <img class="container" src="/img/5.533e93f8.svg" alt="" />
        <img class="container" src="/img/10.cdb6bdc9.svg" alt="" />
        <img class="container" src="/img/05BC058-cropped.ba6ed14d.png" alt="" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import axios from "axios"

import Tooltip from "../base/Tooltip.vue"

import {
  winRateToColor,
  winrateGradientV2,
  winRateToSimpleColor,
} from "../../modules/utils/colorUtils"

const testURL = ref("https://lormaster.herokuapp.com/search/americas/Kevor24/NA1")

const requestDuration = ref(0)
const isLoading = ref(false)

function sendRequest() {
  if (isLoading.value) {
    console.log("Request Already running")
    return
  }
  const reqeustStartTime = Date.now()
  isLoading.value = true
  axios
    .get(testURL.value)
    .then((response) => {
      isLoading.value = false
      var currentDuration = Date.now() - reqeustStartTime
      requestDuration.value = currentDuration
      console.log(`Got response in ${currentDuration} ms`)
    })
    .catch((e) => {
      isLoading.value = false
      console.log("error", e)
    })
}

onMounted(() => {
  sendRequest()
})
</script>

<style scoped>
.wrapper {
  width: auto;
  height: auto;
  gap: 2px;
  padding: 2px;
  display: flex;
}

.container {
  width: 2.65em;
  height: 2.65em;
  border: 2px solid white;
}
</style>
