<template>
  <div id="menu" class="">
    <router-link to="/" class="menu-item">
      <span><i class="fa fa-home"></i></span>
    </router-link>
    <router-link to="/leaderboard" class="menu-item">
      <span><i class="fa fa-trophy"></i></span>
    </router-link>
    <!-- <router-link to="/profile" class="menu-item">
            <span><i class="fa fa-user"></i></span>
        </router-link> -->
  </div>
</template>

<script>
export default {
  // props: ["name"],
  // components: {
  //   MainLayout
  // }
}
</script>

<style scoped>
#menu {
  display: flex;

  position: fixed;
  top: 0px;
  left: 0px;

  flex-direction: column;
  align-items: center;
  justify-content: center;

  height: 100vh;

  margin-left: 0px;
}

.menu-item {
  display: flex;
  /* border: 1px var(--col-gold)enrod solid; */
  color: var(--col-gold);
  /* background-color:white; */

  width: 80px;
  height: 60px;
  align-items: center;
  justify-content: center;

  font-size: 1.4em;

  /* border-radius: 0px 10px 0px 0px; */

  margin: 10px 0px 10px 0px;
  border-right: 2px solid transparent;
}

.menu-item:hover {
  border-right: 2px solid var(--col-gold);
}

.router-link-active.menu-item {
  color: white;
  border-right: 2px solid var(--col-gold);
}

@media only screen and (max-width: 768px) {
  /* For mobile phones: */
  #menu {
    position: fixed;
    top: auto;
    bottom: 0px;
    left: 0px;

    flex-direction: row;
    align-items: center;
    justify-content: center;

    height: auto;
    width: 100vw;

    margin-left: 0px;

    background-color: var(--col-background);
  }

  .menu-item {
    border-right: none;
    border-top: 2px solid transparent;
    margin: 0px 10px 0px 10px;
  }

  .menu-item:hover {
    border-right: none;
    border-top: 2px solid var(--col-gold);
  }

  .router-link-active.menu-item {
    border-right: none;
    border-top: 2px solid var(--col-gold);
  }
}
</style>
