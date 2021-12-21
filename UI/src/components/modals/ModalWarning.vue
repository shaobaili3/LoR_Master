<template>
  <!-- <teleport to="body"> -->
    <transition name="fade">
      <modal :message="$t('str.requestConfirm')" v-if="opened">
        <div class="text-sm px-4 py-4 whitespace-pre text-center">{{message}}</div>
        <div class="buttons mt-auto mb-2">
          <button @click="onConfirmBtn" class="p-2 px-8 btn-default btn-actions btn-primary rounded-md h-18">
            <div class="flex items-center justify-center ">
              <i class="fas fa-check "></i>
            </div>
            {{$t('str.yes')}}
          </button>
          <button  @click="onLaterBtn" class="p-2 px-8 btn-default btn-actions btn-secondary rounded-md h-18">
            <div class="flex items-center justify-center ">
              <i class="fas fa-times"></i>
            </div>
            {{$t('str.no')}}
          </button>
        </div>
      </modal>
    </transition>
  <!-- </teleport> -->
  
</template>

<script>
import Modal from './Modal.vue'
export default {
  components: {
    Modal
  },
  data() {
    return {
      opened: false,
      callbacks: null,
      message: null,
    }
  },
  computed: {
  },
  methods: {
    onConfirmBtn(event) {
      if (this.callbacks && this.callbacks[0]) {
        this.callbacks[0]()
      }
      this.hidePanel()
    },
    onLaterBtn(event) {
      if (this.callbacks && this.callbacks[1]) {
          this.callbacks[1]()
        }
      this.hidePanel()
    },
    showPanel(callbacks, message) {
      this.opened = true
      this.callbacks = callbacks
      this.message = message
    },
    hidePanel() {
      this.opened = false
      this.callbacks = null
    }
  }
}
</script>