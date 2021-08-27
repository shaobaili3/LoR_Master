const Base32 = require('./Base32')
const VarInt = require('./VarInt')
const Card = require('./Card')
const Faction = require('./Faction')

class DeckEncoder {
  static decode (code) {
    const result = []

    let bytes = null
    try {
      bytes = Base32.decode(code)
    } catch (e) {
      throw new TypeError('Invalid deck code')
    }

    const firstByte = bytes.shift()
    const format = firstByte >> 4
    const version = firstByte & 0xF

    if (format !== DeckEncoder.FORMAT) {
      throw new TypeError('The provided code does not match the required format.')
    }
    if (version > DeckEncoder.MAX_KNOWN_VERSION) {
      throw new TypeError('The provided code requires a higher version of this library; please update.')
    }

    for (let i = 3; i > 0; i--) {
      const numGroupOfs = VarInt.pop(bytes)

      for (let j = 0; j < numGroupOfs; j++) {
        const numOfsInThisGroup = VarInt.pop(bytes)
        const set = VarInt.pop(bytes)
        const faction = VarInt.pop(bytes)

        for (let k = 0; k < numOfsInThisGroup; k++) {
          const card = VarInt.pop(bytes)

          const setString = set.toString().padStart(2, '0')
          const factionString = Faction.fromID(faction).shortCode
          const cardString = card.toString().padStart(3, '0')

          result.push(Card.from(setString, factionString, cardString, i))
        }
      }
    }

    while (bytes.length > 0) {
      const fourPlusCount = VarInt.pop(bytes)
      const fourPlusSet = VarInt.pop(bytes)
      const fourPlusFaction = VarInt.pop(bytes)
      const fourPlusNumber = VarInt.pop(bytes)

      const fourPlusSetString = fourPlusSet.toString().padStart(2, '0')
      const fourPlusFactionString = Faction.fromID(fourPlusFaction).shortCode
      const fourPlusNumberString = fourPlusNumber.toString().padStart(3, '0')

      result.push(Card.from(fourPlusSetString, fourPlusFactionString, fourPlusNumberString, fourPlusCount))
    }

    return result
  }

  static encode (cards) {
    if (!this.isValidDeck(cards)) {
      throw new TypeError('The deck provided contains invalid card codes')
    }

    const grouped3 = this.groupByFactionAndSetSorted(cards.filter(c => c.count === 3))
    const grouped2 = this.groupByFactionAndSetSorted(cards.filter(c => c.count === 2))
    const grouped1 = this.groupByFactionAndSetSorted(cards.filter(c => c.count === 1))
    const nOfs = cards.filter(c => c.count > 3)

    return Base32.encode([
      DeckEncoder.FORMAT << 4 | cards.reduce((p, c) => Math.max(p, c.version), 0) & 0xF,
      ...this.encodeGroup(grouped3),
      ...this.encodeGroup(grouped2),
      ...this.encodeGroup(grouped1),
      ...this.encodeNofs(nOfs)
    ])
  }

  static encodeNofs (nOfs) {
    return nOfs
      .sort((a, b) => a.code.localeCompare(b.code))
      .reduce((result, card) => {
        result.push(...VarInt.get(card.count))
        result.push(...VarInt.get(card.set))
        result.push(...VarInt.get(card.faction.id))
        result.push(...VarInt.get(card.id))
        return result
      }, [])
  }

  static encodeGroup (group) {
    return group.reduce((result, list) => {
      result.push(...VarInt.get(list.length))

      const first = list[0]
      result.push(...VarInt.get(first.set))
      result.push(...VarInt.get(first.faction.id))

      for (const card of list) {
        result.push(...VarInt.get(card.id))
      }

      return result
    }, VarInt.get(group.length))
  }

  static isValidDeck (cards) {
    return cards.every(card => (
      card.code.length === 7 &&
      !isNaN(card.id) &&
      !isNaN(card.count) &&
      card.faction &&
      card.count > 0
    ))
  }

  static groupByFactionAndSetSorted (cards) {
    const result = []

    while (cards.length > 0) {
      const set = []

      const first = cards.shift()
      set.push(first)

      for (let i = cards.length - 1; i >= 0; i--) {
        const compare = cards[i]
        if (first.set === compare.set && first.faction.id === compare.faction.id) {
          set.push(compare)
          cards.splice(i, 1)
        }
      }

      result.push(set)
    }

    return result.sort((a, b) => a.length - b.length).map(group => group.sort((a, b) => a.code.localeCompare(b.code)))
  }
}

DeckEncoder.MAX_KNOWN_VERSION = 4
DeckEncoder.FORMAT = 1
DeckEncoder.INITIAL_VERSION = 1

module.exports = DeckEncoder
