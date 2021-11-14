<template>
  <div>
    <!--Overlay Effect-->
    <div
      class="fixed inset-0 bg-gray-900 bg-opacity-50 overflow-y-auto h-full w-full z-[200]"
      id="my-modal"
    ></div>

    <div class="z-[250] fixed w-1/2 max-w-md top-1/2 left-1/2 transform-gpu -translate-x-1/2 -translate-y-1/2
    bg-gray-700 shadow-lg flex flex-col items-center justify-start rounded-lg text-white">
      <div class="text-lg font-bold p-2 mt-2">{{message}}</div>
      <slot></slot>
    </div>

  </div>

</template>

<script>
export default {
  props: {
    message: String
  },
}
</script>