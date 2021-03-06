const remote = require("electron").remote;
const zmq = require("zeromq");

// Sub
const sock = new zmq.Subscriber
  
sock.connect("tcp://127.0.0.1:9621")
sock.subscribe("LoR")
// console.log("Subscriber connected to port 3000")

window.sock = sock;

// Request
const request = new zmq.Request

request.connect("tcp://127.0.0.1:9622")
window.request = request;

// async function runClient() {
//     const sock = new zmq.Subscriber
//     // const window = remote.getCurrentWindow();
  
//     sock.connect("tcp://127.0.0.1:3000")
//     sock.subscribe("kitty cats")
//     console.log("Subscriber connected to port 3000")
  
//     for await (const [topic, msg] of sock) {
//       console.log("received a message related to:", topic.toString(), "containing message:", msg.toString())
//       window.testData = msg.toString()
//       // console.log(mainWindow)
//     }
// }

// runClient()

window.closeWindow = function() {
    // console.log('Closing');
    var win = remote.getCurrentWindow();
    win.close();
	// remote.app.relaunch()
	// remote.app.exit(0);
};

window.minWindow = function() {
    var win = remote.getCurrentWindow();
    // window.minimize();

    // window.setSize(window.getSize[0], 45, true);
    let w = win.getSize()[0]
    let h = win.getSize()[1]

    if (h > 45) {
        h = 45
    } else {
        h = Math.floor(w*1.666)
    }

    win.setSize(w, h, false);
    // console.log(win.getSize());
}

// window.