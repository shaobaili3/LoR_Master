<template>
  <div class="square relative block w-[2.5em]">
    <img
      class="absolute top-0 left-0 h-full w-full rounded-full object-contain"
      :class="{
        'border-2 border-zinc-200': this.code,
        'border-0': !this.code,
      }"
      :src="getChampionImgUrl"
    />
    <div
      v-if="count && count != 3"
      class="absolute -top-[0.25em] -right-[0.35em] flex h-[1.6em] w-[1.6em] items-center justify-center rounded-full bg-gray-800 text-[0.6em] text-white"
    >
      {{ count }}
    </div>
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
    code: String,
    count: Number,
    customClass: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    getChampionImgUrl() {
      if (!this.code) {
        return require("../../assets/images/cards/cropped/no-champion.png")
      }
      // const champImageBaseUrl = 'https://raw.githubusercontent.com/painttist/lor-champ-icons/master/images/cards/cropped/';
      // const champImageBaseUrl = 'https://painttist.github.io/lor-champ-icons/images/cards/cropped/';
      // return "url('" + champImageBaseUrl + code + "-cropped.png')"

      // -- Local
      // - v1
      var fileName = this.code + "-cropped.png"
      // return "url('" + cardImages[fileName] + "')"

      // - v2
      // return "url(" + require("../../assets/images/cards/cropped/" + fileName) + ")"
      return require("../../assets/images/cards/cropped/" + fileName)
    },
  },
  methods: {},
}
</script>

<style lang="scss" scoped>
.square::after {
  content: "";
  display: block;
  padding-bottom: 100%;
}
</style>
