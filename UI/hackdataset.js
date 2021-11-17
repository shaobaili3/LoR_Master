// https://dd.b.pvp.net/2_3_0/set4-en_us.zip

var http = require("http");
const https = require('https')

let v1 = 2;
let v2 = 0;
let v3 = 0;

let setV = 4;

function reqestSet(v1, v2, v3, setV) {
  var options = {
    hostname: 'dd.b.pvp.net',
    port: 443,
    path: `/${v1}_${v2}_${v3}/set${setV}-lite-en_us.zip`,
    method: 'GET'
  };
  
  var req = https.request(options, function(res) {
    // console.log('STATUS: ' + res.statusCode);
    if (res.statusCode == "200") {
      console.log("SUCCESS!", 'https://' + req.host + req.path)
    } else {
      // console.log("Fail", req.path)
    }
    // console.log('HEADERS: ' + JSON.stringify(res.headers));
    // res.setEncoding('utf8');
    res.on('data', function (chunk) {
      // console.log('BODY: ' + chunk);
      req.destroy()
    });
  });
  
  req.on('error', function(e) {
    console.log('problem with request: ' + e.message);
  });
  
  // write data to request body
  req.write('data\n');
  req.end();
}

for (let k = 0; k < 3; k++) {
  for (let j = 0; j < 20; j++) {
    for (var i = 0; i < 20; i++) {
      reqestSet(v1 + k, v2 + j, v3 + i, setV)
    }
  }
}