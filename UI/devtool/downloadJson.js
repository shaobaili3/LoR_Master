"use strict"

const fs = require("fs")
// const http = require("http")

const axios = require("axios").default

const setCodes = ["1", "2", "3", "4", "5", "6", "6cde", "7", "7b"];

const specialAdditions = [
  // {version: "3_14_0", set: "6cde"}
]

const setLocales = [
  "de_de",
  "en_us",
  "es_es",
  "es_mx",
  "fr_fr",
  "it_it",
  "ja_jp",
  "ko_kr",
  "pl_pl",
  "pt_br",
  "th_th",
  "tr_tr",
  "ru_ru",
  "zh_tw",
]

const stream = require("stream")
const promisify = require("util").promisify

const finished = promisify(stream.finished)

async function downloadFile(fileUrl, outputLocationPath) {
  return axios({
      method: "get",
      url: fileUrl,
      responseType: "stream",
    })
    .then((response) => {
      const writer = fs.createWriteStream(outputLocationPath)
      response.data.pipe(writer)
      return finished(writer) //this is a Promise
    })
    .catch((err) => {
      console.log("Error downloading", fileUrl)
    })
}

var promises = []
var files = []

for (let i = 0; i < setCodes.length; i++) {
  for (let j = 0; j < setLocales.length; j++) {
    let setCode = setCodes[i]
    const api = `http://dd.b.pvp.net/latest/set${setCode}/${setLocales[j]}/data/set${setCode}-${setLocales[j]}.json`
    const path = `./src/data/set${setCode}-${setLocales[j]}.json`

    if (files[j] == null) {
      files[j] = []
    }

    files[j].push(path)

    console.log(`Download Started for set${setCode}, locale: ${setLocales[j]}, api: ${api}`)
    promises.push(downloadFile(api, path))
  }

  // const request = http.get(API_LINK, function (response) {
  //   if (response.statusCode === 200) {
  //     console.log(`Downloaded set${i}`)
  //     var file = fs.createWriteStream(path)
  //     response.pipe(file)
  //   }
  //   request.setTimeout(60000, function () {
  //     // if after 60s file not downlaoded, we abort a request
  //     request.destroy()
  //   })
  // })
}

if (specialAdditions.length > 0)
  for (var item of specialAdditions) {
    for (let j = 0; j < setLocales.length; j++) {
      let version = item.version
      let setCode = item.set
      const api = `http://dd.b.pvp.net/${version}/set${setCode}/${setLocales[j]}/data/set${setCode}-${setLocales[j]}.json`
      const path = `./src/data/${version}-set${setCode}-${setLocales[j]}.json`

      files[j].push(path)
      console.log(`Download Started for version: ${version}, set${setCode}, locale: ${setLocales[j]}, api: ${api}`)
      promises.push(downloadFile(api, path))
    }
  }

function allProgress(proms, progress_cb) {
  let d = 0
  progress_cb(0)
  for (const p of proms) {
    p.then(() => {
      d++
      progress_cb((d * 100) / proms.length)
    })
  }
  return Promise.all(proms)
}

function concatFiles() {
  for (let i = 0; i < setLocales.length; i++) {
    var finalJson = []
    for (var file of files[i]) {
      finalJson.push(JSON.parse(fs.readFileSync(file)))
    }

    let data = JSON.stringify(finalJson, null, 2)
    fs.writeFileSync(`./src/data/${setLocales[i]}.json`, data)
  }
}

function generateSimplifiedChinese() {
  const chineseConv = require("chinese-conv")
  let data = chineseConv.sify(fs.readFileSync(`./src/data/zh_tw.json`, "utf8"))
  fs.writeFileSync(`./src/data/zh_cn.json`, data)
}

allProgress(promises, (p) => {
  console.log(`Progress: ${p.toFixed(2)}% Done`)
}).then(() => {
  console.log("All files are donwloaded.")
  concatFiles()
  console.log("Concated files generated.")
  generateSimplifiedChinese()
  console.log("Simplifeid Chinese generated.")
})

// concatFiles()