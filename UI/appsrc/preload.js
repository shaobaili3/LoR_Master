const remote = require("electron").remote

const shell = require('electron').shell

var win = remote.getCurrentWindow()

window.closeWindow = function() {
    // console.log("Close window")
    win.hide()
    // win.close()
}

window.setSkipTaskbar = function(bool) {
    win.setSkipTaskbar(bool)
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

    // Minimize to Taskbar
    win.minimize()

	// remote.app.relaunch()
	// remote.app.exit(0)
}

var clientHeight = 0
const headerHeight = 45 // Repeated in app.js
const defaultRatio = 2.3 // Repeated in app.js
const minHeight = 170 
const defaultHeight = screen.height * 0.6

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


// --- Auto Update Logics ---

const { ipcRenderer } = require('electron')

// window.appVersion = null
// window.appVersionLatest = null

window.ipcRenderer = ipcRenderer

// ipcRenderer.on('app-version', (event, arg) => {
//     console.log(arg)
//     window.appVersion = arg
// })

// ipcRenderer.on('update-available', (event, info) => {
//     // console.log(info)
//     window.appVersionLatest = info.version
//     console.log("Latest Version is:", info.version)
// })

// ipcRenderer.on('update-not-available', (event, arg) => {
//     console.log(arg)
//     window.appVersionLatest = window.appVersion
// })

// ipcRenderer.on('download-process', (event, arg) => {
//     console.log(arg)
// })

// ipcRenderer.on('update-downloaded', (event, arg) => {
//     console.log(arg)
// })

// window.getAppVersion = function() {
//     ipcRenderer.send('get-app-version', 'ping')
// }

// ipcRenderer.on('get-app-version-reply', (event, arg) => {
//     console.log(arg)
// })


// ipcRenderer.send('asynchronous-message', 'ping')

// alert("Preload JS")