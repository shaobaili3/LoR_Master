<template>
  <div
    class="group flex cursor-pointer items-center gap-2 whitespace-nowrap py-2 pl-4 transition-colors hover:bg-gray-600"
    @click="handleBookmarkClick"
  >
    <div class="flex-shrink overflow-hidden text-ellipsis pr-2">
      {{ bookmark.name }}
    </div>

    <div class="text-sm text-gray-200" v-if="bookmark.region">
      <i class="fas pr-1" :class="getRegionFaGlobeClass(bookmark.region)"></i>{{ bookmark.region }}
    </div>

    <div class="text-sm text-gray-200" v-if="leaderboardInfo && leaderboardInfo.rank != null">
      <i class="fas fa-trophy pr-1"></i>{{ leaderboardInfo.rank + 1 }}
    </div>
    <div class="w-0 flex-1"></div>
    <button
      class="cursor-pointer pl-2 pr-4 text-gray-300 opacity-0 transition-opacity hover:text-white group-hover:opacity-100"
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
import { computed } from "vue"
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
    query: {
      name: props.bookmark.name,
      tag: props.bookmark.tag,
      region: props.bookmark.region,
    },
  })
}

const leaderboardInfo = computed(() => {
  return getLeaderboardFromPlayer(props.bookmark.region, props.bookmark.name, props.bookmark.tag)
})
</script>
