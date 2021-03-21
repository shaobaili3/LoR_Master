class Base32 {
  static numberOfTrailingZeros (i) {
    if (i === 0) return 32
    let n = 31
    let y = i << 16
    if (y !== 0) {
      n = n - 16
      i = y
    }
    y = i << 8
    if (y !== 0) {
      n = n - 8
      i = y
    }
    y = i << 4
    if (y !== 0) {
      n = n - 4
      i = y
    }
    y = i << 2
    if (y !== 0) {
      n = n - 2
      i = y
    }
    return n - ((i << 1) >> 31)
  }

  static decode (encoded) {
    encoded = encoded.trim().replace(Base32.SEPARATOR, '')
    encoded = encoded.replace(/[=]*$/, '')
    encoded = encoded.toUpperCase()

    if (encoded.length === 0) return [0]
    const encodedLength = encoded.length
    const outLength = Math.floor(encodedLength * Base32.SHIFT / 8)
    const result = new Array(outLength)
    let buffer = 0
    let next = 0
    let bitsLeft = 0
    for (const c of encoded.split('')) {
      if (typeof Base32.CHAR_MAP[c] === 'undefined') {
        throw new TypeError('Illegal character: ' + c)
      }

      buffer <<= Base32.SHIFT
      buffer |= Base32.CHAR_MAP[c] & Base32.MASK
      bitsLeft += Base32.SHIFT
      if (bitsLeft >= 8) {
        result[next++] = (buffer >> (bitsLeft - 8)) & 0xff
        bitsLeft -= 8
      }
    }

    return result
  }

  static encode (data, padOutput = false) {
    if (data.length === 0) return ''
    if (data.length >= (1 << 28)) throw new RangeError('Array is too long for this')

    const outputLength = Math.floor((data.length * 8 + Base32.SHIFT - 1) / Base32.SHIFT)
    const result = new Array(outputLength)

    let buffer = data[0]
    let next = 1
    let bitsLeft = 8
    while (bitsLeft > 0 || next < data.length) {
      if (bitsLeft < Base32.SHIFT) {
        if (next < data.length) {
          buffer <<= 8
          buffer |= (data[next++] & 0xff)
          bitsLeft += 8
        } else {
          const pad = Base32.SHIFT - bitsLeft
          buffer <<= pad
          bitsLeft += pad
        }
      }
      const index = Base32.MASK & (buffer >> (bitsLeft - Base32.SHIFT))
      bitsLeft -= Base32.SHIFT
      result.push(Base32.DIGITS[index])
    }
    if (padOutput) {
      const padding = 8 - (result.length % 8)
      if (padding > 0) result.push('='.repeat(padding === 8 ? 0 : padding))
    }
    return result.join('')
  }
}

Base32.DIGITS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'.split('')
Base32.MASK = Base32.DIGITS.length - 1
Base32.SHIFT = Base32.numberOfTrailingZeros(Base32.DIGITS.length)
Base32.CHAR_MAP = Base32.DIGITS.reduce((m, d, i) => {
  m[d.toString()] = i
  return m
}, {})
Base32.SEPARATOR = '-'

module.exports = Base32
