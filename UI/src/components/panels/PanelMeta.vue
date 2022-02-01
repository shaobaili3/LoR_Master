<template>
  <div class="flex justify-center h-full overflow-y-auto">
    <div class="max-w-4xl flex-1 w-0">
      <div class="flex flex-col h-full px-2 sm:px-0">
        <p class="title text-3xl text-left pb-5 pt-3">{{ $t("str.meta") }}</p>

        <div v-if="store.isMetaLoading" class="text-2xl pb-5">
          <i class="fas fa-circle-notch fa-spin"></i>
          {{ $t("str.loading") }}
        </div>

        <!-- <p v-if="metaGroups" class="sub-title text-left pb-2">{{$t("matches.games", {num: totalGames})}}</p> -->
        <div v-if="store.metaGroups" class="flex-1 h-0 ">
          <div class="py-1 pb-5" v-for="group in store.metaGroups" :key="group._id">
            <meta-group :group="group"></meta-group>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import MetaGroup from "../meta/MetaGroup.vue"

import { useMetaStore } from "../../store/StoreMeta"

import { ref, onMounted } from "vue"

const store = useMetaStore()

const fetchMetaGroups = store.fetchMetaGroups

onMounted(() => {
  fetchMetaGroups()
})
</script>
