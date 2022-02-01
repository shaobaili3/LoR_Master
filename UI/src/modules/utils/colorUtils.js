export const winrateGradient = [
  ["dc2626", 0.0],
  ["f59e0b", 0.4],
  ["f59e0b", 0.42],
  ["fbbf24", 0.44],
  ["facc15", 0.46],
  ["fde047", 0.48],
  ["fef08a", 0.5],
  ["ecfccb", 0.52],
  ["d9f99d", 0.54],
  ["bef264", 0.56],
  ["a3e635", 0.58],
  ["84cc16", 0.6],
  ["34d399", 0.7],
  ["2dd4bf", 0.8],
  ["38bdf8", 1.1],
]

const mix = function (color_1, color_2, weight) {
  function d2h(d) {
    return d.toString(16)
  } // convert a decimal value to hex
  function h2d(h) {
    return parseInt(h, 16)
  } // convert a hex value to decimal

  weight = typeof weight !== "undefined" ? weight : 50 // set the weight to 50%, if that argument is omitted

  var color = "#"

  for (var i = 0; i <= 5; i += 2) {
    // loop through each of the 3 hex pairs—red, green, and blue
    var v1 = h2d(color_1.substr(i, 2)), // extract the current pairs
      v2 = h2d(color_2.substr(i, 2)),
      // combine the current pairs from each source color, according to the specified weight
      val = d2h(Math.floor(v2 + (v1 - v2) * (weight / 100.0)))

    while (val.length < 2) {
      val = "0" + val
    } // prepend a '0' if val results in a single digit

    color += val // concatenate val to our new color string
  }

  return color // PROFIT!
}

export const winRateToColor = (ratio) => {
  for (let index in winrateGradient) {
    var gradient = winrateGradient[index]
    if (ratio < gradient[1]) {
      var last = winrateGradient[index - 1]
      var percent = ((ratio - last[1]) / (gradient[1] - last[1])) * 100
      return mix(gradient[0], last[0], percent)
    }
  }
  return winrateGradient[0][0]
}