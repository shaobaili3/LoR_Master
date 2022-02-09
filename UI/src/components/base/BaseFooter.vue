<template>
  <div class="footer">
    <p>Brought to you by <a href="#">FlyingFish</a> & <a href="#">Storm</a></p>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.footer {
  position: absolute;
  bottom: 0px;
  margin-top: 100px;
  margin-bottom: 20px;
}

a {
  color: white;
}

@media only screen and (max-width: 768px) {
  /* For mobile phones: */
  .footer {
    position: relative;
  }
}
</style>
