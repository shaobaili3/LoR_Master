const zmq = require("zeromq")

const deckObj = {"name":"Storm","rank":1,"matches":[{"winrate":"55%","badge":["recent"],"matches":1,"time":"3 min ago","deck":"CIBQEAIABENAEAYAAUFASAYJBERTSVCVKZLWAZAAAEAQCAAH"},{"winrate":"52%","badge":["frequent"],"matches":7,"time":"20 min ago","deck":"CIBQEAIABENAEAYAAUFASAYJBERTSVCVKZLWAZAAAEAQCAAH"},{"winrate":"25%","badge":[],"matches":2,"time":"5 hours ago","deck":"CICACAQAAEBACAA2FUBQGAAFBIFQGAYJENKVMAQBAEAASBIDBEBCMSC4MQAQCAIACU"}]}
const deckString = JSON.stringify(deckObj)

async function runPub() {
  console.log(zmq)
  const sock = new zmq.Publisher

  await sock.bind("tcp://127.0.0.1:9622")
  console.log("Publisher bound to port 9622")

  while (true) {
    console.log("Publishing new deck information")
    await sock.send(["LoR", deckString])
    await new Promise(resolve => setTimeout(resolve, 2000))
  }
}

async function runReply() {
  const sock = new zmq.Reply

  // Simulate a late connection from server
  // await new Promise(resolve => setTimeout(resolve, 5000))
  await sock.bind("tcp://127.0.0.1:9621")
  console.log("Reply bound to port 9621")

  for await (const [msg] of sock) {
    console.log("Replying deck info")
    await sock.send(deckString)
  }
}

async function runAll() {
  runPub()
  runReply()
}

module.exports = {
  run: runAll()
}
