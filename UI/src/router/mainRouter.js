import PanelSettings from "../components/panels/PanelSettings.vue"
import PanelSearch from "../components/panels/PanelSearch.vue"
import PanelProfile from "../components/panels/PanelProfile.vue"
import PanelMeta from "../components/panels/PanelMeta.vue"
import PanelDeckLib from "../components/panels/PanelDeckLib.vue"
import PanelDeckCode from "../components/panels/PanelDeckCode.vue"
import PanelLeaderboard from "../components/panels/PanelLeaderboard.vue"
import ContactInfo from "../components/panels/PanelContact.vue"

import PanelTest from "../components/panels/PanelTest.vue"

import PanelPolicyPrivacy from "../components/panels/PanelPolicyPrivacy.vue"
import PanelPolicyTOS from "../components/panels/PanelPolicyTOS.vue"
import PanelSeasonal from "../components/panels/PanelSeasonal.vue"

export default [
  {
    name: "home",
    path: "/",
    component: PanelLeaderboard,
    meta: {
      title: "Home | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "Your LoR companion, Leaderboard, Meta, History, Stats, Mulligan and many more!",
        },
        {
          property: "og:description",
          content: "Your LoR companion, Leaderboard, Meta, History, Stats, Mulligan and many more!",
        },
      ],
    },
  },
  {
    name: "settings",
    path: "/settings",
    component: PanelSettings,
    meta: {
      title: "Settings | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "Adjust langauge & preferences for LoR Master Web App",
        },
        {
          property: "og:description",
          content: "Your LoR companion, Leaderboard, Meta, History, Stats, Mulligan and many more!",
        },
      ],
    },
  },
  {
    name: "search",
    path: "/search",
    component: PanelSearch,
    meta: {
      title: "Player Search | LoR Master App",
      metaTags: [
        {
          name: "description",
          content:
            "History & stats search for anyone playing LoR. Discover & bookmark top players or friends!",
        },
        {
          property: "og:description",
          content:
            "History & stats search for anyone playing LoR. Discover & bookmark top players or friends!",
        },
      ],
    },
    props: (route) => ({
      player: route.query.name,
      region: route.query.region,
      tag: route.query.tag,
    }),
  },
  {
    name: "profile",
    path: "/profile",
    component: PanelProfile,
    meta: {
      title: "Player Profile | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "View player history, winrate, archetypes & more!",
        },
        {
          property: "og:description",
          content: "View player history, winrate, archetypes & more!",
        },
      ],
    },
  },
  {
    name: "meta",
    path: "/meta",
    component: PanelMeta,
    meta: {
      title: "Meta Environment | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "View matchup statistics. Discover hidden gems, best builds and meta trends!",
        },
        {
          property: "og:description",
          content: "View matchup statistics. Discover hidden gems, best builds and meta trends!",
        },
      ],
    },
  },
  {
    name: "seasonal",
    path: "/seasonal",
    component: PanelSeasonal,
    meta: {
      title: "Seasonal | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "View seasonal statistics. Discover hidden gems, best builds and meta trends!",
        },
        {
          property: "og:description",
          content: "View seasonal statistics. Discover hidden gems, best builds and meta trends!",
        },
      ],
    },
  },
  {
    name: "decklib",
    path: "/library",
    component: PanelDeckLib,
    meta: {
      title: "Deck Library | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "Quickly save your favourite decks and use them later!",
        },
        {
          property: "og:description",
          content: "Quickly save your favourite decks and use them later!",
        },
      ],
    },
  },
  {
    name: "code",
    path: "/code",
    component: PanelDeckCode,
    props: (route) => ({ code: route.query.code }),
    meta: {
      title: "Deck Detail | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "Detail and statistics about decks.",
        },
        {
          property: "og:description",
          content: "View matchup statistics. Discover hidden gems, best builds and meta trends!",
        },
      ],
    },
  },
  {
    name: "leaderboard",
    path: "/leaderboard",
    component: PanelLeaderboard,
    meta: {
      title: "Leaderboard | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "Discover top players, rising stars & meta kings!",
        },
        {
          property: "og:description",
          content: "Discover top players, rising stars & meta kings!",
        },
      ],
    },
  },
  {
    name: "contact",
    path: "/contact",
    component: ContactInfo,
    meta: {
      title: "Contact | LoR Master App",
      metaTags: [
        {
          name: "description",
          content: "Contact LoR Master dev team for support & feedbacks.",
        },
      ],
    },
  },
  {
    name: "test",
    path: "/test",
    component: PanelTest,
  },
  {
    path: "/terms-of-service",
    component: PanelPolicyTOS,
  },
  {
    path: "/privacy",
    component: PanelPolicyPrivacy,
  },
]
