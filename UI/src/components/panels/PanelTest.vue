<template>
  <div class="pt-5 pl-5">
    <input class="bg-gray-700 w-[800px] p-2 rounded" type="text" v-model="testURL" name="" id="" />
    <div class="p-2">{{ isLoading ? "Loading..." : "Done" }}</div>
    <div class="p-2">{{ requestDuration / 1000 }} s</div>
    <button class="p-2 bg-gray-700 rounded" @click="sendRequest()">Retry Request</button>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import axios from "axios"

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
      console.log(response)
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
