<template>
  <div>
    <div class="absolute top-0 right-0 p-1 text-white flex justify-end items-center gap-2">
      <a class="hover:no-underline" target="_blank" href="https://github.com/shaobaili3/LoR_Master" >
        <div class="h-9  flex justify-center items-center px-2">
          <i class="fab fa-github"></i>
        </div>
      </a>
      <a class="hover:no-underline" target="_blank" href="https://twitter.com/storm_lor" >
        <div class="h-9  flex justify-center items-center px-2 ">
          <i class="fab fa-twitter"></i>
        </div>
      </a>
      <a class="hover:no-underline" target="_blank" href="https://lormaster.com" >
        <div class="h-9 flex justify-center items-center px-4 text-gray-900 bg-gold-400 rounded-md hover:bg-gold-300">
          <i class="fas fa-download pr-2"></i> {{$t('str.tracker')}}
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>