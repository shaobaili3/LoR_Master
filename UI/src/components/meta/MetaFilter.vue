<template>
  <!-- Meta Search Bar -->
  <div class>
    <!-- Tag Box -->
    <div class="relative pb-4">
      <i
        class="fas fa-filter absolute left-5 top-4"
        :class="{ 'text-gray-200': !(tags.length > 0) }"
        @click="
          () => {
            emits('refresh')
          }
        "
      ></i>
      <ul
        class="flex w-full flex-wrap items-center gap-2 bg-gray-800 pl-12 pr-12 transition-colors focus-within:bg-gray-700"
        :class="{
          'rounded-[40px]': !hasAutoComplete,
          ' rounded-t-[25px]': hasAutoComplete,
        }"
      >
        <MetaFilterTags
          class="flex h-12 items-center"
          v-for="(tag, index) in tags"
          :key="tag"
          :content="tag"
          :index="index"
          :type="TAG_TYPES.string"
          @delete="handleDeleteTag"
        ></MetaFilterTags>
        <input
          @keyup="onKeyUp"
          @keydown="onKeyDown"
          ref="filterInput"
          class="h-12 flex-1 bg-gray-800/0 placeholder-gray-300 outline-0"
          type="text"
          @keyup.up="autoCompleteIndexMinus"
          @keyup.down="autoCompleteIndexPlus"
          :placeholder="$t('filter.placeHolder')"
        />
        <button class="search-btn inside right" @click="clearTags" v-if="tags.length > 0">
          <span><i class="fas fa-times"></i></span>
        </button>
      </ul>
      <slot></slot>

      <!-- Auto Complete -->
      <div
        v-if="hasAutoComplete"
        class="absolute z-10 w-full rounded-b-[25px] bg-gray-800 pb-5 text-left"
      >
        <div
          v-for="(item, index) in autoCompleteItems"
          class="relative mb-1 cursor-pointer px-12 hover:bg-gray-600"
          :class="{ 'bg-gray-700 ': autoCompleteIndex == index }"
          :key="item"
          @click="addACToFilter(item)"
        >
          <CardPreview
            v-if="item.code"
            :noPreview="true"
            :noCost="true"
            :code="item.code"
            :set="item.set"
            :typeRef="item.typeRef"
          ></CardPreview>
          <div class="flex h-9 items-center" v-if="!item.code">
            <IconRegion
              class="mr-1 h-6 w-6"
              v-if="item.factionID"
              :faction="item.factionID"
              :colored="true"
              :fixedSize="false"
            ></IconRegion
            >{{ item.name }}
          </div>
          <!-- Guide -->
          <div
            class="absolute top-0 right-4 hidden h-full items-center text-gray-200"
            :class="{ 'sm:flex': autoCompleteIndex == index }"
          >
            ↵ Enter
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export const getTypeRefFromCard = (card) => {
  var typeRef = ""
  if (card.supertype != "" || card.rarityRef == "Champion") {
    typeRef = "Champion"
  } else if (card.spellSpeedRef != "") {
    typeRef = "Spell"
  } else if (card.keywordRefs && card.keywordRefs.includes("LandmarkVisualOnly")) {
    typeRef = "Landmark"
  } else {
    typeRef = "Unit"
  }
  return typeRef
}
</script>

<script setup>
import { ref, computed, onMounted } from "vue"
import MetaFilterTags, { TAG_TYPES } from "./MetaFilterTags.vue"

import { useBaseStore } from "../../store/StoreBase"
import CardPreview from "../deck/CardPreview.vue"

import { factionNames } from "../../modules/constants.js"
import IconRegion from "../image/IconRegion.vue"

const baseStore = useBaseStore()
const autoCompleteItems = ref([])
const filterInput = ref(null)
const tags = ref([])

const metaFilterStorageID = "lmt-settings-meta-filter"

onMounted(() => {
  let oldFilter = window.localStorage.getItem(metaFilterStorageID)
  if (oldFilter) {
    tags.value = JSON.parse(oldFilter)
  }
  emits("bindFilter", tags.value)
})

const hasAutoComplete = computed(() => {
  return autoCompleteItems.value.length > 0
})

const emits = defineEmits(["bindFilter", "refresh"])

function saveToLocalStorage() {
  window.localStorage.setItem(metaFilterStorageID, JSON.stringify(tags.value))
}

function clearTags() {
  tags.value.splice(0, tags.value.length)
  saveToLocalStorage()
}

function addACToFilter(item) {
  addItemToTags(item)
  filterInput.value.value = ""
  generateAutoComplete("")
}

function generateAutoComplete(val) {
  let newList = []

  if (val != "") {
    // Not pure english => Localizaed string
    if (/[^a-zA-Z]/.test(val)) {
      for (const card of baseStore.sets) {
        if (!card.collectible || card.cardCode.length > 7) continue

        if (card.name.toLowerCase().includes(val.toLowerCase())) {
          let typeRef = getTypeRefFromCard(card)
          newList.push({
            name: card.name,
            code: card.cardCode,
            set: card.set,
            typeRef,
          })
        }

        if (newList.length > 5) break
      }
    } else {
      for (const key in baseStore.sets_en) {
        let card = baseStore.sets_en[key]

        if (!card.collectible || card.cardCode.length > 7) continue

        if (card.name.toLowerCase().includes(val.toLowerCase())) {
          let typeRef = getTypeRefFromCard(card)
          newList.push({
            name: card.name,
            code: card.cardCode,
            set: card.set,
            typeRef,
          })
        }
        if (newList.length > 5) break
      }

      for (const key in factionNames) {
        let faction = factionNames[key]
        if (faction.toLowerCase().includes(val.toLowerCase())) {
          newList.push({
            name: faction,
            factionID: key,
          })
        }
        if (newList.length > 7) break
      }
    }
  }

  newList.sort((a, b) => {
    if (a.typeRef > b.typeRef) {
      return 1
    } else if (a.typeRef == b.typeRef)
      if (a.name > b.name) {
        return 1
      }
    return -1
  })

  autoCompleteItems.value = newList
  checkACIndexBounds()
}

function addItemToTags(item) {
  if (item.code) {
    if (!tags.value.includes(item.code)) {
      tags.value.push(item.code)
    }
  } else if (item.name) {
    if (!tags.value.includes(item.name)) {
      tags.value.push(item.name)
    }
  } else {
    if (!tags.value.includes(item)) {
      tags.value.push(item)
    }
  }
  saveToLocalStorage()
}

function onKeyUp(e) {
  let val = e.target.value
  if (e.key == "Enter") {
    let AC = autoCompleteItems.value[autoCompleteIndex.value]
    if (AC) {
      addItemToTags(AC)
    } else {
      let tag = val.trim()
      // Make sure tag is not empty
      if (tag) {
        tag.split(",").forEach((tag) => {
          if (!tags.value.includes(tag)) {
            tags.value.push(tag)
          }
        })
        saveToLocalStorage()
      }
    }

    e.target.value = ""
    generateAutoComplete("")
    return
  }

  generateAutoComplete(val)
}

function onKeyDown(e) {
  let val = e.target.value
  if (e.key == "Backspace") {
    // Handle deleting tags using backspace
    if (val == "") {
      tags.value.pop()
      saveToLocalStorage()
    }
  }

  if (e.key == "ArrowUp" || e.key == "ArrowDown") {
    e.preventDefault()
  }
}

const autoCompleteIndex = ref(0)

function autoCompleteIndexPlus() {
  autoCompleteIndex.value += 1
  checkACIndexBounds()
}
function autoCompleteIndexMinus() {
  autoCompleteIndex.value -= 1
  checkACIndexBounds()
}

function checkACIndexBounds() {
  if (autoCompleteIndex.value > autoCompleteItems.value.length - 1) {
    autoCompleteIndex.value = 0
  }
  if (autoCompleteIndex.value < 0) {
    autoCompleteIndex.value = autoCompleteItems.value.length - 1
  }
}

function handleDeleteTag(index) {
  tags.value.splice(index, 1)
  saveToLocalStorage()
}
</script>
