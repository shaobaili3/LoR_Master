const sets_en = require('../../Resource/en_us.json')
const fs = require('fs')
const http = require('https')

var champs = []

sets_en.forEach(set => {
  set.forEach(card => {
    if (card.rarityRef == "Champion" && card.collectible) {
      champs.push(card)
    }
  })
});

champs.forEach(champ => {
  try {
    var code = champ.cardCode
    var name =  champ.name
    var set = champ.set[3]

    var location = './src/assets/images/cards/cropped/' + code + '-cropped.png'
    if (fs.existsSync(location)) {
    } else {
      console.log("Missing " + name + ' ' + code)

      champ.associatedCardRefs.forEach(ref => {
        var champLevel = sets_en[set - 1].find( card => {
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
  const API_LINK = `https://dd.b.pvp.net/latest/set${set}/en_us/img/cards/${code}-full.png`
  const path = `./devtool/missingImage/${code}.png`

  console.log(`Download Started for image of ${name}, ${API_LINK}`);
  const request = http.get(API_LINK, function(response) {
    if (response.statusCode === 200) {
      console.log(`Downloaded image of ${name} | ${code}`)
        var file = fs.createWriteStream(path);
        response.pipe(file);
    } else {
      console.log(response.statusCode)
    }
    request.setTimeout(60000, function() { // if after 60s file not downlaoded, we abort a request 
        request.destroy();
    });
  });
}

console.log("Checked All Champ Icons")