<template>
  <div>
    <div class="absolute top-0 right-0 flex items-center justify-end gap-2 p-1 text-white">
      <a class="hover:no-underline" target="_blank" href="https://discord.gg/aes45bMjAz">
        <div class="flex h-9 items-center justify-center px-2">
          <i class="fab fa-discord" aria-label="Discord"></i>
        </div>
      </a>
      <a class="hover:no-underline" target="_blank" href="https://github.com/shaobaili3/LoR_Master">
        <div class="flex h-9 items-center justify-center px-2">
          <i class="fab fa-github" aria-label="Github"></i>
        </div>
      </a>
      <a class="hover:no-underline" target="_blank" href="https://twitter.com/storm_lor">
        <div class="flex h-9 items-center justify-center px-2">
          <i class="fab fa-twitter" aria-label="Twitter"></i>
        </div>
      </a>
      <a class="hover:no-underline" target="_blank" href="https://lormaster.com">
        <div class="flex h-9 items-center justify-center rounded-md bg-gold-400 px-4 text-gray-900 hover:bg-gold-300">
          <i class="fas fa-download pr-2" aria-label="Download"></i>
          {{ $t("str.tracker") }}
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style></style>
