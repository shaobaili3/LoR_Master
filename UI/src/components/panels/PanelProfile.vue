<template>
  <div class="flex h-full justify-center">
    <!-- <SignIn></SignIn> -->
    <!-- Center Column -->
    <div class="w-0 max-w-xl flex-1">
      <!-- Vertical Flex -->
      <div class="flex h-full flex-col items-center justify-center px-2 text-center sm:px-0">
        <div
          v-if="localInfo.name && localInfo.tag && localInfo.region"
          class="relative flex flex-col items-center rounded-xl bg-gray-800 px-12 py-8"
        >
          <button
            class="absolute top-2 right-2 px-2 py-1 text-gray-300 transition-colors hover:text-white"
            @click="handleChangeNameButtonClick"
          >
            <i class="fas fa-pencil"></i>
          </button>
          <div
            class="mb-2 flex h-24 w-24 items-center justify-center rounded-full bg-gray-700 text-5xl"
          >
            {{ localInfo.name[0].toUpperCase() }}
          </div>
          <div class="mb-2 text-2xl">{{ localInfo.name }}</div>
          <div class="mb-4 text-gray-200">
            <i class="fas" :class="getRegionFaGlobeClass(localInfo.region)"></i>
            {{ localInfo.region }}
          </div>
          <router-link
            class="hover:no-underline"
            :to="{
              name: 'search',
              query: {
                name: localInfo.name,
                region: localInfo.region,
                tag: localInfo.tag,
              },
            }"
          >
            <div
              class="rounded-md border-2 border-gold-400 bg-gray-800 p-2 px-6 text-center text-gold-400 transition-colors hover:bg-gray-900"
            >
              {{ $t("search.leaderboard.base") }}
            </div></router-link
          >
        </div>
        <div v-else class="mb-12">
          <!-- <div class="text-2xl">
            {{ $t("str.noDetail") }}
          </div> -->
          <div class="mb-12 text-3xl">
            {{ $t("str.welcome") }}
          </div>

          <div class="mb-4 flex gap-2">
            <div class="flex flex-col gap-2 text-left">
              <div class="text-sm">{{ $t("str.server") }}</div>
              <BaseSelect
                :class="'max-w-[100px]'"
                :options="options"
                :default="optionDefault"
                @input="handleRegionSelect"
              ></BaseSelect>
            </div>
            <div class="flex flex-col gap-2 text-left">
              <div class="text-sm">{{ $t("str.username") }}</div>
              <input
                spellcheck="false"
                autocomplete="off"
                class="h-9 w-full rounded-[6px] border-none pl-4 text-sm text-white placeholder-gray-300 outline-none transition-colors"
                :class="{
                  'bg-gray-800 focus:bg-gray-700': username === '',
                  'bg-gray-600 focus:bg-gray-500': username !== '',
                }"
                v-model="username"
                placeholder="FlyingFish"
              />
            </div>
            <div class="flex flex-col gap-2 text-left">
              <div class="text-sm">
                {{ $t("str.tag")
                }}<Tooltip>
                  <span class="transition-color ml-2 cursor-help text-gray-300 hover:text-gray-150">
                    <i class="fas fa-question-circle"></i>
                  </span>
                  <template #float="props">
                    <div
                      class="pointer-events-none z-50 flex w-full min-w-[10rem] justify-center pl-[88px] pr-2 pb-4 transition"
                      :class="{
                        'delay-250 opacity-100': props.visible,
                        'opacity-0': !props.visible,
                      }"
                    >
                      <div>
                        <!-- <p class="pb-2">
                      To find out your name and tag, go to friends list and hover on your icon
                    </p> -->
                        <img
                          class="h-auto w-fit rounded-lg object-contain shadow-glow"
                          :src="require('../../assets/images/name_tag_screenshot.png')"
                        />
                      </div>
                    </div>
                  </template>
                </Tooltip>
              </div>
              <input
                spellcheck="false"
                autocomplete="off"
                class="h-9 w-full rounded-[6px] border-none pl-4 text-sm text-white placeholder-gray-300 outline-none transition-colors"
                :class="{
                  'bg-gray-800 focus:bg-gray-700': tag === '',
                  'bg-gray-600 focus:bg-gray-500': tag !== '',
                }"
                v-model="tag"
                placeholder="0000"
              />
            </div>
          </div>
          <dv class="flex w-full justify-end"
            ><button
              :disabled="username === '' || tag === ''"
              @click="handleCheckButtonClick"
              class="rounded bg-gray-700 px-10 py-1.5 text-base transition-colors hover:bg-gray-600 disabled:cursor-default disabled:bg-gray-800 disabled:text-gray-500 disabled:hover:bg-gray-800"
            >
              <i class="fas fa-check"></i></button
          ></dv>
        </div>
        <!-- <div class="mt-4 max-w-[220px] text-gray-200">Many more features are in active development</div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStatusStore } from "../../store/StoreStatus"
import { usePlayerInfoStore } from "../../store/StorePlayerInfo"

import { ref, onMounted, computed } from "vue"
import SignIn from "../signin/SignIn.vue"
import { regionNameToShorts } from "./PanelLeaderboard.vue"
import { getRegionFaGlobeClass } from "../search/SearchBookmark.vue"
import BaseSelect from "../base/BaseSelect.vue"
import Tooltip from "../base/Tooltip.vue"
import { router } from "../../pages/home/main"

let options = ["AM", "EU", "APAC"]
let optionDefault = "AM"

let username = ref("")
let tag = ref("")
let region = ref(optionDefault)

const store = useStatusStore()
const playerStore = usePlayerInfoStore()

let handleRegionSelect = (newOption) => {
  region.value = newOption
}

let handleCheckButtonClick = () => {
  if (username.value !== "" && tag.value !== "") {
    playerStore.changePlayerInfo({
      name: username.value,
      tag: tag.value,
      region: region.value,
    })
    router.push({
      path: "/search",
      query: {
        name: username.value,
        tag: tag.value,
        region: region.value,
      },
    })
  }
}

let handleChangeNameButtonClick = () => {
  playerStore.deletePlayerInfo()
  router.go()
}

const localInfo = computed(() => {
  console.log(playerStore.playerInfo)
  var name, tag, region
  if (store.localPlayerID) {
    var splited = store.localPlayerID.split("#")
    name = splited[0]
    tag = splited[1]
    region = regionNameToShorts(store.localServer)
    return {
      name,
      tag,
      region,
    }
  }
  let info = playerStore.playerInfo
  if (info)
    return {
      name: info.name,
      tag: info.tag,
      region: info.region,
    }

  return { name: null, tag: null, region: null }
})

onMounted(() => {
  playerStore.initStore()
})
</script>
