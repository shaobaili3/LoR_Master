<template>
  <div class="flex justify-center h-full">
    <!-- <SignIn></SignIn> -->
    <!-- Center Column -->
    <div class="flex-1 w-0 max-w-xl">
      <!-- Vertical Flex -->
      <div class="flex flex-col items-center justify-center h-full px-2 text-center sm:px-0">
        <div
          v-if="localInfo.name && localInfo.tag && localInfo.region"
          class="flex flex-col items-center px-12 py-8 bg-gray-800 rounded-xl"
        >
          <div class="flex items-center justify-center w-24 h-24 mb-2 text-5xl bg-gray-700 rounded-full">
            {{ localInfo.name[0].toUpperCase() }}
          </div>
          <div class="mb-2 text-2xl">{{ localInfo.name }}</div>
          <div class="mb-4 text-gray-200">
            <i class="fas" :class="getRegionFaGlobeClass(localInfo.region)"></i>
            {{ localInfo.region }}
          </div>
          <router-link
            class="hover:no-underline"
            :to="{ name: 'search', query: { name: localInfo.name, region: localInfo.region, tag: localInfo.tag } }"
            ><div class="p-2 px-6 text-center transition-colors bg-gray-600 rounded-md hover:bg-gray-500">
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
        <div class="mt-4 text-gray-200 max-w-[220px]">Many more features are in active development</div>
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
