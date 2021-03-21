class Faction {
  constructor (code, id) {
    this.shortCode = code
    this.id = id
  }

  static fromCode (code) {
    const factionId = Faction.FACTIONS[code]

    if (factionId === undefined) {
      throw new TypeError('Invalid faction code. It is possible you need to upgrade the runeterra package.')
    }

    return new this(code, factionId)
  }

  static fromID (id) {
    const [shortCode, factionId] = Object.entries(Faction.FACTIONS).find(([shortCode, factionId]) => factionId === id) || []

    if (factionId === undefined) {
      throw new TypeError('Invalid faction id. It is possible you need to upgrade the runeterra package.')
    }

    return new this(shortCode, factionId)
  }
}

Faction.FACTIONS = {
  DE: 0,
  FR: 1,
  IO: 2,
  NX: 3,
  PZ: 4,
  SI: 5,
  BW: 6,
  MT: 9,
  SH: 7
}

module.exports = Faction
