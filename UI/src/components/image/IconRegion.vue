<template>
  <div class="square relative block w-[2.35em]">
    <!-- Padding for some slight visual fix -->
    <!-- :class="{ 'py-[1px] pr-[2px] opacity-20': faction == 99 }" -->
    <img class="absolute top-0 left-0 h-full w-full object-contain" :src="getRegionImgUrl" />
  </div>
</template>

<script>
export default {
  props: {
    faction: Number,
    colored: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    getRegionImgUrl() {
      if (this.faction == 99 || this.faction >= 12) {
        return require("../../assets/images/regions/no-region2.png")
      }

      // Remote
      // const regionImageBaseUrl = 'https://painttist.github.io/lor-champ-icons/images/regions/';
      // return "url(" + regionImageBaseUrl + regionID + ".svg)";

      // Local
      return require("../../assets/images/regions/" + this.faction + ".svg")
    },
  },
}
</script>

<style scoped>
.square::after {
  content: "";
  display: block;
  padding-bottom: 100%;
}
</style>
