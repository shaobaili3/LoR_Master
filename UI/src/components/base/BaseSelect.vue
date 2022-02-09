<template>
  <div class="custom-select" :tabindex="tabindex" @blur="open = false">
    <div class="selected" :class="{ open: open }" @click="open = !open">
      {{ swapNames ? swapNames[selectedIndex] : selected }}
    </div>
    <div class="items" :class="{ selectHide: !open }">
      <div v-for="(option, i) of options" :key="i" @click="onOptionClick(option)">
        {{ swapNames ? swapNames[i] : option }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    options: {
      type: Array,
      required: true,
    },
    default: {
      type: String,
      required: false,
      default: null,
    },
    tabindex: {
      type: Number,
      required: false,
      default: 0,
    },
    swapNames: {
      type: Array,
      require: false,
      default: null,
    },
  },
  data() {
    return {
      selected:
        this.default && this.options.length > 0 && this.options.includes(this.default)
          ? this.default
          : this.options.length > 0
          ? this.options[0]
          : null,
      open: false,
    }
  },
  mounted() {
    // console.log(this.swapNames)
    this.$emit("input", this.selected)
  },
  computed: {
    selectedIndex() {
      return this.options.findIndex((val) => val == this.selected)
    },
  },
  methods: {
    onOptionClick(option) {
      this.selected = option
      this.open = false
      this.$emit("input", option)
    },
  },
}
</script>

<style scoped>
.custom-select {
  position: relative;
  width: 200px;
  text-align: left;
  outline: none;
  height: 36px;
  line-height: 36px;
  font-size: 0.9em;
}

.custom-select .selected {
  background-color: var(--col-dark-grey);
  border-radius: 6px;
  /* border: 1px solid #666666; */
  color: #fff;
  padding-left: 1em;
  cursor: pointer;
  user-select: none;
}

.custom-select .selected.open {
  /* border: 1px solid #ad8225; */
  border-radius: 6px 6px 0px 0px;
}

.custom-select .selected:after {
  position: absolute;
  content: "";
  top: 18px;
  right: 1em;
  width: 0;
  height: 0;
  border: 5px solid transparent;
  border-color: #fff transparent transparent transparent;
}

.custom-select .items {
  color: #fff;
  border-radius: 0px 0px 6px 6px;
  overflow: hidden;
  /* border-right: 1px solid #ad8225; */
  /* border-left: 1px solid #ad8225; */
  /* border-bottom: 1px solid #ad8225; */
  position: absolute;
  background-color: var(--col-dark-grey);
  left: 0;
  right: 0;
  z-index: 1;
}

.custom-select .items div {
  color: #fff;
  padding-left: 1em;
  cursor: pointer;
  user-select: none;
}

.custom-select .items div:hover {
  background-color: var(--col-light-grey);
}

.selectHide {
  display: none;
}
</style>
