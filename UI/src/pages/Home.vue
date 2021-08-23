<template>

    <div class="left-nav"></div>
    
    <base-window-controls :title="''" :titleType="'window'"></base-window-controls>
    
    <div class="content">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Esse debitis consequatur officia eveniet doloremque voluptatum minus cumque, fugit quod necessitatibus nobis iure eius itaque, ab quam ex sed obcaecati earum!
    </div>

    <div class="bottom-bar">
        <div class="left">
            <div class="version">Status: Fine</div>
        </div>
        <div class="right">
            <div class="version">v0.9.3 Beta</div>
        </div>
    </div>
</template>

<script>

import BaseWindowControls from '../components/BaseWindowControls.vue'

export default {
    mounted() {
        console.log("Mounted")
    },
    data() {
        return {
            // rawDataString: null,
        }
    },
    computed: {
    },
    components: { 
        BaseWindowControls,
    },
    methods: {
    }

}

</script>

<style scoped>

    .content {
        text-align: center;
        display: block;
        width: calc(100% - 80px);
        margin-left: 80px;
        margin-top: 43px;
        padding: 10px 40px;
        box-sizing: border-box;
        white-space: normal;

        color: white;
    }

    .left-nav {
        position: absolute;
        top: 0;
        left: 0;
        width: 80px;
        height: 100vh;
        background: #282828;
        z-index: 5;
    }

    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 45px;
        background: #383838;
        z-index: 6;

        display: flex;
        justify-content: space-between;
        align-items: center;

        color: white;
    }

    .bottom-bar .left, .bottom-bar .right {
        padding: 20px;
    }

</style>