<template>
  <div
    class="cardContainer group relative mt-1"
    :class="{
      empty: card.count == 0,
      spell: card.typeRef == 'Spell',
      unit: card.typeRef == 'Unit',
      champ: card.typeRef == 'Champion',
      landmark: card.typeRef == 'Landmark',
      unknown: card.typeRef == 'Unkown',
      'mt-0 mb-1 overflow-hidden rounded': noPreview,
    }"
    :style="{ background: getCardPreviewBackgroundStyle() }"
    ref="container"
    @mouseenter="onMouseEnter"
    @mouseleave="onMouseLeave"
  >
    <div v-if="!noCost" class="cardContent cardCost max-w-[30px]">
      {{ card.cost }}
    </div>
    <div class="cardContent cardName">{{ card.name }}</div>
    <div v-if="card.count && card.count >= 0" class="cardContent cardCount">x{{ card.count }}</div>
    <div
      v-if="type === 'Unknown'"
      class="
        lab-secret
        pointer-events-none
        absolute
        top-0
        left-1/2
        z-10
        flex
        h-full
        w-full
        -translate-x-1/2
        transform
        items-center
        justify-center
        whitespace-nowrap
        bg-black
        px-4
        opacity-0
        transition-opacity
        group-hover:opacity-100
      "
    >
      {{ $t("str.labSecrets") }}
    </div>
    <div ref="image" class="pointer-events-none absolute z-50 aspect-[0.6640625] w-full opacity-0 transition-opacity">
      <card-image :code="code" :set="set"></card-image>
    </div>
  </div>
</template>

<script>
// Image from mobalytics | 220x40
// https://cdn-lor.mobalytics.gg/production/images/cards-preview/01DE029.webp

import axios from "axios"
import CardImage from "../image/CardImage.vue"

import { computePosition, flip } from "@floating-ui/dom"

const requestStatusWaitTime = 1000 //ms
var lastStatusRequestTime

export default {
  components: { CardImage },
  mounted() {
    if (!this.name && this.code) {
      var card = this.sets.find((card) => card.cardCode == this.code)

      var typeRef = ""
      if (card.supertype != "" || card.rarityRef == "Champion") {
        typeRef = "Champion"
      } else if (card.spellSpeedRef != "") {
        typeRef = "Spell"
      } else if (card.keywordRefs && card.keywordRefs.includes("LandmarkVisualOnly")) {
        typeRef = "Landmark"
      } else {
        typeRef = "Unit"
      }

      // cards.push({
      //     code: cardCode,
      //     name: card.name,
      //     count: cardCount,
      //     baseCount: baseCount,
      //     cost: card.cost,
      //     type: card.type,
      //     typeRef: typeRef,
      //     supertype: card.supertype,
      //     set: card.set
      // })

      this.card.name = card.name
      this.card.cost = card.cost
    }

    if (!this.$refs.container || !this.$refs.image) return
    computePosition(this.$refs.container, this.$refs.image, {
      placement: "bottom",
      middleware: [flip()],
    }).then(({ x, y, strategy }) => {
      this.$refs.image.style.left = `${x}px`
      this.$refs.image.style.top = `${y}px`
    })
  },
  data() {
    return {
      card: {
        name: this.name,
        count: this.count,
        cost: this.cost,
        type: this.type,
        typeRef: this.typeRef,

        supertype: this.supertype,
        set: this.set,
      },
    }
  },
  props: {
    code: {
      type: String,
      required: true,
    },
    name: String,
    count: {
      type: Number,
      default: -1,
    },
    cost: Number,
    type: String,
    typeRef: String,

    supertype: String,
    set: String,

    noPreview: {
      type: Boolean,
      default: false,
    },
    noCost: {
      type: Boolean,
      default: false,
    },
  },
  computed: {},
  methods: {
    onMouseEnter() {
      if (!this.$refs.container || !this.$refs.image) return
      computePosition(this.$refs.container, this.$refs.image, {
        placement: "bottom",
        middleware: [flip()],
      }).then(({ x, y, strategy }) => {
        this.$refs.image.style.left = `${x}px`
        this.$refs.image.style.top = `${y}px`
        this.$refs.image.style.opacity = "1"
      })
    },
    onMouseLeave() {
      this.$refs.image.style.opacity = "0"
    },
    getCardPreviewBackgroundStyle() {
      // const champImageBaseUrl = 'https://raw.githubusercontent.com/painttist/lor-champ-icons/master/images/cards/cropped/';
      // const unkown = 'https://cdn-lor.mobalytics.gg/production/images/subscribe-banner.jpg'

      const grayOverlay = "linear-gradient(90deg, rgb(65, 65, 65) 30%, rgba(65, 65, 65, 0) 70%)"

      // const colored = 'linear-gradient(94deg, rgba(73,213,245,1) 44%, rgba(167,79,255,1) 90%)'
      const colored2 = "linear-gradient(120deg, rgba(19,28,69,1) 10%, rgba(73,213,245,1) 50%, rgba(167,79,255,1) 90%)"
      if (this.typeRef === "Unknown") {
        return `${colored2}`
      }

      const cardPreviewUrlBase = "https://cdn-lor.mobalytics.gg/production/images/cards-preview/"

      // const gradient = "linear-gradient(90deg, rgb(191, 176, 131) 30%, rgba(191, 176, 131, 0) 70%),"
      var gradient
      if (this.typeRef == "Champion") {
        gradient = "linear-gradient(90deg, var(--col-darker-gold) 30%, rgba(158, 114, 18, 0) 70%),"
      } else {
        gradient = `${grayOverlay},`
      }

      return gradient + "url(" + cardPreviewUrlBase + this.code + ".webp) right top no-repeat"
    },
  },
}
</script>

<style scoped>
.lab-secret {
  background: linear-gradient(
    120deg,
    rgba(0, 20, 20, 1) 14%,
    rgba(255, 154, 38, 1) 14%,
    rgba(255, 154, 38, 1) 23%,
    rgba(0, 20, 20, 1) 23%,
    rgba(0, 20, 20, 1) 42%,
    rgba(255, 154, 38, 1) 42%,
    rgba(250, 155, 43, 1) 53%,
    rgba(0, 20, 20, 1) 53%,
    rgba(0, 20, 20, 1) 72%,
    rgba(255, 154, 38, 1) 72%,
    rgba(248, 156, 46, 1) 81%,
    rgba(0, 20, 20, 1) 81%
  );
  /* background: linear-gradient(120deg, rgba(0,0,0,1) 14%, rgba(255,154,38,1) 14%, rgba(240,159,55,1) 23%, rgba(0,0,0,1) 23%, rgba(0,0,0,1) 72%, rgba(186,117,35,1) 72%, rgba(248,156,46,1) 81%, rgba(0,0,0,1) 81%); */
}
.cardContainer {
  max-width: 320px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  /* border-radius: 4px; */
}

.cardContainer:hover .cardDisplay,
.cardContainer:focus .cardDisplay {
  /* display: block; */
  /* visibility: initial; */
  /* position: relative; */
  opacity: 1;
}

.cardContainer.empty .cardCount {
  opacity: 0.5;
}

.cardDisplay {
  /* content: ""; */
  /* display: none; */
  /* visibility: hidden; */
  opacity: 0;
  position: absolute;
  top: 0;
  left: 0;

  pointer-events: none;
  @apply transition-opacity;

  width: 100%;
  height: auto;
  /* width: auto; */
  /* height: 100px; */
  /* background: white; */

  /* filter: drop-shadow(3px 3px 2px rgba(43, 38, 27, 0.6)); */

  z-index: 10;

  transition: opacity 0.15s cubic-bezier(0.075, 0.82, 0.165, 1);

  /* background-size: contain; */
}

.cardContent {
  flex: 1 0;
  padding: 8px 3px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 34px;
  max-height: 15.5vw;
  box-sizing: border-box;
  font-size: clamp(12px, 8vw, 15px);
}

.cardCost {
  background: var(--col-blue-light-grey);
  /* background: var(--col-dark-gold); */
  /* color: var(--col-dark-grey); */
  /* width: 50%; */
  /* height: 70%; */
  /* padding: 5px; */
  /* border-radius: 50px 0px 0px 50px; */
  border-radius: 0px 8px 8px 0px;
  /* border-radius: 20px; */
}

.cardName {
  flex: 8 0;
  justify-content: flex-start;
  /* padding: 9px 2px 9px 6px; */
  padding-left: 6px;
  text-shadow: rgb(0 0 0) 0px 1px 3px;
  box-sizing: border-box;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.cardCount {
  /* padding: 0px; */
  background: var(--col-light-grey);
}

.champ .cardCost {
  /* color: black; */
  background: var(--col-mid-gold);
}

.champ .cardCount {
  /* padding: 0px; */
  background: var(--col-mid-gold);
}

:not(.spell) + .spell,
:not(.unit) + .unit,
:not(.landmark) + .landmark {
  position: relative;
  margin-top: 12px;
}

:not(.spell) + .spell::before,
:not(.unit) + .unit::before,
:not(.landmark) + .landmark::before {
  content: "";
  /* display: block; */
  position: absolute;
  top: -6px;
  height: 1px;
  width: 100%;
  padding: 0px 5px;
  box-sizing: border-box;
  background: var(--col-lighter-grey);
  background-clip: content-box;
  /* margin-top: 4px; */
  /* padding-top: 10px; */
  /* border-top: 1px solid white; */
  /* background-origin: content-box; */
}
</style>
