<template>
  <div v-if="deckCode" class="mb-4 flex flex-col items-center justify-center sm:mb-2 sm:flex-row">
    <deck-preview
      class="mr-2 gap-1 py-2 px-3 text-base transition-colors hover:bg-gray-700"
      :fixedWidth="true"
      :deck="deckCode"
    ></deck-preview>
    <div class="flex-col gap-2 text-center sm:flex sm:gap-0 sm:text-left">
      <!-- Summary -->
      <p class="text-sm text-gray-200">
        {{ $t("matches.games", { num: matchup.match_num }) }}
      </p>
      <p class="text-lg" :style="{ color: winRateToColor(matchup.win_rate) }">
        {{
          $t("matches.winRate", {
            num: (matchup.win_rate * 100).toFixed(2),
          })
        }}
      </p>
    </div>
  </div>
</template>

<script>
import { useMetaStore } from "../../store/StoreMeta"
import { mapState } from "pinia"
import DeckPreview from "../deck/DeckPreview.vue"
import { winRateToColor } from "../../modules/utils/colorUtils"

export default {
  components: { DeckPreview },
  props: ["matchup"],
  computed: {
    ...mapState(useMetaStore, ["metaGroups", "isLoading"]),
    deckCode() {
      let decksInfo = this.metaGroups.find((group) => group._id == this.matchup._id)
      if (decksInfo && decksInfo.decks) {
        return decksInfo.decks.reduce(
          (highest, deck) => {
            if (deck.win_rate > highest.win_rate) {
              return deck
            }
            return highest
          },
          { deck_code: null, win_rate: 0 }
        ).deck_code
      }
      return null
    },
  },
  methods: {
    winRateToColor: winRateToColor,
  },
}
</script>
