<template>
  <div class="flex justify-center h-full">
    <div class="max-w-xl flex-1 w-0">
      <div class="flex flex-col h-full px-2 sm:px-0 contact-info">
        <p class="title">{{ $t("contact.contactUs") }}</p>
        <div class="contact-details-container">
          <p class="contact-detail"><i class="fab fa-twitter"></i> <span class="text-link" @click="openURL('https://twitter.com/storm_lor')"> @Storm_lor</span></p>
          <p class="contact-detail"><i class="fab fa-twitter"></i> <span class="text-link" @click="openURL('https://twitter.com/FlyingFishLoR')"> @FlyingFishLoR</span></p>
          <p class="contact-detail"><i class="fab fa-qq"></i> <span class="text-link" @click="openURL('https://qm.qq.com/cgi-bin/qm/qr?k=nartXgATr58IXdisbHL4C4vaje8Stssz&jump_from=webapi')"> 939286502</span></p>
          <p class="contact-detail"><i class="fab fa-discord"></i> <span class="text-link" @click="openURL('https://discord.gg/aes45bMjAz')"> LoR Master Discord</span></p>
        </div>
        <div class="footer">
          <p>{{ $t("contact.broughtWithLove") }} <span class="text-link" @click="openURL('https://twitter.com/storm_lor')"> Storm</span> & <span class="text-link" @click="openURL('https://twitter.com/FlyingFishLoR')"> FlyingFish</span></p>
        </div>
        <contact-message-box></contact-message-box>
      </div>
    </div>
  </div>
</template>

<script>
import ContactMessageBox from "../base/ContactMessageBox.vue"
export default {
  components: {
    ContactMessageBox,
  },
  data() {
    return {}
  },
  mounted() {},
  methods: {
    openURL(url) {
      if (window.openExternal) {
        window.openExternal(url)
      } else {
        window.open(url, "_blank").focus()
      }
    },
  },
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
