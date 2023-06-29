import { getDecodedDeck } from "./getDecodedDeck"
import { useBaseStore } from "../store/StoreBase"
import { regionRefID } from "./constants"

const getFactions = (code) => {
  const baseStore = useBaseStore()
  var cards = getDecodedDeck(code)
  if (!cards) return null

  const getChampFactions = () => {
    var champFactions = []
    for (var j in cards) {
      // First loop to get missing regions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef == "Champion" &&
        card.regions &&
        card.regions.length == 1 && // Only considers mono region cards
        card.collectible
      ) {
        var regionID = regionRefID[card.regionRefs[0]]

        if (card.name == "Bard") {
          regionID = regionRefID.Bard
        } else if (card.name == "Jhin") {
          regionID = regionRefID.Jhin
        } else if (card.name == "Evelynn") {
          regionID = regionRefID.Evelynn
        } else if (card.name == "Jax") {
          regionID = regionRefID.Jax
        } else if (card.name == "Kayn") {
          regionID = regionRefID.Kayn
        } else if (card.name == "Varus") {
          regionID = regionRefID.Varus
        } else if (card.name == "Aatrox") {
          regionID = regionRefID.Aatrox
        } else if (card.name == "Ryze") {
          regionID = regionRefID.Ryze
        } else if (card.name == "Neeko") {
          regionID = regionRefID.Neeko
        } else if (card.name == "The Poro King") {
          regionID = regionRefID.PoroKing
        }

        if (champFactions.indexOf(regionID) == -1) {
          champFactions.push(regionID)
        }
      }
    }
    return champFactions
  }

  var factionIDs = getChampFactions()

  if (factionIDs.length == 2) {
    // Got the 2 regions needed from champ
    return factionIDs.sort((a, b) => a - b)
  }

  const getFollowerFactionsBard = () => {
    for (var j in cards) {
      // Second loop to get followerFactions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !card.description.includes("card.chime") &&
        card.collectible
      ) {
        // Filters champion & card that plants chime
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsJhin = () => {
    for (var j in cards) {
      // Second loop to get follower Factions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !card.description.includes("keyword.AttackSkillMark") &&
        !card.description.includes("keyword.PlaySkillMark") &&
        !card.description.includes("card.skill") &&
        card.collectible
      ) {
        // Filters champion & card that play a skill
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsEvelynn = () => {
    for (var j in cards) {
      // Second loop to get follower Factions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !card.description.toLowerCase().includes("summon a random husk") &&
        card.collectible
      ) {
        // Filters champion & card that summons a random husk
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsJax = () => {
    for (var j in cards) {
      // Second loop to get followerFactions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !card.subtypes.includes("WEAPONMASTER") &&
        card.collectible
      ) {
        // Filters champion & card that plants chime
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsKayn = () => {
    for (var j in cards) {
      // Second loop to get followerFactions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !card.subtypes.includes("CULTIST") && // Filter out all cultist cards
        card.collectible
      ) {
        // Filters champion & card that is cultist
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsAatrox = () => {
    for (var j in cards) {
      // Second loop to get followerFactions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !card.subtypes.includes("DARKIN") && // Filter out all cultist cards
        card.collectible
      ) {
        // Filters champion & card that is darkin
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsRyze = () => {
    for (var j in cards) {
      // Second loop to get followerFactions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        card.spellSpeedRef != "Burst" && // Filter out all burst and focus speed cards
        card.collectible
      ) {
        // Filters champion & all burst and focus speed cards
        // Only considers mono region cards

        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsPoroKing = () => {
    for (var j in cards) {
      // Second loop to get followerFactions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !(card.subtypes.includes("PORO") || card.name.includes("Poro") || card.descriptionRaw.includes("Poro ")) && // Filter out all cards with Poro on the card
        card.collectible
      ) {
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  const getFollowerFactionsNeeko = () => {
    for (var j in cards) {
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        !(card.subtypes.includes("BIRD") || card.subtypes.includes("CAT") || card.subtypes.includes("DOG") || card.subtypes.includes("ELNUK") || card.subtypes.includes("FAE") || card.subtypes.includes("REPTILE") || card.subtypes.includes("SPIDER")) && // Filter out all cards with animals as subtypes
        card.collectible
      ) {
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  if (factionIDs.includes(regionRefID.Bard)) {
    getFollowerFactionsBard()
  } else if (factionIDs.includes(regionRefID.Jhin)) {
    getFollowerFactionsJhin()
  } else if (factionIDs.includes(regionRefID.Evelynn)) {
    getFollowerFactionsEvelynn()
  } else if (factionIDs.includes(regionRefID.Jax)) {
    getFollowerFactionsJax()
  } else if (factionIDs.includes(regionRefID.Kayn)) {
    getFollowerFactionsKayn()
  } else if (factionIDs.includes(regionRefID.Varus)) {
    getFollowerFactionsKayn()
  } else if (factionIDs.includes(regionRefID.Aatrox)) {
    getFollowerFactionsAatrox()
  } else if (factionIDs.includes(regionRefID.Ryze)) {
    getFollowerFactionsRyze()
  } else if (factionIDs.includes(regionRefID.PoroKing)) {
    getFollowerFactionsPoroKing()
  } else if (factionIDs.includes(regionRefID.Neeko)) {
    getFollowerFactionsNeeko()
  }
  else {
    for (var j in cards) {
      // Second loop to get follower Factions
      var card = baseStore.sets_en[cards[j].code]
      if (
        card &&
        card.rarityRef != "Champion" &&
        card.regions &&
        card.regions.length == 1 &&
        card.collectible
      ) {
        // Filters champion
        // Only considers mono region cards
        var regionID = regionRefID[card.regionRefs[0]]
        if (factionIDs.indexOf(regionID) == -1) {
          factionIDs.push(regionID)
        }
      }
    }
  }

  return factionIDs.sort((a, b) => a - b)
}

export default getFactions
