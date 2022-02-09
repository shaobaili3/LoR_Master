<template>
  <div>
    <li class="flex h-8 items-center rounded bg-gray-700 pl-2" v-if="type == TAG_TYPES.string">
      <div class="flex gap-2" v-if="getCard">
        <ChampIcon
          v-if="getCard.supertype != '' || getCard.rarityRef == 'Champion'"
          class="block h-6 w-6 rounded-full border-[1px] border-zinc-200 bg-cover"
          :customClass="true"
          :code="getCard.cardCode"
        ></ChampIcon>
        {{ getCard.name }}
      </div>
      <div class="flex items-center gap-2" v-else-if="getFaction != null">
        <RegionIcon class="h-6 w-6" :faction="getFaction" :fixedSize="false"></RegionIcon>
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
import { defineProps, defineEmits, computed } from "vue"
import CardPreview from "../deck/CardPreview.vue"
import { useBaseStore } from "../../store/StoreBase"
import ChampIcon from "../image/ChampIcon.vue"

import { factionNames } from "../panels/PanelDeckCode.vue"
import RegionIcon from "../image/RegionIcon.vue"

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
  let factionID = Object.values(factionNames).findIndex((val) => val == props.content)
  return factionID
})

const emits = defineEmits(["delete"])

function deleteTag() {
  emits("delete", props.index)
}
</script>
