<template>
    <div class="timeline">
        <!-- <svg viewBox="-5 0 105 20" preserveAspectRatio="none">
            <line @mouseenter="lineHover($event, 0)" x1="0" y1="0" x2="0" y2="20"></line>
            <line @mouseenter="lineHover($event, 1)" x1="20" y1="0" x2="20" y2="20"></line>
        </svg> -->
        <div class="timeline-container" @wheel.prevent ="handleScroll"
            :class="{'grabbing': grabbing}"
            @scroll="whenScrolled"
        >
            <div class="timeline-content" :style="{'width': zoom+'%'}">
                <div class="card-icon event">
                    <!-- <div class="tooltiptext top-start">Game Start</div> -->
                </div>
                <div class="card-icon" v-for="(card, index) in details.time_stamps"
                    :key="index"
                    :class="{'first': card.player}"
                    :style="{'padding-left': 'calc('+timePercents[index]+'% - 10px)'}"
                >
                    <card-image :code="card.card_code" @mousedown.prevent="" :style="{'margin-left': -scrollLeft+'px'}"></card-image>
                </div>
                <div class="card-icon event" 
                :style="{'padding-left': 'calc('+timePercents[details.time_stamps.length]+'% - 10px)'}">
                    <!-- <div class="tooltiptext top-end">Game End</div> -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CardImage from './image/CardImage.vue'
// import CardPreview from './CardPreview.vue'


let pos = { top: 0, left: 0, x: 0, y: 0 };

const gameEndAddTime = 10 // sec

export default {
    components: {
        CardImage
        // CardPreview,
    },
    mounted() {
        // console.log(this.details)
        this.ele = document.querySelector('.timeline-container');
        this.ele.addEventListener('mousedown', this.mouseDownHandler);

        if (this.details) {
            // var timeStamps = this.details.time_stamps
            // var date = new Date(this.time)
            
            // console.log(date.getTime() / 1000)

            // timeStamps.forEach(timeStamp => {

            //     var cardCode = timeStamp.card_code
            //     var cardDate = new Date(timeStamp.utc_time * 1000)
            //     var secDiff = Math.floor((cardDate - date)/1000)

            //     console.log(secDiff) // Get Difference In Milli Seconds
                
            // });
            console.log("Total Match Time", this.matchTime)
        }
    },
    data() {
        return {
            ele: null,
            grabbing: false,
            zoom: 100,
            scrollLeft: 0,
        }
    },
    props: {
        time: String,
        details: Object,
    },
    computed: {
        matchTime() {
            var times = this.details.time_stamps
            var lastTime = times[times.length-1].utc_time

            var date = new Date(this.time)
            var cardDate = new Date(lastTime * 1000)
            
            var secDiff = Math.floor((cardDate - date)/1000)

            return parseInt(times[times.length-1].relative_time) + gameEndAddTime
        },
        timePercents() {
            var percents = []
            var matchTime = this.matchTime
            var times = this.details.time_stamps
            var date = new Date(this.time)

            var remain = 100
            var prevPercent = 0
            
            times.forEach(time => {
                var cardDate = new Date(time.utc_time * 1000)
                
                var secDiff = Math.floor((cardDate - date)/1000)
                
                // console.log(secDiff)
                var cardTime = parseInt(time.relative_time)

                var percent = cardTime / matchTime * 100 - prevPercent
                prevPercent += percent
                remain -= percent
                percents.push(percent)
                console.log(percent)
            });

            percents.push(remain) // Last one for the last item

            return percents
        }
    },
    methods: {
        whenScrolled(event) {
            this.scrollLeft = event.currentTarget.scrollLeft
            console.log(this.scrollLeft)
        },
        mouseDownHandler(e) {
            // console.log("Mouse Down")
            // Some user friendly
            // this.ele.style.cursor = 'grabbing';
            // this.ele.style.userSelect = 'none';
            this.grabbing = true

            pos = {
                // The current scroll
                left: this.ele.scrollLeft,
                top: this.ele.scrollTop,
                // Get the current mouse position
                x: e.clientX,
                y: e.clientY,
            };

            document.addEventListener('mousemove', this.mouseMoveHandler);
            document.addEventListener('mouseup', this.mouseUpHandler);
        },
        mouseMoveHandler(e) {
            // How far the mouse has been moved
            const dx = e.clientX - pos.x;
            const dy = e.clientY - pos.y;

            // Scroll the element
            this.ele.scrollTop = pos.top - dy;
            this.ele.scrollLeft = pos.left - dx;
        },
        mouseUpHandler() {
            // console.log("Mouse Up")
            this.grabbing = false

            document.removeEventListener('mousemove', this.mouseMoveHandler);
            document.removeEventListener('mouseup', this.mouseUpHandler);

            // this.ele.style.cursor = 'grab';
            // this.ele.style.removeProperty('user-select');
        },
        // lineHover(event, index) {
        //     var tar = event.target
        //     var rect = tar.getBoundingClientRect()
        //     console.log("Line", index, "Hovered at (", event.clientX, ", ",event.clientY, ")", 
        //     "Elemetn at (", rect.x, ", ", rect.y, ")")
        // },
        handleScroll(event) {
            var el = event.currentTarget

            const zoomSpeed = 1.2

            // this.ele.scrollTop
            // console.log(this.ele.scrollLeft)
            // console.log(this.ele.scrollWidth)

            if (event.deltaY > 0) {
                // Zoom out
                this.zoom = this.zoom / zoomSpeed
                this.ele.scrollLeft = this.ele.scrollLeft / zoomSpeed
                
                
            } else {
                // Zoom in
                this.zoom = this.zoom * zoomSpeed
                this.ele.scrollLeft = this.ele.scrollLeft * zoomSpeed
                
                
            }
        },
    }
}
</script>

<style lang="scss" scoped>

svg {

    display: block;
    height: 40px;
    width: 100%;

    line {
        stroke: red;
        stroke-width: 1;
        stroke-linecap: round;
        // stroke-dasharray
        transition: stroke 0.5s ease;
    }

    line:hover {
        stroke: blue;
    }
}

@keyframes delay-overflow {
    from { overflow: hidden; }
}

    .timeline {

        .timeline-container {

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

            padding-top: 20px;
            padding-left: 10px;
            padding-right: 10px;
            padding-bottom: 10px;
            box-sizing: border-box;

            .timeline-content {
                // width: 100%;
                
                display: flex;
                justify-content: flex-start;

                .card-icon {

                    position: relative;
                    width: 10px;
                    height: 20px;
                    // background: white;
                    overflow: visible;

                    // box-sizing: border-box;
                    // border-left: 1px solid black;

                    &::after {
                        content: "";
                        position: absolute;
                        top: 0;
                        right: 0;
                        width: 10px;
                        height: 100%;
                        background: white;
                        // background-image: url('../assets/images/cardback.png');
                        // background-repeat: no-repeat;
                        // background-size: auto 100%;
                    }

                    &.first::after {
                        background: black;
                    }

                    &.event::after {
                        background: grey;
                    }

                    .card-image {
                        position: fixed;

                        // top: 0px;
                        // left: 0px;
                        // bottom: 100%;
                        // left: 100%;
                        transform: translateX(calc(-50%)) translateY(-100%); // because of 10px width of the selector
                        
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
                            transition:  visibility 0s linear 0s, opacity 0.3s ease;
                        }
                    }
                }
            }

            
        }

    }
</style>