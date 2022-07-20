<template>
  <div>
    <li
      class="flex h-8 items-center rounded bg-gray-700 pl-2 transition-colors hover:bg-gray-600"
      v-if="type == TAG_TYPES.string"
    >
      <div class="flex gap-2" v-if="getCard">
        <IconChampion
          v-if="getCard.supertype != '' || getCard.rarityRef == 'Champion'"
          class="block h-6 w-[1.5em] rounded-full bg-cover"
          :customClass="true"
          :code="getCard.cardCode"
        ></IconChampion>
        {{ getCard.name }}
      </div>
      <div class="flex items-center gap-2" v-else-if="getFaction != null">
        <IconRegion class="h-6 w-6" :faction="getFaction" :fixedSize="false"></IconRegion>
        {{ content }}
      </div>
      <div v-else-if="!getCard">
        {{ content }}
      </div>
      <i class="fas fa-times cursor-pointer p-2" @click="deleteTag"></i>
    </li>
  </div>
</template>

<script>
export const TAG_TYPES = {
  string: 0,
  card: 1,
  champion: 2,
  region: 3,
}

export default {}
</script>

<script setup>
import { defineEmits, computed } from "vue"
import CardPreview from "../deck/CardPreview.vue"
import { useBaseStore } from "../../store/StoreBase"

import { factionNames } from "../../modules/constants.js"
import RegionIcon from "../image/IconRegion.vue"
import IconChampion from "../image/IconChampion.vue"
import IconRegion from "../image/IconRegion.vue"

const baseStore = useBaseStore()

const props = defineProps({
  content: String,
  type: TAG_TYPES,
  tags: Object,
  index: Number,
})

const getCard = computed(() => {
  if (props.content in baseStore.sets_en) {
    let card = baseStore.sets.find((card) => card.cardCode == props.content)
    return card
  }
  return null
})

const getFaction = computed(() => {
  var key = Object.keys(factionNames).find((key) => factionNames[key] == props.content)
  let factionID = key ? parseInt(key) : null
  return factionID
})

const emits = defineEmits(["delete"])

function deleteTag() {
  emits("delete", props.index)
}
</script>
