<template>
    <div class="match-detail">
        <div class="" v-for="(card, index) in details.time_stamps"
        :key="index">
            {{card}}
            <div class="card-icon">
                <card-image :code="card.card_code" ></card-image>
            </div>
            <!-- <card-preview></card-preview> -->
        </div>
    </div>
</template>

<script>
import CardImage from './image/CardImage.vue'
// import CardPreview from './CardPreview.vue'

export default {
    components: {
        CardImage
        // CardPreview,
    },
    mounted() {
        // console.log(this.details)
        if (this.details) {
            var timeStamps = this.details.time_stamps
            var date = new Date(this.time)
            
            console.log(date.getTime() / 1000)

            timeStamps.forEach(timeStamp => {

                var cardCode = timeStamp.card_code
                var cardDate = new Date(timeStamp.utc_time * 1000)

                var secDiff = Math.floor((cardDate - date)/1000)

                console.log(secDiff) // Get Difference In Milli Seconds
                
            });
        }
    },
    data() {
    },
    props: {
        time: String,
        details: Object,
    },
    computed: {
    },
    methods: {
    }
}
</script>

<style lang="scss" scoped>
    .match-detail {

        .card-icon {
            width: 10px;
            height: 10px;
            background: white;

            .card-image {
                width: 100px;
                height: auto;
                opacity: 0;
                filter: drop-shadow(3px 3px 2px rgba(43, 38, 27, 0.6));
                z-index: 10;
                transition: opacity 0.15s cubic-bezier(0.075, 0.82, 0.165, 1);
            }

            &:hover {
                .card-image {
                    opacity: 1;
                    
                }
            }
        }


        
    }
</style>