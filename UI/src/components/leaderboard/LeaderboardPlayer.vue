<template>
    <div class="info flex" :class="{champion: isChampion}">
        <div class="info-rank">{{rank}}</div>
        <div class="info-name">{{name}}</div>
        <div class="info-lp">{{lp}}</div>
    </div>
</template>

<script>
export default {
    props: {
        rank: Number,
        name: String,
        lp: Number,
    },
    computed: {
        isChampion() {
            return this.rank == 1
        }
    }
}
</script>

<style scoped>

    .info {
        color: white;
        background-color: var(--col-dark-grey);
        width: 100%;
        height: 40px;
        padding: 5px 0px;
        margin: 0px 0px;
        align-items: center;
        justify-content: space-around;
        border-radius: 5px;

        cursor: pointer;
    }

    .info:hover {
        background-color: var(--col-light-grey);

        /* box-shadow: 0px 0px 10px 2px var(--col-gold); */

    }

    .info.champion {
        /* color: rgb(126, 15, 15); */
        /* background-color: var(--col-gold); */

        box-shadow: inset 0px 0px 0px 2px var(--col-gold);
    }

    .info.champion:hover {

        /* color: var(--col-background); */
        /* background-color: rgb(250, 200, 34); */
        background: linear-gradient(60deg, var(--col-dark-gold), var(--col-gold));
        box-shadow: none;
        /* box-shadow: 0px 0px 10px 2px var(--col-gold); */
        /* font-weight: 600; */
    }

    .info-rank {
        width: 9.6%;
        text-align: center;
    }

    .info-name {
        width: 53.8%;
        text-align: left;
    }

    .info-lp {
        width: 9.6%;
        text-align: center;
    }

    a {
        text-decoration: none;
    }

    

</style>