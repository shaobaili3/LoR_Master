<template>
  <div class="pt-5 pl-5">
    <input
      class="w-[800px] rounded bg-gray-700 p-2"
      type="text"
      v-model="testURL"
      name=""
      id=""
    />
    <div class="p-2">{{ isLoading ? "Loading..." : "Done" }}</div>
    <div class="p-2">{{ requestDuration / 1000 }} s</div>
    <button class="rounded bg-gray-700 p-2" @click="sendRequest()">
      Retry Request
    </button>

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
          {{
            `${((item / 100) * 100).toFixed(0)}% | ${winRateToSimpleColor(
              item / 100
            )}`
          }}
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
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import {
  winRateToColor,
  winrateGradientV2,
  winRateToSimpleColor,
} from "../../modules/utils/colorUtils";

const testURL = ref(
  "https://lormaster.herokuapp.com/search/americas/Kevor24/NA1"
);

const requestDuration = ref(0);
const isLoading = ref(false);

function sendRequest() {
  if (isLoading.value) {
    console.log("Request Already running");
    return;
  }
  const reqeustStartTime = Date.now();
  isLoading.value = true;
  axios
    .get(testURL.value)
    .then((response) => {
      isLoading.value = false;
      var currentDuration = Date.now() - reqeustStartTime;
      requestDuration.value = currentDuration;
      console.log(`Got response in ${currentDuration} ms`);
    })
    .catch((e) => {
      isLoading.value = false;
      console.log("error", e);
    });
}

onMounted(() => {
  sendRequest();
});
</script>
