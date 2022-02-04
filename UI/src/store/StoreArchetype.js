import axios from "axios"

import { defineStore } from "pinia"
import { useBaseStore } from "./StoreBase"

export const useArchetypeStore = defineStore("archetype", {
  state: () => {
    return {
      archetypeDetails: {},
      archetypeController: null,
      archetypeLoading: true,
      archetypeRequestTime: null,
      archetypeError: null,
    }
  },
  actions: {
    cancelRequest() {
      if (this.archetypeController) this.archetypeController.abort()
    },
    fetchArchetypeDetail(deckID) {
      this.archetypeRequestTime = Date.now()
      this.archetypeLoading = true

      this.cancelRequest()

      const baseStore = useBaseStore()
      var api = `${baseStore.API_WEB}/archetype/${encodeURIComponent(deckID)}`

      // console.log("Request Archetype", api)

      const controller = new AbortController()
      this.archetypeController = controller
      var promise = axios.get(api, { signal: controller.signal })

      promise
        .then((res) => {
          this.archetypeLoading = false
          if (res && res.data && res.data.data) {
            // Item wrapped in data: { _id: 1 , data: {}, time: "" }
            this.archetypeDetails[deckID] = res.data.data
          } else {
            throw Error("Archetype API response invalid")
          }
        })
        .catch((e) => {
          console.log("error", e)
          this.archetypeError = e
        })
    },
  },
})
