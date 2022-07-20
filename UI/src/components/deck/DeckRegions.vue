<template>
  <region-icon
    class=""
    v-for="(faction, index) in getFactionsFixed(props.deck)"
    :key="index"
    :faction="faction"
  ></region-icon>
</template>

<script setup>
import RegionIcon from "../image/IconRegion.vue"
import getFactions from "../../modules/getFactions"

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

const getFactionsFixed = (code) => {
  var factions = getFactions(code)
  if (props.fixedWidth) {
    // Add filler champ icons
    var fillerIcons = props.maxFactions - factions.length
    for (let i = 0; i < fillerIcons; i++) {
      factions.push(99)
    }
  }
  return factions
}

// console.log(props)
</script>

<style scoped>
.icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
