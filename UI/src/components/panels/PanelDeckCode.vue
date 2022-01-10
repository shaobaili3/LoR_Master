<template>
  <div>
    <p class="text-3xl text-left pb-5 pt-3 sticky-top">{{ title }}</p>
    <p class="text-left">{{ error }}</p>
    <div class="block md:flex">
      <div class="w-full md:w-1/4 flex justify-center md:justify-start">
        <deck-detail class="max-w-[250px]" :base-deck="code"></deck-detail>
      </div>
      <div class="w-full md:w-3/4 px-4 text-left" v-if="deck">
        <!-- Loading -->

        <div v-if="loadingStats || isLoading" class="text-2xl pb-4">
          <span><i class="fas fa-circle-notch fa-spin"></i></span>
          <span class="pl-2">{{ $t("str.loading") }}</span>
        </div>

        <div v-if="noInfo">
          <div class="text-3xl pb-3">{{ $t('str.noDetail') }}</div>
        </div>

        <!-- Meta -->

        <div v-if="!isLoading && deckStats" class="pb-4">
          <div class="text-3xl pb-3">{{ $t('deckCode.archetypeStats') }}</div>
          <meta-group :no-detail="true" :group="deckStats"></meta-group>
          <div class="text-3xl pb-3">{{ $t('deckCode.archetypeMatchups') }}</div>
          <meta-matchup :matchups="deckStats.matchup"></meta-matchup>
        </div>

        <!-- Mulligan -->

        <div v-if="keeps || swaps" class="pb-6">
          <div class="text-3xl pb-3">{{ $t('deckCode.mulliganGuide') }}</div>
          <div class="block sm:flex w-full">
            <div class="w-full sm:w-1/2" v-if="keeps">
              <div class="text-xl pb-2">{{ $t('deckCode.keep') }}</div>
              <div
                class="flex w-full items-center"
                v-for="keep in keeps"
                :key="keep.code"
              >
                <card-preview class="flex-1" :code="keep.code"></card-preview>
                <div class="px-4">+{{ keep.rate }}%</div>
              </div>
            </div>
            <div class="w-full sm:w-1/2" v-if="swaps">
              <div class="text-xl pb-2">{{ $t('deckCode.mulligan') }}</div>
              <div
                class="flex w-full items-center"
                v-for="swap in swaps"
                :key="swap.code"
              >
                <card-preview class="flex-1" :code="swap.code"></card-preview>
                <div class="px-4">-{{ swap.rate }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const regionRefID = {
  Demacia: 0,
  Freljord: 1,
  Ionia: 2,
  Noxus: 3,
  PiltoverZaun: 4,
  ShadowIsles: 5,
  Bilgewater: 6,
  Shurima: 7,
  Targon: 9,
  BandleCity: 10,
};

const regionNames = {
  0: "faction_Demacia_Name",
  1: "faction_Freljord_Name",
  2: "faction_Ionia_Name",
  3: "faction_Noxus_Name",
  4: "faction_Piltover_Name",
  5: "faction_ShadowIsles_Name",
  6: "faction_Bilgewater_Name",
  7: "faction_Shurima_Name",
  9: "faction_MtTargon_Name",
  10: "faction_BandleCity_Name",
};

import DeckEncoder from "../../modules/runeterra/DeckEncoder";
import CardPreview from "../deck/CardPreview.vue";
import DeckDetail from "../deck/DeckDetail.vue";

import championCards from "../../assets/data/champion.js";

import { mapState, mapActions } from "vuex";
import MetaGroup from "../meta/MetaGroup.vue";
import MetaMatchup from "../meta/MetaMatchup.vue";

export default {
  mounted() {
    console.log("PANEL CODE:", this.code);
    this.processDeck();
    this.fetchMetaGroups();
  },
  props: ["code"],
  data() {
    return {
      error: "",
      title: "Deck Detail",
      deck: null,
      keeps: null,
      swaps: null,

      loadingStats: true,
    };
  },
  computed: {
    ...mapState("metaData", ["metaGroups", "isLoading"]),
    noInfo() {
      // Not loading and no information
      return (
        !(this.loadingStats || this.isLoading) &&
        !(this.keeps || this.swaps) &&
        !this.deckStats
      );
    },
    getDecodedDeck() {
      var deck = null;
      if (this.code) {
        try {
          deck = DeckEncoder.decode(this.code);
        } catch (error) {
          console.log(error);
          return null;
        }
      }
      return deck;
    },
    getFactions() {
      var cards = this.getDecodedDeck;
      if (!cards) return null;

      var factionIDs = [];
      for (var j in cards) {
        var cardCode = cards[j].code;
        var card = this.sets_en[cardCode];
        if (card) {
          if (card.regions && card.regions.length == 1) {
            // Only considers mono region cards
            var regionID = regionRefID[card.regionRefs[0]];

            if (factionIDs.indexOf(regionID) == -1) {
              factionIDs.push(regionID);
            }
          }
        }
      }
      return factionIDs;
    },
    getChamps() {
      var deck = this.getDecodedDeck;
      if (!deck) return null;

      var champs = [];
      for (var j in deck) {
        let cardCode = deck[j].code;
        if (championCards.champObj[cardCode] != null) {
          var card = this.sets_en[cardCode];
          if (card) {
            let champ = {
              count: deck[j].count,
              code: cardCode,
              name: card.name
            };
            champs.push(champ);
          }
        }
      }
      champs = champs.sort((a, b) => (a.count > b.count ? 1 : -1));
      return champs;
    },
    archetypeID() {
      var factionNames = this.getFactions.map((id) => regionNames[id]).sort();
      var champNames = this.getChamps.slice(0,2).map(champ => champ.name).sort();
      if (this.getChamps.length == 0) {
        champNames = ["No-Champion"];
      }
      var IDString = factionNames.join(" ") + " " + champNames.join(" ")
      return IDString;
    },
    deckStats() {
      if (this.metaGroups) {
        for (let group of this.metaGroups) {
          let stats = group.decks.find((deck) => {
            return deck.deck_code == this.code;
          });
          if (group._id == this.archetypeID) {
            let newGroup = { ...group };
            newGroup.feature = stats;
            return newGroup;
          }
        }
      }

      return null;
    },
  },
  methods: {
    ...mapActions("metaData", ["fetchMetaGroups"]),
    processDeck() {
      try {
        let deck = DeckEncoder.decode(this.code);
        this.deck = deck;
        this.requestDeckStats();
        let champNames = deck.reduce((names, card) => {
          let info = this.sets.find((info) => info.cardCode == card.code);
          if (info.rarityRef === "Champion") {
            names.push(info.name);
          }
          return names;
        }, []);
        this.title = champNames.join(" ");
      } catch (err) {
        console.log(err);
        this.error = this.$t("str.invalidDeck");
      }
    },

    async requestDeckStats() {
      // this.loadingStats = true;
      // await new Promise((resolve) => setTimeout(resolve, 2000));
      this.processDeckStats({});
    },
    processDeckStats(data) {
      this.loadingStats = false;
      // this.keeps = [
      //   { code: this.deck[0].code, rate: 3 },
      //   { code: this.deck[1].code, rate: 2 },
      //   { code: this.deck[2].code, rate: 1.3 },
      //   { code: this.deck[3].code, rate: 0.8 },
      // ];
      // this.swaps = [
      //   { code: this.deck[4].code, rate: 3.1 },
      //   { code: this.deck[5].code, rate: 2.1 },
      //   { code: this.deck[6].code, rate: 1.9 },
      //   { code: this.deck[7].code, rate: 0.9 },
      // ];
    },
  },
  components: { DeckDetail, CardPreview, MetaGroup, MetaMatchup },
};
</script>
