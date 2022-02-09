<template>
  <div>
    <div>Sign In</div>
    <div
      id="g_id_onload"
      data-client_id="536594918559-mihfo859ua1e42nte95mrni6e3jdk683.apps.googleusercontent.com"
      data-callback="onSignIn"
      date-login-uri=""
      data-auto_prompt="false"
    ></div>
    <div
      class="g_id_signin"
      data-type="standard"
      data-size="large"
      data-theme="outline"
      data-text="sign_in_with"
      data-shape="rectangular"
      data-logo_alignment="left"
    ></div>
  </div>
</template>

<script></script>

<script setup>
import { onMounted } from "vue"

onMounted(() => {
  window.onSignIn = (googleUser) => {
    console.log("Succesfully Singed in!!!", googleUser)
  }
  let gsi = document.createElement("script")
  gsi.setAttribute("src", "https://accounts.google.com/gsi/client")
  document.head.appendChild(gsi)
})
</script>
