<template>
  <div
    class="aspect-square h-[90%] rounded-full border-transparent bg-cover bg-center bg-no-repeat"
    :style="{ backgroundImage: getRegionImgUrl }"
  >
    <img
      class="invisible aspect-square h-full"
      src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    />
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
    fixedSize: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    getRegionImgUrl() {
      if (this.faction == -1) {
        return "none"
      }
      // Remote
      // const regionImageBaseUrl = 'https://painttist.github.io/lor-champ-icons/images/regions/';
      // return "url(" + regionImageBaseUrl + regionID + ".svg)";

      // Local
      return "url(" + require("../../assets/images/regions/" + this.faction + ".svg") + ")"
    },
  },
  methods: {},
}
</script>
