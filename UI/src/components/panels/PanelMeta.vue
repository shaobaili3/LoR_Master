<template>
  <div>
    <p class="title text-3xl text-left pb-5 pt-3 sticky-top">Meta</p>
    <p class="sub-title text-left pb-2">Last 5 days | Patch 1.xx | 221k Matches</p>
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
      groups: null
    }
  },
  computed: {
    ...mapState('metaData',[
      'metaGroups'
    ])
  },
  methods: {
    ...mapActions('metaData', [
      'fetchMetaGroups'
    ]),
  }

}
</script>