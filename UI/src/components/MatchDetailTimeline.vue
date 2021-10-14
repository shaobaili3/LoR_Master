<template>
    <div class="timeline">
        <!-- <svg viewBox="-5 0 105 20" preserveAspectRatio="none">
            <line @mouseenter="lineHover($event, 0)" x1="0" y1="0" x2="0" y2="20"></line>
            <line @mouseenter="lineHover($event, 1)" x1="20" y1="0" x2="20" y2="20"></line>
        </svg> -->
        <!-- <p class="title-text">Timeline</p> -->
        <div class="timeline-container" @wheel.prevent ="handleScroll"
            :class="{'grabbing': grabbing}"
            @scroll="whenScrolled"
        >
            <div class="timeline-content" :style="{'width': zoom+'%'}">
                <!-- <div class="gridline" v-for="i in 10"
                    :key="i"
                    :style="{'left': i*10+'%'}"
                    :class="{'thick': i%5==0 }"
                ></div> -->
                <div class="card-icon event">
                    <!-- <div class="tooltiptext top-start">Game Start</div> -->
                </div>
                <div class="card-icon" v-for="(card, index) in details.time_stamps"
                    :key="index"
                    :class="{'first': card.player, 'diamond': index % 7 == 0}"
                    :style="{'padding-left': 'calc('+timePercents[index]+'% - 10px)'}"
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
                    <p class="time-text">{{Math.floor(card.relative_time/60)}}:{{card.relative_time % 60}}</p>
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
            // this.ele.scrollTop = pos.top - dy;
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

                if (this.zoom <= 100) {
                    this.zoom = 100
                    this.ele.scrollLeft = 0
                }
                
            } else {
                // Zoom in
                this.zoom = this.zoom * zoomSpeed
                this.ele.scrollLeft = this.ele.scrollLeft * zoomSpeed
                
                if (this.zoom >= 3000) {
                    this.zoom = 3000
                }
            }
        },
    }
}
</script>

<style lang="scss" scoped>


    @keyframes delay-overflow {
        from { overflow: hidden; }
    }

    .timeline {

        margin-top: 5px;

        .title-text {
            text-align: left;
            font-size: 0.8em;
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

                    position: relative;
                    width: 10px;
                    height: 20px;
                    padding-top: 22px;
                    padding-bottom: 12px;
                    // background: white;
                    overflow: visible;
                    
                    opacity: 0.5;

                    &.first {
                        svg {
                            padding-top: 10px;
                            fill: var(--col-gold);;
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
                        opacity: 1;

                        &::before {
                            // On hover shows the indicator
                            content: "";
                            position: absolute;
                            bottom: -50%;
                            right: 4px;
                            width: 2px;
                            height: 200%;
                            background: var(--col-dark-gold);

                            // transform: translateX(-50%);
                        }

                        &.event::before {
                            display: none;
                        }

                        .time-text {
                            opacity: 1;
                        }

                        svg {
                            width: 14px;
                            height: 14px;
                            margin-right: -2px;
                            margin-top: -2px;
                        }
                        
                    }

                    svg {
                        position: absolute;
                        display: block;
                        height: 10px;
                        width: 10px;

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
                        background: #160C28;
                        border-radius: 0px;

                        display: none;
                    }

                    .time-text {
                        opacity: 0;
                        font-size: 0.8em;
                        position: absolute;
                        margin-top: -22px;
                        margin-left: 20px;
                        z-index: 12; // Above the image which is 10
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
                            transition:  visibility 0s linear 0s, opacity 0.3s ease;
                        }
                    }
                }
            }

            
        }

    }
</style>