<template>
    <base-window-controls :title="'Main'" :titleType="'window'"></base-window-controls>
    <div> Main Page</div>
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


</style>