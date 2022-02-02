<template>
  <div>
    <li class="h-8 pl-2 bg-gray-700 rounded" v-if="type == TAG_TYPES.string">
      <span v-if="getCard">
        {{ getCard.name }}
      </span>
      <span v-if="!getCard">
        {{ content }}
      </span>
      <i class="p-2 cursor-pointer fas fa-times" @click="deleteTag"></i>
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

const emits = defineEmits(["delete"])

function deleteTag() {
  emits("delete", props.index)
}
</script>
