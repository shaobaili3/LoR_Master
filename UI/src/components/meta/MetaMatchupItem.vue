<template>
  <div class="flex flex-col items-center justify-center mb-4 sm:mb-2 sm:flex-row">
    <deck-preview class="max-w-[200px] md:mr-2" :fixedWidth="true" :deck="deckCode"></deck-preview>
    <div class="flex-col gap-2 text-center sm:text-left sm:flex sm:gap-0">
      <!-- Summary -->
      <p class="text-sm text-gray-200">
        {{ $t("matches.games", { num: matchup.match_num }) }}
      </p>
      <p class="text-lg">
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
}
</script>
