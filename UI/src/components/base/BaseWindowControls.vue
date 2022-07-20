<template>
  <!-- Top Bar BG -->
  <div class="fixed left-0 top-0 z-[2] h-[45px] w-full bg-gray-900"></div>
  <!-- Might need to add some margin for resize capabilities -->
  <div
    class="can-drag fixed top-0 left-0 z-[100] mt-[2px] flex h-[43px] w-full items-center justify-end bg-gray-900"
  >
    <!-- Back Button -->
    <div
      v-if="IS_ELECTRON && titleType != 'match'"
      @click="$router.go(-1)"
      class="route-back no-drag z-[110] ml-[90px] mt-2 cursor-pointer py-2 px-3 text-white"
    >
      <i class="fas fa-chevron-left"></i> {{ $t("str.back") }}
    </div>
    <!-- Title -->
    <div class="absolute left-3 text-white" :title="title" v-if="titleType == 'window'">
      {{ title }}
    </div>
    <!-- In Game Title -->
    <div
      class="left-0 overflow-hidden text-ellipsis whitespace-nowrap pl-2 text-sm text-white 2xs:pl-4 2xs:text-base"
      v-if="titleType == 'match'"
    >
      {{ playerName }}
    </div>
    <!-- Player Info -->
    <div
      class="left-0 ml-1 whitespace-nowrap text-xs text-gray-200 2xs:ml-2 2xs:text-sm"
      v-if="titleType == 'match' && playerRank"
    >
      <i class="fas fa-trophy"></i> {{ playerRank }}
      <span class="pl-1 2xs:pl-2"><i class="pr-1 font-black 2xs:pr-2">LP</i>{{ playerLP }}</span>
    </div>
    <!-- Middle Expansion -->
    <div class="w-0 flex-1"></div>
    <!-- Right Buttons -->
    <div
      v-if="canMin"
      class="no-drag flex h-full w-10 min-w-[30px] cursor-pointer items-center justify-center text-sm text-gold-300 hover:text-white 2xs:text-base"
      @click="minApp()"
    >
      <span><i class="fas fa-minus"></i></span>
    </div>
    <div
      v-if="canShrink"
      class="no-drag flex h-full w-10 min-w-[30px] cursor-pointer items-center justify-center text-sm text-gold-300 hover:text-white 2xs:text-base"
      @click="shrinkToggle()"
    >
      <span v-if="!isWindowMin"><i class="fas fa-compress-alt"></i></span>
      <span v-if="isWindowMin"><i class="fas fa-expand-alt"></i></span>
    </div>
    <div
      v-if="canClose"
      class="no-drag flex h-full w-10 min-w-[30px] cursor-pointer items-center justify-center text-sm text-gold-300 hover:text-white 2xs:text-base"
      @click="closeApp()"
    >
      <span><i class="fas fa-times"></i></span>
    </div>

    <!-- <router-link to="/" class="menu-item"> -->
    <!-- <span><i class="fa fa-home"></i></span> -->
    <!-- </router-link> -->
    <!-- <router-link to="/leaderboard" class="menu-item"> -->
    <!-- <span><i class="fa fa-trophy"></i></span> -->
    <!-- </router-link> -->
    <!-- <router-link to="/profile" class="menu-item">
            <span><i class="fa fa-user"></i></span>
        </router-link> -->
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    playerName: String,
    playerRank: Number,
    titleType: String,
    playerLP: Number,
    canShrink: {
      type: Boolean,
      default: false,
    },
    canMin: {
      type: Boolean,
      default: true,
    },
    canClose: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      isWindowMin: false,
    }
  },
  mounted() {
    window.addEventListener("resize", this.checkIsMin)
  },
  unmounted() {
    window.removeEventListener("resize", this.checkIsMin)
  },
  computed: {
    playerInfoString() {
      return (
        this.playerName +
        (this.playerRank ? " Rank:" + this.playerRank : "") +
        (this.playerLP ? " LP:" + this.playerLP : "")
      )
    },
  },
  // components: {
  //   MainLayout
  // }
  methods: {
    shrinkToggle() {
      if (this.IS_ELECTRON) window.toggleShrinkWindow() // Defined in appsrc > preload.js
    },
    minApp() {
      if (this.IS_ELECTRON) window.minWindow() // Defined in appsrc > preload.js
      //   console.log("Closing App")
    },
    closeApp() {
      if (this.IS_ELECTRON) window.hideWindow()
    },
    checkIsMin() {
      if (window.isMin) this.isWindowMin = window.isMin()
    },
  },
}
</script>

<style lang="scss" scoped>
.no-drag {
  -webkit-app-region: no-drag;
}

.can-drag {
  -webkit-app-region: drag;
}
</style>
