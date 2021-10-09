<template>
    <img class="cardDisplay" :src="getCardDisplayUrl" alt="">
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
            var setString = this.set
            if (!setString) {setString = this.sets.find(card => card.cardCode == this.code).set}
            return cardDisplayUrlBase + setString.toLowerCase()  + '/' + this.locale + '/img/cards/' + this.code + '.png' 
        }
    }
}
</script>

<style>

</style>