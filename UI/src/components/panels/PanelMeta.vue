<template>
  <div class="main-content-container">
    <div class="mb-32">
      <p class="title text-3xl text-left pb-5 pt-3 sticky-top">{{ $t("str.meta") }}</p>

      <div v-if="store.isMetaLoading" class="text-2xl pb-5">
        <i class="fas fa-circle-notch fa-spin"></i>
        {{ $t("str.loading") }}
      </div>

      <!-- <p v-if="metaGroups" class="sub-title text-left pb-2">{{$t("matches.games", {num: totalGames})}}</p> -->
      <div v-if="store.metaGroups">
        <div class="py-1" v-for="group in store.metaGroups" :key="group._id">
          <meta-group :group="group"></meta-group>
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
