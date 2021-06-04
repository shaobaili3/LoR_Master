<template>
    <base-window-controls :title="'Info'" :titleType="'window'"></base-window-controls>
    <div id="content">
        <p>Brought to you by</p>
        <p>
            <span class="text-link" @click="openURL('https://twitter.com/FlyingFishLoR')">
                FlyingFish</span> & 
            <span class="text-link" @click="openURL('https://twitter.com/storm_lor')">Storm</span>
        </p>
    </div>
</template>

<script>
import BaseWindowControls from '../../components/BaseWindowControls.vue';
export default {
    components: { BaseWindowControls },
    methods: {
        openURL(url) {
            window.openExternal(url);
        }
    }
}
</script>

<style scoped>
    .text-link {
        text-decoration: underline;
        cursor: pointer;
    }

    #content {
        text-align: center;
        display: block;
        width: 100%;
        margin-top: 43px;
        padding: 10px;
        box-sizing: border-box;
        white-space: normal;
    }

/* 
    .content {
        background-color: var(--col-background);
    }

    p {
        color: white;
    } */
</style>