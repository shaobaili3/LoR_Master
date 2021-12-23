<template>
  <div>
    <p class="text-3xl text-left pb-5 pt-3 sticky-top">{{title}}</p>
    <p class="text-left">{{error}}</p>
    <div class=" block md:flex">
      <div class=" w-full md:w-1/4 flex justify-center md:justify-start">
        <deck-detail class="max-w-[250px]" :base-deck="code"></deck-detail>
      </div>
      <div class=" w-full md:w-3/4 px-4 text-left" v-if="deck">
        <div v-if="loadingStats" class="text-2xl">
          <span><i class="fas fa-circle-notch fa-spin"></i></span>
          <span class="pl-2">{{ $t("str.loading") }}</span>
        </div>
        <div v-if="keeps || swaps" class="pb-6">
          <div class="text-3xl pb-3" >Mulligan Guide</div>
          <div class=" block sm:flex w-full" >
            <div class=" w-full sm:w-1/2 " v-if="keeps">
              <div class="text-xl pb-2 ">Keep</div>
              <div class="flex w-full items-center" v-for="keep in keeps" :key="keep.code">
                <card-preview class="flex-1" :code="keep.code"></card-preview>
                <div class="px-4">+{{keep.rate}}%</div>
              </div>
            </div>
            <div class=" w-full sm:w-1/2 " v-if="swaps">
              <div class="text-xl pb-2 ">Mulligan</div>
                <div class="flex w-full items-center" v-for="swap in swaps" :key="swap.code">
                <card-preview class="flex-1" :code="swap.code"></card-preview>
                <div class="px-4">-{{swap.rate}}%</div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!loadingStats">
          <div class="text-3xl pb-3" >Match Ups</div>
          <div class="text-xl pb-1">Strong Against</div>
          <p class="mb-4">voluptate tenetur deserunt obcaecati delectus vero aut quia, dolore dicta? Ab itaque nostrum cum animi ducimus architecto minima.</p>
          <div class="text-xl pb-1">Weak Against</div>
          <p class="mb-4">Lorem ipsum dolor sit amet consectetur adipisicing elit. Exercitationem quas, provident nihil, voluptate tenetur da.</p>
        </div>
        
      </div>
    </div>
    
  </div>
</template>

<script>
import DeckEncoder from '../../modules/runeterra/DeckEncoder'
import CardPreview from '../deck/CardPreview.vue';
import DeckDetail from '../deck/DeckDetail.vue'

export default {
    mounted() {
        console.log("PANEL CODE:", this.code);
        this.processDeck();
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
    methods: {
        processDeck() {
            try {
                let deck = DeckEncoder.decode(this.code);
                this.deck = deck
                this.requestDeckStats()
                let champNames = deck.reduce((names, card) => {
                    let info = this.sets.find(info => info.cardCode == card.code);
                    if (info.rarityRef === "Champion") {
                        names.push(info.name);
                    }
                    return names;
                }, []);
                this.title = champNames.join(" ");
            }
            catch (err) {
                console.log(err);
                this.error = this.$t("str.invalidDeck");
            }
        },
        async requestDeckStats() {
          this.loadingStats = true
          await new Promise(resolve => setTimeout(resolve, 2000));
          this.processDeckStats({})
          
        },
        processDeckStats(data) {
          this.loadingStats = false
          this.keeps = [
            {code: this.deck[0].code, rate: 3},
            {code: this.deck[1].code, rate: 2},
            {code: this.deck[2].code, rate: 1.3},
            {code: this.deck[3].code, rate: 0.8}
          ]
          this.swaps = [
            {code: this.deck[4].code, rate: 3.1},
            {code: this.deck[5].code, rate: 2.1},
            {code: this.deck[6].code, rate: 1.9},
            {code: this.deck[7].code, rate: 0.9}
          ]
        }

    },
    components: { DeckDetail, CardPreview }
}
</script>