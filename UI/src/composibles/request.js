import { ref, onMounted, onUnmounted, isRef } from "vue"

import axios from "axios"

export function useRequest(api) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const controller = ref(null)
  const duration = ref(0)
  const cancel = () => {
    if (controller.value) controller.value.abort()
  }

  const fetch = () => {
    if (loading.value) cancel()
    controller.value = new AbortController()
    loading.value = true
    const reqeustStartTime = Date.now()
    const requestAPi = isRef(api) ? api.value : api
    console.log(requestAPi)
    axios
      .get(requestAPi, { signal: controller.value.signal })
      .then((res) => {
        loading.value = false
        if (res && res.data) {
          error.value = null
          duration.value = Date.now() - reqeustStartTime
          data.value = res.data
        } else {
          error.value = `API ${requestAPi} response invalid`
        }
      })
      .catch((e) => {
        if (axios.isCancel(e)) {
          console.log(`API ${requestAPi} request cancelled`)
        } else {
          loading.value = false
          error.value = e
        }
      })
  }

  // expose managed state as return value
  return { data, loading, duration, error, fetch, cancel }
}
