<template>
  <div class="grid grid-cols-12 items-center bg-gray-600 group hover:bg-gray-800 cursor-pointer group relative h-16">
    <div class="bg-gray-600 group-hover:bg-gray-800 z-[1]">{{ rank }}</div>
    <div class="col-span-4 sm:col-span-3 bg-gray-600 group-hover:bg-gray-800 z[1] overflow-hidden text-ellipsis">{{ name }}</div>
    <div class="col-span-2 sm:col-span-1">{{ lp }}</div>
    <div class="hidden sm:block sm:col-span-2">
      <div v-if="lastRankTime" class="text-sm text-white text-opacity-70">
        {{ lastRank }}
      </div>
    </div>
    <div class="hidden sm:block sm:col-span-2">
      <div v-if="winRate">
        {{ $t("matches.winRate", { num: winRate }) }}
      </div>
    </div>

    <div class="col-span-5 sm:col-span-3">
      <deck-preview v-if="deck" @click.stop :deck="deck" :fixed-width="true" :size="1"></deck-preview>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"
import { format, formatDistanceStrict } from "date-fns"

import { dateFNSLocales } from "../../assets/data/messages"

export default {
  components: { DeckPreview },
  props: {
    rank: String,
    name: String,
    lp: Number,
    deck: String,
    winRate: String,
    lastRankTime: String,
  },
  computed: {
    lastRank() {
      // return format(new Date(this.lastRankTime), "HH:mm | yyyy-MM-dd")
      return formatDistanceStrict(new Date(this.lastRankTime), new Date(), {
        addSuffix: true,
        locale: dateFNSLocales[this.$i18n.locale],
      })
    },
    isChampion() {
      return this.rank == 1
    },
  },
}
</script>

<style>
.info {
  color: white;
  width: 100%;
  padding: 5px 0px;
  margin: 0px 0px;
  align-items: center;
  justify-content: space-around;
  border-radius: 5px;

  cursor: pointer;
}

.info:hover {
  background-color: var(--col-light-grey);

  /* box-shadow: 0px 0px 10px 2px var(--col-gold); */
}

.info.champion {
  /* color: rgb(126, 15, 15); */
  /* background-color: var(--col-gold); */

  box-shadow: inset 0px 0px 0px 2px var(--col-gold);
}

.info.champion:hover {
  /* color: var(--col-background); */
  /* background-color: rgb(250, 200, 34); */
  background: linear-gradient(60deg, var(--col-dark-gold), var(--col-gold));
  box-shadow: none;
  /* box-shadow: 0px 0px 10px 2px var(--col-gold); */
  /* font-weight: 600; */
}

.info-rank {
  width: 9.6%;
  text-align: center;
}

.info-name {
  width: 53.8%;
  text-align: left;
}

.info-lp {
  width: 9.6%;
  text-align: center;
}

a {
  text-decoration: none;
}
</style>
