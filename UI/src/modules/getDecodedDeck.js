import DeckEncoder from "./runeterra/DeckEncoder"
export const getDecodedDeck = (code) => {
  if (code) {
    try {
      var deck = DeckEncoder.decode(code)
      return deck
    } catch (error) {
      console.log(error)
      if (error.message) console.log(error.message)
      return null
    }
  }

  return null
}
