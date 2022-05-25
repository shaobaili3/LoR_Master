class VarInt {
  static pop (bytes) {
    let result = 0
    let currentShift = 0
    let bytesPopped = 0
    for (let i = 0; i < bytes.length; i++) {
      bytesPopped++
      const current = bytes[i] & VarInt.AllButMSB
      result |= current << currentShift

      if ((bytes[i] & VarInt.JustMSB) !== VarInt.JustMSB) {
        bytes.splice(0, bytesPopped)
        return result
      }

      currentShift += 7
    }

    throw new TypeError('Byte array did not contain valid varints.')
  }

  static get (value) {
    const buff = new Array(10)
    buff.fill(0)

    let currentIndex = 0
    if (value === 0) return [0]

    while (value !== 0) {
      let byteVal = value & VarInt.AllButMSB
      value >>>= 7

      if (value !== 0) byteVal |= VarInt.JustMSB
      buff[currentIndex++] = byteVal
    }

    return buff.slice(0, currentIndex)
  }
}

VarInt.AllButMSB = 0x7f
VarInt.JustMSB = 0x80

module.exports = VarInt
