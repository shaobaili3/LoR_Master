<template>
  <div class="flex items-center gap-2 py-2 pl-4 cursor-pointer group hover:bg-gray-600 whitespace-nowrap" @click="handleBookmarkClick">
    <div class="flex-shrink pr-2 overflow-hidden text-ellipsis">{{ bookmark.name }}</div>

    <div class="text-sm text-gray-200" v-if="bookmark.region">
      <i class="pr-1 fas" :class="getRegionFaGlobeClass(bookmark.region)"></i>{{ bookmark.region }}
    </div>

    <div class="text-sm text-gray-200" v-if="leaderboardInfo && leaderboardInfo.rank != null">
      <i class="pr-1 fas fa-trophy"></i>{{ leaderboardInfo.rank + 1 }}
    </div>
    <div class="flex-1 w-0"></div>
    <button
      class="invisible pl-2 pr-4 cursor-pointer group-hover:hover:text-white group-hover:visible group-hover:text-gray-300"
      @click.stop="onDelete"
    >
      <i class="fas fa-trash-alt"></i>
    </button>
  </div>
</template>

<script>
export const getRegionFaGlobeClass = (regionShort) => {
  if (regionShort == "APAC") return "fa-globe-asia"
  else if (regionShort == "EU") return "fa-globe-europe"
  return "fa-globe-americas"
}
</script>

<script setup>
import { defineProps, computed } from "vue"
import { getLeaderboardFromPlayer } from "../match/PlayerMatches.vue"

import { router } from "../../pages/home/main"
import { useBookmarkStore } from "../../store/StoreBookmark"

const props = defineProps({
  index: Number,
  bookmark: Object,
})

function onDelete() {
  const bookmarkStore = useBookmarkStore()
  bookmarkStore.deleteBookmark(props.index)
}

function handleBookmarkClick() {
  router.push({
    path: "/search",
    query: { name: props.bookmark.name, tag: props.bookmark.tag, region: props.bookmark.region },
  })
}

const leaderboardInfo = computed(() => {
  return getLeaderboardFromPlayer(props.bookmark.region, props.bookmark.name, props.bookmark.tag)
})
</script>
