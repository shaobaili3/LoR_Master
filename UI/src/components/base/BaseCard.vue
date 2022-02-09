<template>
  <router-link class="card" :to="to">
    <div class="card-title">
      <slot></slot>
    </div>
    <span class="icon">
      <i class="fa fa-trophy"></i>
    </span>
  </router-link>
</template>

<script>
export default {
  props: {
    to: String,
  },
}
</script>

<style scoped>
.card {
  width: 100px;
  height: 100px;
  padding: 20px;
  background: var(--col-light-grey);
  color: white;
  text-decoration: none;
  display: flex;
  /* flex-wrap: wrap; */
  flex-direction: column;
  align-items: center;
  border-radius: 10px;
}

.card:hover {
  color: var(--col-gold);
}

.card-title {
  display: block;
  /* flex-basis: 1; */
}

.icon {
  display: block;
  margin-top: 20px;
  font-size: 2.5em;
  /* flex-basis: 1; */
}
</style>
