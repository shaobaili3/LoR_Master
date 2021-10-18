<template>
    <div class="mulligan">
        <!-- <p class="title-text">Mulligan</p> -->
        <div class="images-contaienr">
            <div class="card-container" 
                v-for="(card, index) in startHandFiltered"
                :key="index">
                <card-image class="img" :code="card.CardCode"></card-image>
            </div>
            <div class="arrow">
                <i class="fas fa-arrow-right"></i>
            </div>
            <div class="card-container" 
                v-for="(card, index) in endHandFiltered"
                :key="index">
                <card-image class="img" :code="card.CardCode"></card-image>
            </div>
        </div>
    </div>
</template>

<script>
import CardImage from './image/CardImage.vue'

export default {
    components: {
        CardImage
    },
    mounted() {
    },
    data() {
        return {
        }
    },
    props: {
        startHand: Array,
        endHand: Array
    },
    computed: {
        startHandFiltered() {
            return this.startHand.filter((card) => {
                return card.CardCode !== 'face' && card.LocalPlayer
            })
        },
        endHandFiltered() {
            return this.endHand.filter((card) => {
                return card.CardCode !== 'face' && card.LocalPlayer
            })
        }
    },
    methods: {
    }
}
</script>

<style lang="scss" scoped>
.mulligan {

    // z-index: 8;

    .title-text {
        text-align: left;
        font-size: 0.8em;
    }
    .images-contaienr {
        // height: 100px;
        width: 100%;

        padding: 0px 5px;
        box-sizing: border-box;

        display: flex;
        justify-content: space-between;
        align-items: center;

        margin-top: 5px;
        

        .card-container {
            // height: 10%;
            display: flex;

            align-items: center;
            position: relative;

            width: 11%;
            min-height: 90px;
            

        &:hover {
            .img {
                position: absolute;
                width: 170px;
                // height: 200px;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 14;
            }
        }

            .img {
                pointer-events: none;
                width: 100%;
                height: auto;
            }
        }

        
    }
}
</style>