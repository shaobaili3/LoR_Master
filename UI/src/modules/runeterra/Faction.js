class Faction {
  constructor (code, id) {
    this.shortCode = code
    this.id = id
  }

  static fromCode (code) {
    const [factionId] = Faction.FACTIONS[code] || []

    if (factionId === undefined) {
      throw new TypeError('Invalid faction code. It is possible you need to upgrade the runeterra package.')
    }

    return new this(code, factionId)
  }

  static fromID (id) {
    const [shortCode, [factionId]] = Object.entries(Faction.FACTIONS).find(([, [factionId]]) => factionId === id) || [undefined, []]

    if (factionId === undefined) {
      throw new TypeError('Invalid faction id. It is possible you need to upgrade the runeterra package.')
    }

    return new this(shortCode, factionId)
  }

  static getVersion (code) {
    const [, version] = Faction.FACTIONS[code] || []

    if (version === undefined) {
      throw new TypeError('Invalid faction code. It is possible you need to upgrade the runeterra package.')
    }

    return version
  }
}

Faction.FACTIONS = {
  DE: [0, 1],
  FR: [1, 1],
  IO: [2, 1],
  NX: [3, 1],
  PZ: [4, 1],
  SI: [5, 1],
  BW: [6, 2],
  MT: [9, 2],
  SH: [7, 3],
  BC: [10, 4],
  RU: [12, 5]
}

module.exports = Faction
