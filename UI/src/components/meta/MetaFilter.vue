<template>
  <!-- Meta Search Bar -->
  <div class>
    <!-- Tag Box -->
    <div class="relative pb-4">
      <i class="absolute text-base fas fa-filter left-4 top-3.5" :class="{ 'text-gray-200': !(tags.length > 0) }"></i>
      <ul
        class="flex flex-wrap items-center w-full gap-2 pl-12 pr-12 bg-gray-800"
        :class="{ 'rounded-[40px]': !hasAutoComplete, ' rounded-t-[25px]': hasAutoComplete }"
      >
        <MetaFilterTags
          class="h-[50px] flex items-center"
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
          class="flex-1 h-[50px] outline-0 bg-gray-800/0"
          type="text"
          @keyup.up="autoCompleteIndexMinus"
          @keyup.down="autoCompleteIndexPlus"
          :placeholder="$t('filter.placeHolder')"
        />
        <button class="search-btn inside right" @click="clearTags" v-if="tags.length > 0">
          <span><i class="fas fa-times"></i></span>
        </button>
      </ul>

      <!-- Auto Complete -->
      <div v-if="hasAutoComplete" class="absolute z-10 w-full text-left bg-gray-800 pb-5 rounded-b-[25px]">
        <div
          v-for="(item, index) in autoCompleteItems"
          class="relative px-12 cursor-pointer hover:bg-gray-700"
          :class="{ 'bg-gray-700': autoCompleteIndex == index }"
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
          <div class="flex items-center h-9" v-if="!item.code">
            <RegionIcon class="w-6 h-6 mr-1" v-if="item.factionID" :faction="item.factionID" :colored="true" :fixedSize="false"></RegionIcon
            >{{ item.name }}
          </div>
          <!-- Guide -->
          <div class="absolute top-0 items-center hidden h-full text-gray-200 right-4" :class="{ 'sm:flex': autoCompleteIndex == index }">
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
import { ref, defineEmits, computed } from "vue"
import MetaFilterTags, { TAG_TYPES } from "./MetaFilterTags.vue"

import { useBaseStore } from "../../store/StoreBase"
import CardPreview from "../deck/CardPreview.vue"
const baseStore = useBaseStore()

const autoCompleteItems = ref([])

const filterInput = ref(null)

const tags = ref([])

const hasAutoComplete = computed(() => {
  return autoCompleteItems.value.length > 0
})

const emits = defineEmits(["updateFilter"])

function emitFilter() {
  emits("updateFilter", tags.value)
}

function clearTags() {
  tags.value = []
  emitFilter()
}

function addACToFilter(item) {
  addItemToTags(item)
  filterInput.value.value = ""
  generateAutoComplete("")
}

import { factionNames } from "../panels/PanelDeckCode.vue"
import RegionIcon from "../image/RegionIcon.vue"

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
      emitFilter()
    }
  } else if (item.name) {
    if (!tags.value.includes(item.name)) {
      tags.value.push(item.name)
      emitFilter()
    }
  } else {
    if (!tags.value.includes(item)) {
      tags.value.push(item)
      emitFilter()
    }
  }
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
        emitFilter()
      }
      console.log(tags.value)
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
  emitFilter()
}
</script>
