<template>
  <div class="contact-message-box">
    <textarea
      spellcheck="false"
      rows="3"
      autocomplete="off"
      type="text"
      class="input-textarea"
      :class="{ doubleCheck: doubleCheck }"
      v-model="message"
      :placeholder="$t('contact.messageBox.placeholder')"
      @keyup="onKeyUp"
    ></textarea>
    <div class="flex">
      <div
        class="pl-2 text-sm"
        :class="{ 'text-gray-500': message.length <= maxCharLimit, 'text-orange-600': message.length > maxCharLimit }"
      >
        {{ message.length }}
      </div>
      <button class="mt-1 send-btn" :class="{ active: message != '', doubleCheck: doubleCheck }" @click="sendMessage">
        <span v-if="messageSending">{{ $t("contact.messageBox.messageSending") }} <i class="fas fa-spin fa-spinner-third"></i></span>
        <span v-else-if="messageSent">{{ $t("contact.messageBox.messageSent") }} <i class="fas fa-check"></i></span>
        <span v-else-if="doubleCheck">{{ $t("contact.messageBox.confirm") }}</span>
        <span v-else>{{ $t("contact.messageBox.send") }}</span>
      </button>
    </div>
    <div v-if="errorMessage.length > 0" class="text-orange-600">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import axios from "axios"
import { ref } from "vue"
import { useStatusStore } from "../../store/StoreStatus"
import { useBaseStore } from "../../store/StoreBase"

const baseStore = useBaseStore()
const statusStore = useStatusStore()

const maxCharLimit = 3000

const message = ref("")
const doubleCheck = ref(false)
const messageSent = ref(false)
const messageSending = ref(false)

const errorMessage = ref("")

function onKeyUp() {
  doubleCheck.value = false
  messageSent.value = false
  messageSending.value = false
}

function validate() {
  return message.value.length <= maxCharLimit
}

function handleMessageError(err) {
  errorMessage.value = err
}

function postRequest() {
  // const reportURL = `${this.API_WEB}/report/${encodeURIComponent(message.value)}`
  var reportUrl = `${baseStore.API_WEB}/feedback`
  axios
    .post(reportUrl, {
      time: Date.now(),
      platform: baseStore.IS_ELECTRON ? "electron" : "web",
      lor_running: statusStore.lorRunning,
      local_api_enabled: statusStore.localApiEnabled,
      server: statusStore.localServer,
      player_id: statusStore.localPlayerID,
      message: message.value,
    })
    .then((response) => {
      console.log("Send Report Success")
      handleMessageSent()
    })
    .catch((err) => {
      console.log(err)
      handleMessageError(err.toString())
    })
}

function sendMessage() {
  if (!validate()) {
    handleMessageError(`Max length exceeded ${maxCharLimit}`)
    return
  }

  if (doubleCheck.value) {
    postRequest()
    handleMessageSending()
  } else if (message.value != "") {
    doubleCheck.value = true
  }
}

function handleMessageSending() {
  doubleCheck.value = false
  messageSending.value = true
}

function handleMessageSent() {
  doubleCheck.value = false
  messageSending.value = false
  messageSent.value = true
  message.value = ""
}

function openURL(url) {
  window.openExternal(url)
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
