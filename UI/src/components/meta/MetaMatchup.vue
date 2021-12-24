<template>
  <div v-if="matchups">
    <div v-for="matchup in matchups" :key="matchup._id">
      <div class="flex items-center">
        <deck-preview
          class="max-w-[200px] md:mr-2"
          :fixedWidth="true"
          :deck="'CQCACAYGCEBAEBQYDIBAKBQFBMDQKCQEDIUDDJQBXQA4MAIBAECQUAICAECAMCQBAUFKOAI'"
        ></deck-preview>
        <div class="block sm:flex gap-3">
          <!-- Summary -->
          <p>{{$t("matches.games", {num: matchup.match_num})}}</p>
          <p>{{$t('matches.winRate', {num: (matchup.win_rate * 100).toFixed(2)})}}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue";
export default {
  components: { DeckPreview },
  props: ["matchups"],
};
</script>