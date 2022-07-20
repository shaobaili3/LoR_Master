<template>
  <region-icon
    class=""
    v-for="(faction, index) in getFactions(props.deck)"
    :key="index"
    :faction="faction"
  ></region-icon>
</template>

<script setup>
import RegionIcon from "../image/IconRegion.vue"
// import { getFactions } from "../panels/PanelMeta.vue"
import getFactions from "../../modules/getFactions"

// import { defineProps } from "vue"
const props = defineProps({
  deck: {
    type: String,
    require: true,
  },
  maxFactions: {
    type: Number,
    default: 2,
  },
  fixedWidth: {
    type: Boolean,
    default: true,
  },
})

// console.log(props)
</script>

<style scoped>
.icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
