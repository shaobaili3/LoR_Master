class Faction {
  constructor(code, id) {
    this.shortCode = code;
    this.id = id;
  }

  static fromCode(code) {
    const factionIdVersion = Faction.FACTIONS[code];

    if (factionIdVersion === undefined) {
      throw new TypeError(
        "Invalid faction code. It is possible you need to upgrade the runeterra package."
      );
    }

    return new this(code, factionIdVersion[0]);
  }

  static fromID(id) {
    const [shortCode, factionId] =
      Object.entries(Faction.FACTIONS).find(
        ([, [factionId]]) => factionId === id
      ) || [];

    if (factionId === undefined) {
      throw new TypeError(
        "Invalid faction id. It is possible you need to upgrade the runeterra package."
      );
    }

    return new this(shortCode, factionId);
  }

  static getVersion(code) {
    const factionIdVersion = Faction.FACTIONS[code];

    if (factionIdVersion === undefined) {
      throw new TypeError(
        "Invalid faction code. It is possible you need to upgrade the runeterra package."
      );
    }

    return factionIdVersion[1];
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
};

module.exports = Faction;
