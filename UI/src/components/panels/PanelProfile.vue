<template>
  <div class="flex h-full justify-center">
    <!-- <SignIn></SignIn> -->
    <!-- Center Column -->
    <div class="w-0 max-w-xl flex-1">
      <!-- Vertical Flex -->
      <div class="flex h-full flex-col items-center justify-center px-2 text-center sm:px-0">
        <div
          v-if="localInfo.name && localInfo.tag && localInfo.region"
          class="flex flex-col items-center rounded-xl bg-gray-800 px-12 py-8"
        >
          <div class="mb-2 flex h-24 w-24 items-center justify-center rounded-full bg-gray-700 text-5xl">
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
        <div v-else>
          <div class="text-2xl">
            {{ $t("str.noDetail") }}
          </div>
          <div>
            {{ $t("tooltips.lorlogin") }}
          </div>
        </div>
        <div class="mt-4 max-w-[220px] text-gray-200">Many more features are in active development</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStatusStore } from "../../store/StoreStatus"

import { ref, onMounted, computed } from "vue"
import SignIn from "../signin/SignIn.vue"
import { regionNameToShorts } from "./PanelLeaderboard.vue"
import { getRegionFaGlobeClass } from "../search/SearchBookmark.vue"

const localInfo = computed(() => {
  const store = useStatusStore()
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
  return { name: null, tag: null, server: null }
})

onMounted(() => {})
</script>
