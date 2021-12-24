<template>
  <div>
    <div class="info group relative" :class="{ champion: isChampion }">
      <div class="w-full h-10 flex justify-around items-center">
        <div class="info-rank">{{ rank }}</div>
        <div class="info-name group-hover:invisible">{{ name }}</div>
        <div class="info-lp group-hover:invisible">{{ lp }}</div>
      </div>
      <div class="hidden absolute h-10 left-0 top-1/2 -translate-y-1/2 md:group-hover:flex w-full justify-end items-center">
        
        <div class="text-left w-[41%]">
          <div v-if="winRate">
            {{ $t("matches.winRate", { num: winRate }) }}
          </div>
          <div v-if="lastRankTime" class="text-sm opacity-70">
            {{ $t('leaderboard.lastRank') + ' ' + lastRank }}
          </div>
        </div>
        <div class=" scale-75" v-if="deck">
          <deck-preview
            :won="isChampion"
            @click.stop
            :deck="deck"
            :fixed-width="true"
          ></deck-preview>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue";
import { format, formatDistance } from "date-fns";
export default {
  components: { DeckPreview },
  props: {
    rank: Number,
    name: String,
    lp: Number,
    deck: String,
    winRate: Number,
    lastRankTime: String,
  },
  computed: {
    lastRank() {
      // return format(new Date(this.lastRankTime), "HH:mm | yyyy-MM-dd")
      return formatDistance(new Date(this.lastRankTime), new Date(), {
        addSuffix: true,
      });
    },
    isChampion() {
      return this.rank == 1;
    },
  },
};
</script>

<style>
.info {
  color: white;
  background-color: var(--col-dark-grey);
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