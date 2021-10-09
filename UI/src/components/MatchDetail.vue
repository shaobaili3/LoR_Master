<template>
    <div class="match-detail">
        <div class="" v-for="(card, index) in details.time_stamps"
        :key="index">
            {{card}}
            <!-- <card-preview></card-preview> -->
        </div>
    </div>
</template>

<script>
// import CardPreview from './CardPreview.vue'

export default {
    components: {
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

</style>