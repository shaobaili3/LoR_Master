<template>
  <div
    class="mr-2 rounded-lg px-4 transition-colors duration-150 hover:bg-gray-800"
    :class="{
      'bg-gray-800': expand && !hasFeature && !selfExpand,
      'h-[552px]': expand && !selfExpand,
      'h-[92px]': !expand && !selfExpand,
    }"
  >
    <meta-deck
      class="cursor-pointer"
      :code="recomended"
      :isFeature="hasFeature && this.group.feature.deck_code == recomended"
      :playNum="group.play_num"
      :playRate="group.play_rate"
      :winRate="group.win_rate"
      :players="group.players"
      :linkDetail="!noDetail"
      :isSummary="true"
      @click="onSelfExpand"
    ></meta-deck>
    <transition :name="selfExpand ? 'height' : ''">
      <div v-if="expand" class="pl-4" @click.stop>
        <div v-for="deck in group.decks" :key="deck.deck_code">
          <meta-deck
            :isFeature="
              hasFeature && this.group.feature.deck_code == deck.deck_code
            "
            :code="deck.deck_code"
            :playNum="deck.play_num"
            :playRate="deck.play_rate"
            :winRate="deck.win_rate"
          ></meta-deck>
        </div>
      </div>
    </transition>
    <transition v-if="selfExpand" name="height">
      <div v-if="!expand && hasFeature" class="pl-4">
        <meta-deck
          :isFeature="true"
          :code="this.group.feature.deck_code"
          :playNum="this.group.feature.play_num"
          :playRate="this.group.feature.play_rate"
          :winRate="this.group.feature.win_rate"
        ></meta-deck>
      </div>
    </transition>
  </div>
</template>

<script>
import MetaDeck from "../meta/MetaDeck.vue";
export default {
  components: { MetaDeck },
  props: {
    group: Object,
    noDetail: Boolean,
    selfExpand: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      selfExpanded: false,
    };
  },
  computed: {
    hasFeature() {
      return this.group && this.group.feature;
    },
    recomended() {
      if (!(this.group && this.group.decks)) return null;
      var highest = 0;
      var code = null;
      for (let deck of this.group.decks) {
        if (deck.win_rate > highest) {
          highest = deck.win_rate;
          code = deck.deck_code;
        }
      }
      return code;
    },
    expand() {
      return this.selfExpand ? this.selfExpanded : this.group?.expanded;
    },
  },
  methods: {
    onSelfExpand() {
      this.selfExpanded = !this.selfExpanded;
    },
  },
};
</script>

<style></style>
