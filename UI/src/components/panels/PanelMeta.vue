<template>
  <div>
    <p class="title text-3xl text-left pb-5 pt-3 sticky-top">{{$t("str.meta")}}</p>
    
    <div v-if="isLoading" class="text-2xl pb-5">
      <i class="fas fa-circle-notch fa-spin"></i>
      {{ $t("str.loading") }}
    </div>
    
    <!-- <p v-if="metaGroups" class="sub-title text-left pb-2">{{$t("matches.games", {num: totalGames})}}</p> -->
    <div v-if="metaGroups">
      <div class="py-1" v-for="group in metaGroups" :key="group.id">
        <meta-group :group="group"></meta-group>
      </div>
    </div>
  </div>
</template>

<script>
import MetaGroup from '../meta/MetaGroup.vue'

import { mapState, mapActions } from 'vuex'

export default {
  components: { MetaGroup },
  mounted() {
    this.fetchMetaGroups()
  },
  data() {
    return {
      groups: null,
      totalGames: 200000
    }
  },
  computed: {
    ...mapState('metaData',[
      'metaGroups',
      'isLoading'
    ])
  },
  methods: {
    ...mapActions('metaData', [
      'fetchMetaGroups'
    ]),
  }

}
</script>