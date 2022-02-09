export const showDeckMixin = {
  emits: {
    showDeck: (deck) => {
      if (deck) {
        return true
      } else {
        return false
      }
    },
  },
  methods: {
    showDeck(deck) {
      this.$emit("showDeck", deck)
    },
  },
}
