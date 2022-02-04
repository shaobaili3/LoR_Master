<template>
  <div
    :class="{
      'h-[94px] sm:h-[106px]': !winStreak && !isDateBreak,
      'h-[118px] sm:h-[130px]': isDateBreak,
      'h-[126px] sm:h-[138px]': winStreak,
    }"
  >
    <div class="flex justify-between pt-1 pb-1" v-if="winStreak">
      <div class="pl-2 text-left">
        {{ $t("matches.winStreak", { num: winStreak }) }}
      </div>
      <!-- <div class="text-right cursor-pointer" @click="downloadStreakScreenshot">
        Download Screenshot
      </div> -->
    </div>
    <div class="pb-1 pl-2 text-sm text-left text-gray-200" v-if="isDateBreak && !winStreak">
      {{ timeString }}
    </div>
    <div class="match-history match" :class="{ won: won, loss: !won }">
      <div class="btn-expand-detail" v-if="details" @click="toggleDetail">
        <i class="fas" :class="{ 'fa-chevron-down': !showDetail, 'fa-chevron-up': showDetail }"></i>
      </div>
      <div class="overflow-x-scroll row opponent no-scrollbar">
        <p @click="search" class="match-info-title">
          <i class="fas" :class="{ 'fa-pennant pr-2': win, '': !win }"></i>
          <span class="desktop">vs </span>
          <span class="name" :class="{ search: region }">{{ opponentName }}</span>
        </p>
        <div class="opponent-info" v-if="opponentRank"><i class="fas fa-trophy"></i> {{ opponentRank }}</div>
        <div class="history-info">{{ timeString }}</div>
        <div class="history-info desktop" v-if="rounds">{{ rounds }} {{ $t("str.rounds") }}</div>
        <div class="match-info-badge" v-for="badge in filteredBadges" :key="badge">
          <span
            v-if="badge == 'recent' || badge == 'frequent'"
            class="match-info-badge-icon fa"
            :class="{ 'fa-clock': badge == 'recent', 'fa-angle-double-up': badge == 'frequent' }"
          ></span>
          {{ $t("matches.badges." + badge.replace(/\s+/g, "")) }}
        </div>
      </div>
      <div class="row decklist">
        <deck-preview @click.stop :deck="deck" :won="won" :fixedWidth="false"></deck-preview>
        <span class="vs-text">
          <span>VS</span>
          <span class="mobile">
            <p @click="search" class="match-info-title">
              vs <span class="name" :class="{ search: region }">{{ opponentName }}</span>
            </p>
            <div class="opponent-info" v-if="opponentRank"><i class="fas fa-trophy"></i> {{ opponentRank }}</div>
          </span>
        </span>
        <deck-preview @click.stop :deck="opponentDeck" :won="won" :fixedWidth="false"></deck-preview>
      </div>
      <div class="divider" v-if="details && showDetail" :class="{ won: won }"></div>
      <match-detail-mulligan
        v-if="details && showDetail"
        :startHand="details.openHand"
        :endHand="details.replacedHand"
      ></match-detail-mulligan>

      <match-detail-timeline v-if="details && showDetail" :time="time" :details="details"></match-detail-timeline>
    </div>
  </div>
</template>

<script>
import DeckPreview from "../deck/DeckPreview.vue"
import MatchDetailMulligan from "../match/MatchDetailMulligan.vue"
import MatchDetailTimeline from "../match/MatchDetailTimeline.vue"

import { format, formatDistanceStrict } from "date-fns"
import { dateFNSLocales } from "../../assets/data/messages"

export default {
  components: {
    DeckPreview,
    MatchDetailTimeline,
    MatchDetailMulligan,
  },
  mounted() {
    // console.log(this.details)
  },
  data() {
    return {
      visibleDeck: 0,
      showDetail: false,
    }
  },
  emits: ["search", "screenshot"],
  props: {
    // opponentName, opponentRank, opponentLp, opponentDeck
    // deck, rounds, win, time, badges, details, region, winStreak, isDateBreak
    opponentName: String,
    opponentRank: String,
    opponentLp: String,
    rounds: Number,
    deck: String,
    opponentDeck: String,
    win: Boolean,
    time: String,
    badges: Array,
    details: Object,
    region: String,
    winStreak: { type: Number, default: 0 },
    isDateBreak: { type: Boolean, default: false },
    index: Number,
  },
  computed: {
    timeString() {
      // var date = new Date(this.time)
      // var time

      // var milliElapsed = Date.now() - date
      // var secondsElapsed = milliElapsed / 1000
      // var minElapse = secondsElapsed / 60
      // var hoursElapse = minElapse / 60
      // var daysElapsed = hoursElapse / 24

      // if (secondsElapsed < 60) {
      //   time = this.$t("str.times.sec", { t: Math.floor(secondsElapsed) })
      // } else if (minElapse < 60) {
      //   time = this.$t("str.times.min", { t: Math.floor(minElapse) })
      // } else if (hoursElapse < 24) {
      //   if (Math.floor(hoursElapse) == 1) {
      //     time = this.$t("str.times.hour", { t: Math.floor(hoursElapse) })
      //   } else {
      //     time = this.$t("str.times.hours", { t: Math.floor(hoursElapse) })
      //   }
      // } else if (daysElapsed < 7) {
      //   if (Math.floor(daysElapsed) == 1) {
      //     time = this.$t("str.times.day", { t: Math.floor(daysElapsed) })
      //   } else {
      //     time = this.$t("str.times.days", { t: Math.floor(daysElapsed) })
      //   }
      // } else {
      //   time = date.toLocaleDateString()
      // }

      return formatDistanceStrict(new Date(this.time), new Date(), {
        addSuffix: true,
        locale: dateFNSLocales[this.$i18n.locale],
      })

      // return time
    },
    opponentLink() {
      return "/profile/" + this.opponentName
    },
    won() {
      // return parseFloat(this.winrate) > 0.5;
      return this.win
    },
    filteredBadges() {
      if (!this.badges) return null
      var filtered = this.badges
        .map((b) => b.trim())
        .filter((badge, pos, self) => {
          // remove "Constructed" and duplicates
          return !badge.includes("Constructed") && self.indexOf(badge) == pos
        })
      return filtered
    },
  },
  methods: {
    downloadStreakScreenshot() {
      this.$emit("screenshot", this.index)
    },
    toggleDetail() {
      this.showDetail = !this.showDetail

      this.sendUserEvent({
        category: "Main Window Match",
        action: this.showDetail ? "Show Detail" : "Hide Detail",
        label: this.deck,
        value: null,
      })
    },
    search() {
      // console.log("Match History Search")
      this.$emit("search")
    },
    showOpponentDeck() {
      // console.log("Show Oppo Deck")
      if (this.visibleDeck == 2) this.visibleDeck = 0
      else this.visibleDeck = 2
    },
  },
}
</script>

<style lang="scss">
.divider {
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  height: 2px;
  /* background-color: var(--col-background); */
  background-color: var(--col-light-grey);
  margin-top: 8px;
  /* margin-bottom: 5px; */

  &.won {
    background-color: var(--col-gold);
  }
}

.btn-expand-detail {
  position: absolute;
  top: 0;
  right: 0;
  padding: 0.7em;
  cursor: pointer;
}

.match {
  position: relative;
  display: flex;
  width: 100%;
  flex-direction: column;
  background: linear-gradient(60deg, var(--col-grey), var(--col-lighter-grey));
  box-sizing: border-box;
  padding: 5px;
  border-radius: 6px;

  overflow-x: visible;

  /* overflow: hidden; */

  border-left: 3px solid var(--col-background);
  border-right: 3px solid var(--col-background);

  font-size: 1em;
}

.match.won {
  /* background: linear-gradient(-60deg,rgb(224, 171, 24), rgb(78, 78, 78) 60%); */
  /* box-shadow: inset 0px 0px 0px 2px var(--col-gold); */
  background: linear-gradient(60deg, var(--col-dark-gold), var(--col-gold));
  /* box-shadow: 2px solid gold; */
  /* background: linear-gradient(90deg,rgb(224, 171, 24) 1%, rgb(94, 94, 94) 1%); */
}

.match.loss {
  /* background: linear-gradient(300deg,rgb(224, 171, 24), rgb(94, 94, 94)); */
  /* background: linear-gradient(300deg,rgb(224, 171, 24) 20%, rgb(94, 94, 94) 20%); */
  /* background: linear-gradient(-90deg,rgb(224, 171, 24) 1%, rgb(94, 94, 94) 1%); */
}

.match-info-badge-icon {
  /* margin-right: 3px; */
  /* width: 10px; */
  /* display: flex; */
  /* align-content: center; */
  /* justify-content: center; */
}

.match-info-badge {
  font-size: 0.7em;
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.2);
  padding: 3px 8px;
  margin-right: 5px;
  border-radius: 50px;
  cursor: default;
  white-space: nowrap;
}

.match-info-badge:hover {
  color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.3);
}

.history-info {
  font-size: 0.8em;
  color: rgba(255, 255, 255, 0.7);
  padding: 8px 6px;
  cursor: default;
  white-space: nowrap;
}

.history-info:hover {
  color: rgba(255, 255, 255, 1);
}

.opponent-info {
  font-size: 0.8em;
  color: rgba(255, 255, 255, 1);
  padding: 8px 6px 8px 0px;
  cursor: default;
  white-space: nowrap;
}

.opponent-info i {
  font-size: 0.85em;
}

.row {
  display: flex;
  align-items: center;
}

.row.decklist {
  /* justify-content: space-between; */
  justify-content: space-around;
  align-items: center;
}

.vs-text {
  padding: 0px 10px;
}

.match-history-dots {
  display: flex;
  gap: 8px;
  /* height: 20px; */

  justify-content: flex-start;
  align-items: center;

  padding: 2px 2px 5px 2px;
  margin: 0;
  margin-left: 8px;
  margin-right: 8px;
}

.row.match-history-dots .dot {
  height: 10px;
  width: 10px;
  border-radius: 10px;

  background-color: var(--col-background);
  opacity: 0.1;
}

.row.match-history-dots .dot.played {
  opacity: 0.3;
  background: rgb(255, 255, 255);
}

.row.match-history-dots .dot.played.won {
  opacity: 0.7;
  background: rgb(255, 255, 255);
}

/* .row.match-history-dots:hover .dot {
        display: none;
    } */

.row.match-history-dots:hover .dot {
  opacity: 0.05;
}

.row.match-history-dots:hover .dot.played {
  /* display: initial; */
  opacity: 0.5;
  /* background-color: var(--col-background); */
}

.match-history-dots:hover .dot.played.won {
  opacity: 1;
  background: rgb(255, 255, 255);
  box-shadow: 1px 2px 5px -2px #000000;
}

.match-history-summary {
  /* display: block; */
  /* display: flex; */
  /* align-items: center; */
  line-height: 10px;
  height: 10px;
  text-align: center;
  /* height: 20px; */
  /* line-height: 20px; */
  font-size: 0.8em;
  /* display: none; */
  opacity: 0.7;
  white-space: nowrap;
}

.match-history-dots:hover .match-history-summary {
  opacity: 1;
}

.match-info-title {
  /* display: block; */
  padding: 5px 5px 5px 1px;
  margin: 0;
  margin-left: 8px;
  margin-right: 5px;

  /* padding-bottom: 5px; */
  /* border-radius: 6px; */
  text-decoration: none;
  white-space: nowrap;

  /* border-bottom: 2px solid transparent; */
  border-radius: 0px;
}

.match-info-title:hover .name.search {
  cursor: pointer;
  text-decoration: underline;
}

.btn:hover {
  /* background-color: rgba(255, 255, 255, 0.5); */
  /* text-decoration: underline; */
  /* border-bottom: 1px solid white; */
  cursor: pointer;
}

@media screen and (max-width: 275px) {
  .match {
    font-size: 0.85em;
  }

  .match-info-title {
    padding: 3px 3px 3px 1px;
    margin-left: 5px;
  }

  .match-history-dots {
    gap: 5px;
    margin-left: 5px;
  }

  .history-info {
    padding-right: 2px;
  }
}
</style>
