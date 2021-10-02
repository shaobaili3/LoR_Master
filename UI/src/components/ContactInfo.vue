<template>
    <div class="contact-info">
        <p class="title">{{$t('contact.contactUs')}}</p>
        <div class="contact-details-container">
            <p class="contact-detail"><i class="fab fa-twitter"></i> <span class="text-link" @click="openURL('https://twitter.com/storm_lor')">
            @Storm_lor</span></p>
            <p class="contact-detail"><i class="fab fa-twitter"></i> <span class="text-link" @click="openURL('https://twitter.com/FlyingFishLoR')">
            @FlyingFishLoR</span></p>
            <p class="contact-detail"><i class="fab fa-qq"></i> <span class="text-link" @click="openURL('https://qm.qq.com/cgi-bin/qm/qr?k=nartXgATr58IXdisbHL4C4vaje8Stssz&jump_from=webapi')">
            939286502</span></p>
        </div>
        <div class="footer">
            <p>{{$t('contact.broughtWithLove')}} 
                <span class="text-link" @click="openURL('https://twitter.com/storm_lor')">
                Storm</span> & <span class="text-link" @click="openURL('https://twitter.com/FlyingFishLoR')">
                FlyingFish</span>
            </p>
        </div>
        <contact-message-box :locale="locale" :apiBase="apiBase"></contact-message-box>
        
    </div>
</template>

<script>
import ContactMessageBox from './ContactMessageBox.vue';
export default {
    components: {
        ContactMessageBox

    },
    data() {
        return {}
    },
    props: {
        locale: {
            type: String,
            default: 'en_us'
        },
        apiBase: {
            type: String,
            required: true
        }
    },
    mounted() {
        
    },
    methods: {
        openURL(url) {
            window.openExternal(url);
        },
    }
}
</script>

<style scoped>
    .text-link {
        /* text-decoration: underline; */
        background-color: var(--col-dark-grey);
        padding: 3px 6px;
        border-radius: 6px;
        font-size: 0.95em;

        cursor: pointer;
    }

    .text-link:hover {
        background-color: var(--col-light-grey);
    }

    .title {
        font-size: 32px;
        text-align: left;
        padding: 10px 0px 20px 0px;
    }

    .contact-details-container {
        text-align: left;
    }
    
    .contact-detail {
        padding: 4px 0px;
    }

    .contact-detail .fab {
        width: 20px;
        text-align: center;
    }

    .footer {
        margin-top: 40px;
    }

</style>