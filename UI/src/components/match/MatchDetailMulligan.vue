<template>
  <div class="mulligan">
    <!-- <p class="title-text">Mulligan</p> -->
    <div class="images-contaienr">
      <div class="card-container" v-for="(card, index) in startHandFiltered" :key="index">
        <i v-if="card.kept" class="indicator fas fa-check"></i>
        <i v-if="!card.kept" class="indicator fas fa-sync-alt"></i>
        <image-card class="img" :code="card.CardCode"></image-card>
      </div>
      <div class="arrow">
        <i class="fas fa-arrow-right"></i>
      </div>
      <div
        class="card-container"
        v-for="(card, index) in endHandFiltered"
        :class="{ kept: card.kept }"
        :key="index"
      >
        <i v-if="card.kept" class="indicator fas fa-check"></i>
        <i v-if="!card.kept" class="indicator fas fa-plus"></i>
        <image-card class="img" :code="card.CardCode"></image-card>
      </div>
    </div>
  </div>
</template>

<script>
import ImageCard from "../image/ImageCard.vue"

export default {
  components: {
    ImageCard,
  },
  mounted() {},
  data() {
    return {}
  },
  props: {
    startHand: Array,
    endHand: Array,
  },
  computed: {
    startHandFiltered() {
      return this.startHand
        .filter((card) => {
          return card.CardCode !== "face" && card.LocalPlayer
        })
        .map((card) => {
          card.kept = this.endHand.find((c) => {
            return c.CardID == card.CardID
          })
          return card
        })
    },
    endHandFiltered() {
      return this.endHand
        .filter((card) => {
          return card.CardCode !== "face" && card.LocalPlayer
        })
        .map((card) => {
          card.kept = this.startHand.find((c) => {
            return c.CardID == card.CardID
          })
          return card
        })
    },
  },
  methods: {},
}
</script>

<style lang="scss" scoped>
.mulligan {
  // z-index: 8;

  .title-text {
    text-align: left;
    font-size: 0.8em;
  }
  .images-contaienr {
    // height: 100px;
    width: 100%;

    padding: 0px 5px;
    box-sizing: border-box;

    display: flex;
    justify-content: space-between;
    align-items: center;

    margin-top: 5px;

    .card-container {
      // height: 10%;
      display: flex;

      align-items: center;
      position: relative;

      width: 11%;
      min-height: 90px;

      &:hover {
        .img {
          position: absolute;
          width: 170px;
          // height: 200px;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          z-index: 14;
        }
      }

      .indicator {
        // background: var(--col-background);
        // color: var(--col-gold);
        // padding: 0.5em;
        // font-size: 0.8em;
        // border-radius: 50px;

        color: white;
        opacity: 0.9;
        text-shadow: 2px 0 5px #000;

        position: absolute;
        bottom: 0px;
        right: 0px;
      }

      .img {
        pointer-events: none;
        width: 100%;
        height: auto;
      }
    }
  }
}
</style>
