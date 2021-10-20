<template>
    <div class="icon" :class="{'faction': faction != -1}" :style=" {backgroundImage: getRegionImgUrl}"></div>
</template>

<script>

export default {
    components: {

    },
    data() {
        return {
        }
    },
    mounted() {
    },
    props: {
        faction: Number,
    },
    computed: {
        getRegionImgUrl() {
            if (this.faction == -1) {
                return "none"
            }
            // Remote
            // const regionImageBaseUrl = 'https://painttist.github.io/lor-champ-icons/images/regions/';
            // return "url(" + regionImageBaseUrl + regionID + ".svg)";
            
            // Local
            return "url(" + require('../../assets/images/regions/' + this.faction + ".svg") + ")"
        },
    },
    methods: {
    }
}
</script>

<style scoped>

    .icon {
        
        display: block;
        margin-right: 0;
        margin-left: 0;

        padding: 9px;
        text-align: center;
        /* line-height: 30px; */
        /* vertical-align: middle; */
        width: 18px;
        height: 18px;
        color: white;

        /* background-color: white; */
        

        background-position: 50% 50%;
        background-size: cover;

        /* background-image: url('../assets/images/cards/cropped/01DE012-cropped.png'); */
    }

    .icon.faction {
        opacity: 0.8;
        /* width: 26px; */
        padding: 9px 9px;
        /* padding-left: 0px; */
        filter: brightness(0) invert(1) drop-shadow(0.5px 1px 0.5px rgba(0, 0, 0, 0.1));
        /* box-shadow: 2px 2px 3px -2px black; */
        /* filter: drop-shadow(-2px 2px 1px rgba(43, 38, 27, 0.6)); */
        /* filter: drop-shadow(-0.5px 1px 0.5px white); */
    }

    /* .icon.faction:hover {
        opacity: 1;
        filter: brightness(0) invert(1) drop-shadow(1px 2px 1px rgba(0, 0, 0, 0.6));
    } */

    @media screen and (max-width: 275px) {
        .icon {
            width: 15px;
            height: 15px;
        }
    }

    @media screen and (max-width: 190px) {
        .icon {
            width: 12px;
            height: 12px;
        }
    }

</style>