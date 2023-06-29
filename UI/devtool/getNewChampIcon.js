const sets_en = require("../src/data/en_us.json")
const fs = require("fs")
const http = require("https")

const setCodes = ["1", "2", "3", "4", "5", "6", "6cde", "7", "7b"];

var champs = []

sets_en.forEach((set) => {
  set.forEach((card) => {
    if (card.rarityRef == "Champion" && card.collectible) {
      champs.push(card)
    }
  })
})

champs.forEach((champ) => {
  try {
    var code = champ.cardCode
    var name = champ.name
    var setCode = champ.set.slice(3)
    var set = setCodes.findIndex((val) => val == setCode)

    var location = "./src/assets/images/cards/cropped/" + code + "-cropped.png"
    if (!fs.existsSync(location)) {
      console.log("Missing " + name + " " + code)

      champ.associatedCardRefs.forEach((ref) => {
        var champLevel = sets_en[set].find((card) => {
          // Find all none champ spell alternative images
          return card.cardCode == ref && card.type == "Unit" && card.supertype == "Champion"
        })
        if (champLevel) downloadImage(name, ref, set)
      })

      downloadImage(name, code, set)
    }
  } catch (error) {
    console.log(error)
  }
})

function downloadImage(name, code, set) {
  // Download image and save to ./missingImage with name {code}.png
  let setCode = setCodes[set]
  const API_LINK = `https://dd.b.pvp.net/latest/set${setCode}/en_us/img/cards/${code}-full.png`
  const path = `./devtool/missingImage/${code}.png`

  console.log(`Download Started for image of ${name}, ${API_LINK}`)
  const request = http.get(API_LINK, function (response) {
    if (response.statusCode === 200) {
      console.log(`Downloaded image of ${name} | ${code}`)
      var file = fs.createWriteStream(path)
      response.pipe(file)
    } else {
      console.log(response.statusCode)
    }
    request.setTimeout(60000, function () {
      // if after 60s file not downlaoded, we abort a request
      request.destroy()
    })
  })
}

console.log("Checked All Champ Icons")
console.log("Crop (200x200): https://watermarkly.com/crop-photo/")
