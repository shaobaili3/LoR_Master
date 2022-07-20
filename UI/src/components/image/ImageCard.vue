<template>
  <img class="object-contain drop-shadow-dark" :src="getCardDisplayUrl" alt="" />
</template>

<script setup>
import { computed } from "vue"
import { useBaseStore } from "../../store/StoreBase"

const cardDisplayUrlBase = "https://dd.b.pvp.net/latest/"

const props = defineProps({
  code: String,
  set: String,
})

const getCardDisplayUrl = computed(() => {
  if (!props.code) {
    return ""
  }

  var setString = props.set
  const baseStore = useBaseStore()
  if (!setString) {
    var card = baseStore.sets.find((card) => card.cardCode == this.code)
    if (!card) {
      return ""
    }
    setString = card.set
  }

  return (
    cardDisplayUrlBase +
    setString.toLowerCase() +
    "/" +
    (baseStore.locale == "zh_cn" ? "zh_tw" : baseStore.locale) +
    "/img/cards/" +
    props.code +
    ".png"
  )
})
</script>

<style></style>
