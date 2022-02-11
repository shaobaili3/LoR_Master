<template>
  <div class="timeline">
    <!-- <svg viewBox="-5 0 105 20" preserveAspectRatio="none">
            <line @mouseenter="lineHover($event, 0)" x1="0" y1="0" x2="0" y2="20"></line>
            <line @mouseenter="lineHover($event, 1)" x1="20" y1="0" x2="20" y2="20"></line>
        </svg> -->
    <!-- <p class="title-text">Timeline</p> -->
    <div
      class="hover-container"
      v-if="displayInfo"
      :style="{ left: displayInfo.left + 'px', top: displayInfo.top + 'px' }"
    >
      <div
        class="time-indicator"
        v-if="displayInfo.code"
        :class="{ first: displayInfo.first }"
      ></div>
      <p class="time-text" v-if="displayInfo.time">
        {{ moment(new Date(displayInfo.time) - new Date(details.startTime)).format("mm:ss") }}
      </p>
      <image-card class="card-hover" v-if="displayInfo.code" :code="displayInfo.code"></image-card>
    </div>
    <div
      class="timeline-container"
      @wheel.prevent="handleScroll"
      :class="{ grabbing: grabbing }"
      @scroll="whenScrolled"
    >
      <div class="timeline-content" :style="{ width: zoom + '%' }">
        <!-- <div class="gridline" v-for="i in 10"
                    :key="i"
                    :style="{'left': i*10+'%'}"
                    :class="{'thick': i%5==0 }"
                ></div> -->
        <!-- <div class="card-icon event"> -->
        <!-- <div class="tooltiptext top-start">Game Start</div> -->
        <!-- </div> -->
        <div
          class="card-icon"
          v-for="(card, index) in timelineFiltered"
          :key="index"
          :class="{ first: card.LocalPlayer }"
          :style="{ left: 'calc(' + timePercents[index] + '% - 10px)' }"
          @mouseenter="iconHover($event, card)"
          @mouseleave="iconLeave($event)"
        >
          <svg viewBox="0 0 10 10">
            <!-- <polygon points="0,0 10,0 10,10 0,10"></polygon> -->
            <!-- normal circle -->
            <!-- <ellipse cx="5" cy="5" rx="4.045" ry="4.045"></ellipse> -->

            <ellipse cx="5" cy="5" rx="3.6" ry="3.6"></ellipse>

            <!-- pentagon -->
            <!-- <polygon points="5,0 9.755,3.455 7.939,9.045 2.061,9.045 0.245,3.455"></polygon> -->

            <!-- diamond -->
            <polygon points="5,0 10,5 5,10 0,5"></polygon>

            <!-- triangle up -->
            <!-- <polygon points="5,0 10,8 0,8"></polygon> -->
            <!-- triangle down -->
            <!-- <polygon points="5,9 10,1 0,1"></polygon> -->

            <!-- angled triangle -->
            <!-- <polygon points="7,0 8.009,8.993 0,6"></polygon> -->

            <!-- <polygon points="0,0 0,10 10,10 10,0"></polygon> -->

            <!-- 6 sided -->
            <!-- upward -->
            <!-- <polygon points="5,0 9.33,2.5 9.33,7.5 5,10 0.67,7.5 0.67,2.5"></polygon> -->
            <!-- thinner -->
            <!-- <polygon points="5,0 8.33,2.5 8.33,7.5 5,10 1.67,7.5 1.67,2.5"></polygon> -->
            <!-- side way -->
            <!-- <polygon points="10,5 7.5,9.33 2.5,9.33 0,5 2.5,0.67 7.5,0.67"></polygon> -->
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import CardPreview from './CardPreview.vue'

import moment from "moment"
import ImageCard from "../image/ImageCard.vue"

let pos = { top: 0, left: 0, x: 0, y: 0 }

const gameEndAddTime = 10 // sec
const minZoom = 100 // percent
const maxZoom = 3000 // percent

export default {
  components: {
    ImageCard,
  },
  mounted() {
    this.ele = document.querySelectorAll(".timeline-container")

    for (const el of this.ele) {
      el.addEventListener("mousedown", this.mouseDownHandler)
    }
  },
  data() {
    return {
      ele: null,
      grabbing: false,
      zoom: minZoom,
      scrollLeft: 0,
      moment: moment,

      displayInfo: {
        code: null,
        left: null,
        top: null,
        time: null,
        first: null,
      },

      mouseMoveListener: null,
      mouseUpListener: null,
    }
  },
  props: {
    details: Object,
  },
  computed: {
    matchTime() {
      var startTime = new Date(this.details.startTime)
      console.log("Start time", startTime)
      var endTime = new Date(this.details.endTime)
      console.log("End time", endTime)

      var secDiff = Math.floor((endTime - startTime) / 1000)
      console.log("Match Time: ", secDiff)
      return secDiff
    },
    timelineFiltered() {
      return this.details.timeline.filter((card) => {
        return card.CardCode != "face"
      })
    },
    timePercents() {
      var percents = []
      var matchTime = this.matchTime
      var times = this.timelineFiltered

      var date = new Date(this.details.startTime)

      var remain = 100

      times.forEach((time) => {
        var cardDate = new Date(time.playTime)

        var secDiff = Math.floor((cardDate - date) / 1000)
        var percent = (secDiff / matchTime) * 100

        percents.push(percent)
      })

      percents.push(remain) // Last one for the last item

      return percents
    },
  },
  methods: {
    whenScrolled(event) {
      this.scrollLeft = event.currentTarget.scrollLeft
    },
    mouseDownHandler(e) {
      this.grabbing = true

      pos = {
        // The current scroll
        left: e.currentTarget.scrollLeft,
        top: e.currentTarget.scrollTop,
        // Get the current mouse position
        x: e.clientX,
        y: e.clientY,
      }

      const tar = e.currentTarget

      this.mouseMoveListener = (ev) => {
        this.mouseMoveHandler(ev, tar)
      }
      this.mouseUpListener = (ev) => {
        this.mouseUpHandler(ev, tar)
      }

      document.addEventListener("mousemove", this.mouseMoveListener)
      document.addEventListener("mouseup", this.mouseUpListener)
    },
    mouseMoveHandler(e, tar) {
      // How far the mouse has been moved

      const dx = e.clientX - pos.x
      const dy = e.clientY - pos.y

      // Scroll the element
      tar.scrollLeft = pos.left - dx
    },
    mouseUpHandler() {
      // HAndle Mouse Up
      this.grabbing = false

      document.removeEventListener("mousemove", this.mouseMoveListener)
      document.removeEventListener("mouseup", this.mouseUpListener)
    },
    iconHover(event, card) {
      var tar = event.currentTarget
      var rect = tar.getBoundingClientRect()

      var left = rect.x + rect.width
      var top = rect.y + rect.height

      this.displayInfo = {
        code: card.CardCode,
        time: card.playTime,
        left: left,
        top: top,
        first: card.LocalPlayer,
      }
    },
    iconLeave(event) {
      this.displayInfo = null
    },
    handleScroll(event) {
      var el = event.currentTarget

      let box = el.getBoundingClientRect()
      var elWidth = box.width

      const zoomSpeed = 1.2

      if (event.deltaY > 0) {
        // Zoom out
        let newZoom = this.zoom / zoomSpeed
        if (newZoom <= minZoom) {
          newZoom = minZoom
        }
        this.zoom = newZoom

        let offset = event.clientX - box.x
        let offsetZoomed = offset / zoomSpeed
        const newScroolLeft = el.scrollLeft / zoomSpeed - (offset - offsetZoomed)

        this.$nextTick(() => {
          el.scrollLeft = newScroolLeft
        })
      } else {
        // Zoom in

        let newZoom = this.zoom * zoomSpeed
        if (newZoom >= maxZoom) {
          newZoom = maxZoom
        }

        let offset = event.clientX - box.x
        let offsetZoomed = offset * zoomSpeed
        const newScroolLeft = el.scrollLeft * zoomSpeed + (offsetZoomed - offset)

        this.zoom = newZoom
        this.$nextTick(() => {
          el.scrollLeft = newScroolLeft
        })
      }
    },
  },
}
</script>

<style lang="scss" scoped>
@keyframes delay-overflow {
  from {
    overflow: hidden;
  }
}

.timeline {
  margin-top: 5px;

  .title-text {
    text-align: left;
    font-size: 0.8em;
  }

  .hover-container {
    pointer-events: none;
    position: fixed;
    z-index: 10;

    .time-indicator {
      position: absolute;
      width: 2px;
      height: 60px;
      background: white;
      top: -60px;
      left: -6px;
      opacity: 0.8;
      // z-index: 5;

      &.first {
        background: var(--col-gold);
      }
    }

    .card-hover {
      position: absolute;
      width: 200px;
      height: auto;
      transform: translateX(calc(-50% - 5px)) translateY(calc(-100% - 45px));
    }

    .time-text {
      position: absolute;
      font-size: 0.8em;
      transform: translateX(10px) translateY(calc(-100% - 40px));
    }
  }

  .timeline-container {
    // position: relative;

    cursor: grab;
    &.grabbing {
      cursor: grabbing;
    }

    width: 100%;
    overflow-x: scroll;

    // &::-webkit-scrollbar {
    //     dis
    // }

    // gap: 1px;

    margin-top: 2px;

    // padding-top: 20px;
    padding-left: 10px;
    padding-right: 10px;
    // padding-bottom: 10px;
    box-sizing: border-box;

    // background: var(--col-gold);
    // background: var(--col-background);
    background: var(--col-darker-grey);

    border-radius: 4px;

    .timeline-content {
      // width: 100%;

      position: relative;

      height: 60px;

      display: flex;
      justify-content: flex-start;

      .gridline {
        position: absolute;
        left: 10%;
        top: -50%;
        width: 1px;
        height: 200%;
        background-color: white;

        &.thick {
          width: 2px;
        }
      }

      .card-icon {
        position: absolute;
        width: 10px;
        height: 100%;
        // padding-top: 22px;
        // padding-bottom: 12px;
        // background: white;
        overflow: visible;

        opacity: 0.5;

        &.first {
          svg {
            padding-top: 10px;
            fill: var(--col-gold);
          }
        }

        &.diamond {
          opacity: 0.6;
          svg {
            ellipse {
              display: none;
            }
            polygon {
              display: initial;
            }
          }
        }

        // box-sizing: border-box;
        // border-left: 1px solid black;

        &:hover {
          // Hover
          opacity: 0.99; // Somehow setting this to 1 changes the order and thus changes the layout ?!

          // Something seems wrong with this before indicator? Causes some layout shift
          &.event::before {
            display: none;
          }

          // svg {
          //     width: 14px;
          //     height: 14px;
          //     margin-right: -2px;
          //     margin-top: -2px;
          // }
        }

        svg {
          position: absolute;
          display: block;
          height: 10px;
          width: 10px;
          top: calc(50% - 5px);

          right: 0px;

          fill: white;

          ellipse {
            display: initial;
          }

          polygon {
            display: none;
          }
        }

        &.event::after {
          // top: 0;
          height: 100%;
          width: 4px;
          background: #160c28;
          border-radius: 0px;

          display: none;
        }

        .card-image {
          position: fixed;

          // top: 0px;
          // left: 0px;
          // bottom: 100%;
          // left: 100%;
          transform: translateX(calc(-50% - 1px)) translateY(calc(-100% - 10px)); // because of 10px width of the selector

          width: 200px;
          height: auto;

          visibility: hidden;
          opacity: 0;
          filter: drop-shadow(3px 3px 2px rgba(43, 38, 27, 0.6));
          z-index: 10;
          transition: visibility 0s linear 0.3s, opacity 0.3s cubic-bezier(0.075, 0.82, 0.165, 1);

          pointer-events: none;
        }

        &:hover {
          // overflow: visible;

          .card-image {
            visibility: visible;
            opacity: 1;
            transition: visibility 0s linear 0s, opacity 0.3s ease;
          }
        }
      }
    }
  }
}
</style>
