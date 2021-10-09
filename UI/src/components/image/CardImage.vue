<template>
    <img class="card-image" :src="getCardDisplayUrl" alt="">
</template>

<script>

const cardDisplayUrlBase = 'https://dd.b.pvp.net/latest/'

export default {
    date() {
        return {}
    },
    props: {
        code: String,
        set: String,
    },
    computed: {
        getCardDisplayUrl() {
            if (!this.code) {
                return ""
            }
            var setString = this.set
            if (!setString) {
                var card = this.sets.find(card => card.cardCode == this.code)
                if (!card) {
                    return ""
                }
                setString = card.set
            }

            return cardDisplayUrlBase + setString.toLowerCase()  + '/' + this.locale + '/img/cards/' + this.code + '.png' 
        }
    }
}
</script>

<style>

</style>