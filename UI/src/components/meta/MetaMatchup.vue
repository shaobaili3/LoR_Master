<template>
  <div class="block lg:flex justify-around" v-if="matchups">
    <div class="block mb-4">
      <div class="text-center py-4">Good against</div>
      <div v-for="matchup in good" :key="matchup._id">
        <meta-matchup-item :matchup="matchup"></meta-matchup-item>
      </div>
    </div>

    <div class="block">
      <div class="text-center py-4">Bad against</div>
      <div v-for="matchup in bad" :key="matchup._id">
        <meta-matchup-item :matchup="matchup"></meta-matchup-item>
      </div>
    </div>
  </div>
</template>

<script>
import MetaMatchupItem from "./MetaMatchupItem.vue";
export default {
  components: { MetaMatchupItem },
  mounted() {},
  props: ["matchups"],
  computed: {
    good() {
      return this.matchups?.filter((matchup) => matchup.win_rate >= 0.5).sort((a, b) => a.win_rate < b.win_rate ? 1 : -1);
    },
    bad() {
      return this.matchups?.filter((matchup) => matchup.win_rate < 0.5).sort((a, b) => a.win_rate > b.win_rate ? 1 : -1);
    },
  },
};
</script>