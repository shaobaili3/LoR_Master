<template>
    <div class="contact-message-box">
        <textarea spellcheck="false" rows="3" autocomplete='off' type="text" 
            class="input-textarea"
            :class="{doubleCheck: doubleCheck}"
            v-model="message"
            :placeholder="$t('contact.messageBox.placeholder')"
            @keyup="checkInput"
        ></textarea>
        <button class="send-btn" 
            :class="{active: message!='', doubleCheck: doubleCheck}"
            @click="sendMessage">
            <span v-if="messageSent">{{$t('contact.messageBox.messageSent')}} <i class="fas fa-check"></i></span>
            <span v-if="doubleCheck && !messageSent">{{$t('contact.messageBox.confirm')}}</span>
            <span v-if="!doubleCheck && !messageSent">{{$t('contact.messageBox.send')}}</span>
        </button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    components: {

    },
    data() {
        return {
            message: "",
            doubleCheck: false,
        }
    },
    mounted() {
    },
    methods: {
        checkInput() {
            this.doubleCheck = false
            this.messageSent = false
        },
        sendMessage() {
            if (this.doubleCheck) {
                var reportUrl = `${this.API_WEB}/report/${encodeURIComponent(this.message)}`
                console.log('Sending url', reportUrl)
                axios.get(reportUrl).then((response) => {
                    console.log("Send Report Success")
                }).catch(err => {console.log(err)})

                this.handleMessageSent()
            } else if (this.message != "") {
                this.doubleCheck = true
            }
        },
        handleMessageSent() {
            this.doubleCheck = false
            this.messageSent = true
            this.message = ""
        },
        openURL(url) {
            window.openExternal(url);
        },
    }
}
</script>

<style scoped>

    .contact-message-box {
        font-size: 16px;
    }

    .text-link {
        text-decoration: underline;
        cursor: pointer;
    }

    .input-textarea {
        width: 100%;

        margin-top: 20px;
        padding: 10px;
        
        background-color: var(--col-darker-grey);
        color: white;
        
        outline: 0px;
        border: 0px;
        border-radius: 6px;

        font-size: inherit;
        box-sizing: border-box;
        resize: none;

        transition: background-color 0.35s ease;
    }

    .input-textarea:focus {
        background-color: var(--col-dark-grey);
    }

    .send-btn {
        display: block;
        min-height: 30px;
        min-width: 50px;
        
        margin-top: 8px;
        margin-left: auto;
        padding: 8px 15px;

        background-color: var(--col-dark-grey);
        color: var(--col-dark-white);
        
        outline: 0px;
        border: 0px;
        border-radius: 6px;

        font-size: inherit;

        transition: background-color 0.35s ease;
    }

    .send-btn.active {
        cursor: pointer;
        color: white;
    }

    .send-btn.active:hover {
        background-color: var(--col-light-grey);
    }

    .send-btn.active.doubleCheck {
        background-color: var(--col-gold);
    }


</style>