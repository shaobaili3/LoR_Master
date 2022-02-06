<template>
  <div class="flex gap-2 py-2 pl-4 cursor-pointer group hover:bg-gray-600" @click="handleBookmarkClick">
    <div>{{ bookmark.name }}</div>

    <div v-if="leaderboardInfo && leaderboardInfo.rank != null" class="pl-4 text-gray-200">
      <i class="pr-2 text-sm fas fa-trophy"></i>{{ leaderboardInfo.rank + 1 }}
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
