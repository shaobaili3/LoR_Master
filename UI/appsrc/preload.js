const remote = require("electron").remote
const zmq = require("zeromq")

const shell = require('electron').shell

// Sub
const sock = new zmq.Subscriber

sock.connect("tcp://127.0.0.1:9622")
sock.subscribe("LoR")
console.log("Subscriber connected to port 9622")

window.sock = sock

// Request
const request = new zmq.Request

request.connect("tcp://127.0.0.1:9621")
console.log("Request connected to port 9621")
window.request = request

var win = remote.getCurrentWindow()

// async function runClient() {
//     const sock = new zmq.Subscriber
//     // const window = remote.getCurrentWindow()

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
    // console.log("Close window")
    win.close()
}

window.toggleWindow = function() {
    
    if (win.isMinimized()) {
        window.showWindow()
    } else {
        window.toggleShrinkWindow()
    }
}

window.showWindow = function() {
    
    if (win.isMinimized()) {
        win.restore()
    }
    if (window.isMin()) {
        window.expandWindow()
    }
        // win.show()
    // console.log("Show Window")
}

window.makeVisible = function() {
    if (!win.isVisible()) {
        win.show()
    }
}

window.minWindow = function() {
    // console.log('Closing')
    
    
    // Close Logic
    // win.close()

    // Minimize to Tray
    win.minimize()

	// remote.app.relaunch()
	// remote.app.exit(0)
}

var clientHeight = 0
const headerHeight = 45 // Repeated in app.js
const defaultRatio = 2.3 // Repeated in app.js
const minHeight = 170 
const defaultHeight = 620

window.expandWindow = function() {

    let w = win.getSize()[0]
    let h = win.getSize()[1]

    if (clientHeight <= headerHeight) {
        // in case recorded height is too small, reset it to default
        clientHeight = defaultHeight
    }   
    h = clientHeight

    win.setSize(w, h, false)
}

window.shrinkWindow = function() {

    let w = win.getSize()[0]
    let h = win.getSize()[1]

    if (h > minHeight) {
        // record height and minimize
        clientHeight = h
        h = headerHeight
    } else {
        if (h > headerHeight) {
            // shrink to min when too small but no record
            h = headerHeight
        }
    }

    win.setSize(w, h, false)
}

window.toggleShrinkWindow = function() {
    
    let w = win.getSize()[0]
    let h = win.getSize()[1]
    // window.minimize()
    // window.setSize(window.getSize[0], 45, true)

    if (h > minHeight) {
        // record height and minimize
        clientHeight = h
        h = headerHeight
    } else {
        if (h > headerHeight) {
            // shrink to min when too small but no record
            h = headerHeight
        } else {
            // expand to recorded height
            if (clientHeight <= headerHeight) {
                clientHeight = defaultHeight
                }
            h = clientHeight
        }
    }

    win.setSize(w, h, false)
    // console.log(win.getSize())
}

window.openExternal = function(url) {
    shell.openExternal(url)
}

window.isMin = function() {
    
    // window.minimize()

    // window.setSize(window.getSize[0], 45, true)
    // let w = win.getSize()[0]
    let h = win.getSize()[1]

    if (h > headerHeight) {
        return false
    } else {
        return true
    }
}