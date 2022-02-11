<template>
  <icon-champion
    v-for="(champ, index) in getChamps"
    :key="index"
    :code="champ.code"
    :count="champ.count"
    class=""
  ></icon-champion>
</template>

<script>
import DeckEncoder from "../../modules/runeterra/DeckEncoder"
import championCards from "../../assets/data/champion.js"
import IconChampion from "../image/IconChampion.vue"

export default {
  components: { IconChampion },
  data() {
    return {}
  },
  mounted() {},
  props: {
    deck: {
      type: String,
      require: true,
    },
    fixedNum: {
      type: Number,
      default: 2,
    },
  },
  computed: {
    extraChampString() {
      var extra = this.getChampsFromDeck.length - this.fixedNum
      if (extra > 0) return "+" + extra
      return ""
    },
    getChamps() {
      if (!this.deck) {
        return this.matchWidth([])
      }

      var deck = null
      var champs = []
      try {
        deck = DeckEncoder.decode(this.deck)
      } catch (err) {
        console.log(err)
        return this.matchWidth([])
      }

      for (var j in deck) {
        let champCode = deck[j].code
        if (championCards.champObj[champCode] != null) {
          let champ = {
            count: deck[j].count,
            code: champCode,
          }
          champs.push(champ)
        }
      }

      champs.sort((a, b) => {
        if (a.count > b.count) {
          return -1
        } else if (a.count == b.count) {
          if (a.code > b.code) {
            return -1
          }
        }
        return 1
      })

      return this.matchWidth(champs)
    },
  },
  methods: {
    matchWidth(champs) {
      var fixedNum = this.fixedNum
      if (fixedNum > 0) {
        if (champs.length > fixedNum) {
          return champs.slice(0, fixedNum)
        } else {
          while (champs.length < fixedNum) {
            champs.push({
              count: null,
              code: null,
            })
          }
        }
      }
      return champs
    },
  },
}
</script>

<style>
.icon-container {
  display: flex;
  /* padding: 4px; */
  align-items: center;
  position: relative;

  /* border-radius: 50px; */
}

.btn:hover .icon-container .icon.champ,
.btn.active .icon-container .icon.champ {
  border: 2px solid rgba(255, 255, 255, 1);
  box-shadow: 1px 2px 5px -2px #000000;
}

.extra-champ.fixed-width {
  position: absolute;
  bottom: -3px;
  right: -7px;
  /* background: var(--col-background); */
  border-radius: 5px;
}

/*     
    .count {
        padding: 2px;
        background: var(--col-darker-grey);
        border-radius: 100%;
    } */
</style>
