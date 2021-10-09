<template>
    <div class="match-detail">
        <div class="timeline-container">
            <div class="card-icon tooltip">
                <div class="tooltiptext top-start">Game Start</div>
            </div>
            <div class="card-icon" v-for="(card, index) in details.time_stamps"
                :key="index"
                :class="{'first': card.player}"
                :style="{'margin-left': 'calc('+timePercents[index]+'% - 10px)'}"
            >
                <card-image :code="card.card_code"></card-image>
            </div>
            <div class="card-icon tooltip" 
            :style="{'margin-left': 'calc('+timePercents[details.time_stamps.length]+'% - 10px)'}">
                <div class="tooltiptext top-end">Game End</div>
            </div>
        </div>
    </div>
</template>

<script>
import CardImage from './image/CardImage.vue'
// import CardPreview from './CardPreview.vue'

const gameEndAddTime = 10 // sec

export default {
    components: {
        CardImage
        // CardPreview,
    },
    mounted() {
        // console.log(this.details)
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

            return secDiff + gameEndAddTime
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
                var percent = secDiff / matchTime * 100 - prevPercent
                prevPercent = percent
                remain -= percent
                percents.push(percent)
                console.log(percent)
            });

            percents.push(remain) // Last one for the last item

            return percents
        }
    },
    methods: {
    }
}
</script>

<style lang="scss" scoped>
    .match-detail {

        .timeline-container {
            display: flex;
            width: 100%;
            justify-content: flex-start;
            // gap: 1px;

            padding-top: 20px;
            padding-left: 10px;
            padding-right: 10px;
            box-sizing: border-box;

            .card-icon {

                position: relative;
                width: 10px;
                height: 20px;
                background: white;
                overflow: hidden;

                box-sizing: border-box;
                // border-left: 1px solid black;

                &.first {
                    background: black;
                }

                .card-image {
                    position: absolute;

                    bottom: 100%;
                    left: 100%;
                    transform: translateX(-50%);
                    
                    width: 100px;
                    height: auto;
                    opacity: 0;
                    filter: drop-shadow(3px 3px 2px rgba(43, 38, 27, 0.6));
                    z-index: 10;
                    transition: opacity 0.15s cubic-bezier(0.075, 0.82, 0.165, 1);

                    
                }

                &:hover {
                    overflow: visible;
                    .card-image {
                        opacity: 1;
                        
                    }
                }
            }
        }

    }
</style>