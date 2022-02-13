<template>
  <div class="relative block h-full w-auto">
    <!-- Padding for some slight visual fix -->
    <!-- :class="{ 'py-[1px] pr-[2px] opacity-20': faction == 99 }" -->
    <img class="aspect-square max-h-full rounded-full p-0.5" :src="getRegionImgUrl" />
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {}
  },
  mounted() {},
  props: {
    faction: Number,
    colored: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    getRegionImgUrl() {
      if (this.faction == 99) {
        return require("../../assets/images/regions/no-region.png")
      }
      // Remote
      // const regionImageBaseUrl = 'https://painttist.github.io/lor-champ-icons/images/regions/';
      // return "url(" + regionImageBaseUrl + regionID + ".svg)";

      // Local
      return require("../../assets/images/regions/" + this.faction + ".svg")
    },
  },
  methods: {},
}
</script>
