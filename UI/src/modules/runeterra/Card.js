const Faction = require('./Faction')

module.exports = class Card {
  constructor (cardCode, count) {
    this.code = cardCode
    this.count = count
  }

  static from (setString, factionString, numberString, count) {
    return new this(setString + factionString + numberString, count)
  }

  static fromCardString (cardString) {
    const [count, cardCode] = cardString.split(':')
    return new this(cardCode, parseInt(count))
  }

  get set () {
    return parseInt(this.code.substring(0, 2))
  }

  get faction () {
    return Faction.fromCode(this.code.substring(2, 4))
  }

  get id () {
    return parseInt(this.code.substring(4, 7))
  }
}
