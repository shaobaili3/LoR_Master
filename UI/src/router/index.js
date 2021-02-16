import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
// import About from '../pages/About.vue'
// import Profile from '../pages/Profile.vue'
// import NotFound from '../pages/404.vue'
// import Leaderboard from '../pages/Leaderboard.vue'


// const routerHistory = createWebHistory('/lor-master-leaderboard/')
const routerHistory = createWebHistory('')
const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    // component: Leaderboard,
  },
  // {
  //   path: "/about",
  //   name: "About",
  //   component: About,
  //   // props: true,
  // },
  // {
  //   path: "/profile",
  //   name: "Profile",
  //   component: Profile,
  // },
  // {
  //   path: "/profile/:name",
  //   name: "ProfileWithName",
  //   component: Profile,
  // },
  // {
  //   path: "/leaderboard",
  //   name: "Leaderboard",
  //   component: Leaderboard,
  //   // props: true,
  // },
  { path: '/:pathMatch(.*)*', 
    name: 'not-found', 
    component: Home },
];

const router = createRouter({
    history: routerHistory,
    routes: routes,
});

router.resolve({
    name: 'not-found',
    params: { pathMatch: ['not', 'found'] },
}).href // '/not/found'

export default router;