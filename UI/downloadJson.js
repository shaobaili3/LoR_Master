"use strict"

const fs = require("fs")
const http = require("http")

const setNum = 5

try {
  for (let i = 1; i <= setNum; i++) {
    const API_LINK = `http://dd.b.pvp.net/latest/set${i}/en_us/data/set${i}-en_us.json`
    const path = `./src/data/set${i}-en_us.json`

    console.log(`Download Started for set${i}`)
    const request = http.get(API_LINK, function (response) {
      if (response.statusCode === 200) {
        console.log(`Downloaded set${i}`)
        var file = fs.createWriteStream(path)
        response.pipe(file)
      }
      request.setTimeout(60000, function () {
        // if after 60s file not downlaoded, we abort a request
        request.destroy()
      })
    })
  }
} catch (error) {
  console.log(error)
}
