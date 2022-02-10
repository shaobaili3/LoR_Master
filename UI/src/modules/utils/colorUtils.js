// export const winrateGradientV3 = [
//   ["e11d48", 0.0],
//   ["f94242", 0.29],
//   ["f95137", 0.32],
//   ["f66c3b", 0.35],
//   ["fc8a2b", 0.37],
//   ["f7a61b", 0.4],
//   ["fbbf24", 0.42],
//   ["facc15", 0.44],
//   ["fde047", 0.465],
//   ["fef08a", 0.49],
//   ["ebfba2", 0.51],
//   ["d9f99d", 0.535],
//   ["bef264", 0.56],
//   ["a3e635", 0.58],
//   ["92da24", 0.6],
//   ["84cc16", 0.62],
//   ["50c532", 0.65],
//   ["2fc841", 0.69],
//   ["0f98f1", 0.73],
//   ["0ea5e9", 0.77],
//   ["38bdf8", 0.85],
//   ["22d3ee", 0.9],
//   ["67e8f9", 0.95],
//   ["89f1ff", 1.01],
// ]

export const winrateGradientV2 = [
  ["f33535", 0.0],
  ["f94242", 0.29],
  ["f95137", 0.32],
  ["f66c3b", 0.35],
  ["fc8a2b", 0.37],
  ["f7a61b", 0.4],
  ["fbbf24", 0.42],
  ["facc15", 0.44],
  ["fde047", 0.465],
  ["fef08a", 0.49],
  ["ebfba2", 0.51],
  ["d9f99d", 0.535],
  ["bef264", 0.56],
  ["a3e635", 0.58],
  ["92da24", 0.6],
  ["84cc16", 0.62],
  ["50c532", 0.65],
  ["2fc841", 0.69],
  ["0ede99", 0.74],
  ["2eddf7", 0.79],
  ["38bdf8", 0.84],
  // ["3b82f6", 0.91],
  // ["1d4ed8", 0.99],
  // ["d8b4fe", 1.01],
]

export const winrateGradientSimple = [
  ["f33535", 0.0],
  ["fc8a2b", 0.15],
  ["f7a61b", 0.3],
  ["fbbf24", 0.4],
  ["bef264", 0.51],
  ["a3e635", 0.6],
  ["92da24", 0.7],
  ["84cc16", 0.8],
  ["50c532", 0.9],
  ["38bdf8", 0.95],
]

// export const winrateGradient = [
//   ["ef4444", 0.0],
//   ["f59e0b", 0.4],
//   ["f59e0b", 0.42],
//   ["fbbf24", 0.44],
//   ["facc15", 0.46],
//   ["fde047", 0.48],
//   ["fef08a", 0.5],
//   ["ecfccb", 0.52],
//   ["d9f99d", 0.54],
//   ["bef264", 0.56],
//   ["a3e635", 0.58],
//   ["84cc16", 0.6],
//   ["22c55e", 0.62],
//   ["2dd4bf", 0.8],
//   ["38bdf8", 0.9],
// ]

// export const winRateMonoYellow = [
//   ["fefce8", 0.0],
//   ["fffbeb", 0.1],
//   ["fef9c3", 0.2],
//   ["fef3c7", 0.3],
//   ["fef08a", 0.4],
//   ["fde68a", 0.5],
//   ["fde047", 0.6],
//   ["fcd34d", 0.7],
//   ["facc15", 0.8],
//   ["fbbf24", 0.9],
//   ["f59e0b", 1.0],
// ]

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
  var colorArray = winrateGradientV2
  if (ratio < 0) return "#" + colorArray[0][0]
  if (ratio >= colorArray.at(-1)[1]) return "#" + colorArray.at(-1)[0]

  for (let index in colorArray) {
    var gradient = colorArray[index]
    if (gradient[1] > ratio) {
      var last = colorArray[index - 1]
      var percent = ((ratio - last[1]) / (gradient[1] - last[1])) * 100
      return mix(gradient[0], last[0], percent)
    }
  }
  return "#" + colorArray[0][0]
}

export const winRateToSimpleColor = (ratio) => {
  var colorArray = winrateGradientSimple
  if (ratio <= 0) return "#" + colorArray[0][0]
  if (ratio >= colorArray.at(-1)[1]) return "#" + colorArray.at(-1)[0]

  for (let index in colorArray) {
    var gradient = colorArray[index]
    if (gradient[1] > ratio) {
      return "#" + colorArray[index - 1][0]
    }
  }
  return "#fff"
}
