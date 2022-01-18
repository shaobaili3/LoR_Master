import {
  REGION_ID, REGION_SHORTS, REGION_NAMES
} from "../../components/leaderboard/Leaderboard.vue"

const requestLeaderboardWaitTime = 1000 // ms

import axios from 'axios'

export default {
  namespaced: true,
  state() {
    return {
      request: null,
      leaderboard: null,
      lastRequestTime: null,
      isLoading: false,
    };
  },
  getters: {
  },
  mutations: {
    setLeaderboard(state, {regionID, data}) {
      if (!state.leaderboard) state.leaderboard = []
      state.leaderboard[regionID] = data;
    },
    setLastRequestTime(state, time) {
      state.lastRequestTime = time
    },
    setIsLoading(state, isLoading) {
      state.isLoading = isLoading
    }
  },
  actions: {
    cancelLeaderboard({ state }) {
      state.request.cancel();
    },
    fetchLeaderboard({ commit, state, rootState, dispatch }, regionID) {
      commit('setLastRequestTime', Date.now())
      commit('setIsLoading', true)

      var region = REGION_NAMES[regionID];

      if (!region) return // if region is undefined

      if (state.request) dispatch('cancelLeaderboard');
      const axiosSource = axios.CancelToken.source();
      state.request = { cancel: axiosSource.cancel, msg: "Loading..." };

      var api_link = `${rootState.API_WEB}/leaderboard/${region}`;

      axios
        .get(api_link, { cancelToken: axiosSource.token })
        .then((res) => {
          // this.rawPlayers = res.data;
          commit('setIsLoading', false)
          commit('setLeaderboard', {regionID: regionID, data: res.data});
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled");
          } else {
            console.log("error", e);
            var elapsedTime = Date.now() - state.lastRequestTime; // ms
            if (elapsedTime > requestLeaderboardWaitTime) {
              setTimeout(() => {
                dispatch('fetchLeaderboard', regionID)
              }, 100);
            } else {
              setTimeout(() => {
                dispatch('fetchLeaderboard', regionID)
              }, requestLeaderboardWaitTime - elapsedTime)
            }
          }
        });
    },
  },
};
