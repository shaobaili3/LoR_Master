<template>
  <div class="fixed z-[200]">
    <!--Overlay Effect-->
    <div class="fixed inset-0 z-[200] h-full w-full overflow-y-auto bg-gray-900 bg-opacity-50" id="my-modal"></div>

    <div
      class="sm:1/2 fixed top-1/2 left-1/2 z-[250] flex w-full max-w-md -translate-x-1/2 -translate-y-1/2 transform-gpu flex-col items-center justify-start rounded-lg bg-gray-700 text-white shadow-lg md:w-1/3"
    >
      <div class="mt-2 p-2 text-lg font-bold">{{ message }}</div>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: String,
  },
}
</script>
