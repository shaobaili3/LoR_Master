<template>
  <div class="locale-changer">
    <div class="locale-changer-title">
      {{ title }}
    </div>
    <div class="select-container">
      <!-- <select v-model="$i18n.locale">
        <option v-for="locale in $i18n.availableLocales" :key="`locale-${locale}`" :value="locale">{{ locale }}</option>
      </select> -->
      <base-select :swapNames="swapNames" :options="options" :default="optionDefault" @input="input($event)"></base-select>
    </div>
  </div>
</template>

<script>
import BaseSelect from "./BaseSelect.vue"
export default {
  components: { BaseSelect },
  props: {
    title: String,
    options: Array,
    optionDefault: String,
    input: Function,
    swapNames: Array,
  },
}
</script>

<style>
.locale-changer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

select {
  font-size: 0.9em;
  outline: none;
  background: var(--col-dark-grey);
  color: white;
  padding: 8px 15px;
  border-radius: 40px;
  border: 0px;
  appearance: none;
  cursor: pointer;
}
</style>
