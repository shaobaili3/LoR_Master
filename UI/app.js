const Sentry = require("@sentry/electron")

Sentry.init({
  dsn: "https://18f2ad8a49d54543880b7e1852dd10b8@o958702.ingest.sentry.io/6126340",
})

const electron = require("electron")
const { app, Tray, Menu, MenuItem, globalShortcut, ipcMain } = require("electron")
const { autoUpdater } = require("electron-updater")
// const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require("path")
const remote = require("@electron/remote/main")
remote.initialize()

const isPackaged = app.isPackaged
const isDev = process.argv.includes("--dev")
const useFile = process.argv.includes("--file")

const developmentMode = (true && !isPackaged) || isDev

const closeWithoutTracker = false
const headerHeight = 45 // Repeated in preload.js
const defaultRatio = 2.3 // Repeated in preload.js

const defaultPort = "26531"

const spawnService = true || isPackaged
const spawnPython = true && !isPackaged

let currentVersion = ""
var startHidden = false

var isWin = process.platform === "win32"
var port = defaultPort

process.env.IS_ELECTRON = "electron"

// -----------------------------------------------
// --- app entry points ---
// -----------------------------------------------

const gotTheLock = app.requestSingleInstanceLock()

// Set up single instance
if (!gotTheLock) {
  console.log("Another Instance is alreaedy running")
  app.quit()
} else {
  app.on("second-instance", (event, commandLine, workingDirectory) => {
    // Someone tried to run a second instance, we should focus our window.
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore()
      if (!mainWindow.isVisible()) mainWindow.show()
      mainWindow.focus()
    }
  })
}

detectPortAndStartService()

app.on("ready", () => {
  // --- registers global shortcuts ---
  // globalShortcut.register('Alt+CommandOrControl+E', () => {
  // console.log('Electron loves global shortcuts!')
  // toggleDeckWindow()
  // })

  // globalShortcut.register('Alt+CommandOrControl+W', () => {
  // toggleMinDeckWindow()
  // })

  if (developmentMode) {
    globalShortcut.register("Alt+CommandOrControl+T", () => {
      requestTestHistory()
    })
    globalShortcut.register("CommandOrControl+R", function () {
      console.log("Reload Window")
      mainWindow.reload()
      deckWindow.reload()
    })
  }

  if (app.isPackaged) {
    currentVersion = app.getVersion()
  } else {
    currentVersion = require("./package.json").version
    autoUpdater.autoDownload = false
    autoUpdater.currentVersion = require("./package.json").version
  }

  appReady()
})

app.on("window-all-closed", () => {
  // console.log("All Window Closed")
  // if (process.platform !== 'darwin') {
  // app.quit()
  // }
})

// app.on("browser-window-blur", (event, window) => {
//   console.log("Window Blur", window)
// })

app.on("activate", () => {
  newMainWindow()
})

function showAlert(title, message) {
  const { dialog } = require("electron")
  dialog.showMessageBox({
    title: title,
    message: message,
  })
}

const appReady = () => {
  console.log("--------")
  console.log("App Ready")
  console.log("--------")
  console.log("Process Args:", process.argv)

  startHidden = process.argv.includes("--hidden")

  // --- deckWindow ---
  newDeckWindow()

  // --- mainWindow ---
  newMainWindow()

  // --- tray ---
  initTray()

  // const worker = new Worker(__dirname + '/electron/server.js')
  // server.run
  // runClient()

  console.log("Is Packaged?", app.isPackaged)
  console.log("Version: ", currentVersion)

  // newAlert()

  // if (app.isPackaged) {
  // Init Auto Launch on startup only on packaged app
  // enableAutoLaunch()
  // }
}

function requestTestHistory() {
  if (deckWindow) {
    deckWindow.webContents.send("request-test-history")
  }
}

// -----------------------------------------------
// --- Google Analytics (UA) ---
// -----------------------------------------------

const ua = require("universal-analytics")
var user
var userSet = false

ipcMain.on("user-init", (event, uid) => {
  console.log("Init User: ", uid)

  userSet = true

  // if (!isPackaged || isDev) return

  user = ua("UA-209481840-1", uid, { strictCidFormat: false })
  user.set("ds", "app")
  user.set("uid", uid)

  var eventCategory = "App"
  var eventAction = "Initialize"
  var eventLabel = "ID: " + uid + " | Version: " + currentVersion
  var eventValue = null

  recordUserEvent(eventCategory, eventAction, eventLabel, eventValue)
})

ipcMain.on("user-event", (event, eventInfo) => {
  var eventCategory = eventInfo.category
  var eventAction = eventInfo.action
  var eventLabel = eventInfo.label
  var eventValue = eventInfo.value

  recordUserEvent(eventCategory, eventAction, eventLabel, eventValue)
})

function recordUserEvent(eventCategory, eventAction, eventLabel, eventValue) {
  console.log(eventCategory, "|", eventAction, "|", eventLabel, "|", eventValue)
  // if (!isPackaged || isDev) return

  if (!userSet) {
    user = ua("UA-209481840-1")
    user.set("ds", "app")

    userSet = true
  }

  user.event(eventCategory, eventAction, eventLabel, eventValue, function (err) {
    if (err) console.log(err)
  })
}

// -----------------------------------------------
// --- Auto Updater ---
// -----------------------------------------------

autoUpdater.logger = require("electron-log")
autoUpdater.logger.transports.file.level = "info"

// autoUpdater.channel = "beta"

autoUpdater.on("checking-for-update", () => {
  console.log("Checking for Update...")
  if (mainWindow) mainWindow.webContents.send("checking-for-update")
})

autoUpdater.on("update-available", (info) => {
  console.log("Update available")
  console.log("Version", info.version)
  console.log("Release Data", info.releaseDate)
  if (mainWindow) mainWindow.webContents.send("update-available", info)
})

autoUpdater.on("update-not-available", () => {
  console.log("Update not available")
  if (mainWindow) mainWindow.webContents.send("update-not-available")
})

autoUpdater.on("download-progress", (progress) => {
  console.log(`Progress ${Math.floor(progress.percent)}`)
  if (mainWindow) mainWindow.webContents.send("download-process", progress)
})

autoUpdater.on("update-downloaded", (info) => {
  console.log("Update downloaded")
  // autoUpdater.quitAndInstall(true)
  if (mainWindow) mainWindow.webContents.send("update-downloaded", info)
})

autoUpdater.on("error", (err) => {
  console.log(err)
})

ipcMain.on("check-update", (event) => {
  mainWindow.webContents.send("app-version", currentVersion)
  checkForUpdates()
})

ipcMain.on("install-update", (event) => {
  autoUpdater.quitAndInstall(true, true)
})

ipcMain.on("game-start-trigger", () => {
  console.log("Handling Game Start")
  recordUserEvent("Tracker Event", "Game Start", new Date().toUTCString(), null)
})

ipcMain.on("game-end-trigger", () => {
  console.log("Handling Game End")

  recordUserEvent("Tracker Event", "Game End", new Date().toUTCString(), null)
  if (mainWindow) mainWindow.webContents.send("game-end-handle")
})

ipcMain.on("get-port", (event, args) => {
  event.sender.send("return-port", port)
  // if (mainWindow) mainWindow.webContents.send('return-port', port)
  // if (deckWindow) deckWindow.webContents.send('return-port', port)
})

setInterval(() => {
  checkForUpdates()
}, 1000 * 60 * 15) // 15 miniutes

function checkForUpdates() {
  if (isWin) {
    autoUpdater.checkForUpdates().catch((err) => {
      console.log(err) // Should no longer report uncaught error due to connection lose
    })
  }
}

// -----------------------------------------------
// --- Tray ---
// -----------------------------------------------

let tray = null
function initTray() {
  tray = new Tray(__dirname + "/image.ico")
  const contextMenu = Menu.buildFromTemplate([
    // { label: 'Item1', type: 'radio' },
    // { label: 'Item2', type: 'radio' },
    // { label: 'Item3', type: 'radio', checked: true },
    // { label: 'Item4', type: 'radio' },
    {
      label: "Open",
      click: () => {
        newMainWindow()
      },
    },
    {
      label: "About",
      click: () => {
        newInfoWindow()
      },
    },
    { type: "separator" },
    {
      label: "Quit",
      click: () => {
        app.quit()
      },
    },
  ])
  tray.setToolTip("LoR Master Tracker")
  tray.on("click", () => {
    // tray.popUpContextMenu()
    // console.log("Tray Clicked")
    newMainWindow()
  })

  tray.setContextMenu(contextMenu)

  console.log("Tray Created")
}

// -----------------------------------------------
// --- Menu and short cuts ---
// -----------------------------------------------

const menu = new Menu()
menu.append(
  new MenuItem({
    label: "Electron",
    submenu: [
      {
        role: "help",
        accelerator: process.platform === "darwin" ? "Alt+Cmd+I" : "Alt+Shift+I",
        click: () => {
          console.log("New Info Window")
          newInfoWindow()
        },
      },
    ],
  })
)

Menu.setApplicationMenu(menu)

const log = require("electron-log")

// -----------------------------------------------
// --- Backend Service ---
// -----------------------------------------------

var lmtServiceStarted = false
const lmstServiceRetryLimit = 3
var lmstServiceRetryCount = 0
function detectPortAndStartService() {
  if (lmtServiceStarted) return

  const detect = require("detect-port")
  detect(port, (err, _port) => {
    if (err) {
      console.log(err)
      return
    }

    if (port == _port) {
      console.log(`port: ${port} was not occupied`)
    } else {
      console.log(`port: ${port} was occupied, try port: ${_port}`)
    }

    if (spawnService) {
      // Only if spawning service will the port be changed
      port = _port

      if (mainWindow) mainWindow.webContents.send("return-port", port)
      if (deckWindow) deckWindow.webContents.send("return-port", port)

      startLMTService(port)
    }
  })
}

function startLMTService(port) {
  console.log("--------------------")
  console.log("Starting LMT Service", "Port equals to: ", port)
  console.log("--------------------")

  if (lmtServiceStarted) return

  try {
    lmtServiceStarted = true
    const { spawn } = require("child_process")

    var proc

    var devarg = developmentMode ? "dev" : "prod"

    var args = [`--port=${port}`, `--status=${devarg}`]

    if (spawnPython) {
      proc = spawn("python", ["./LMTService.py", ...args], { cwd: "../" })
    } else {
      var backend, execPath
      if (app.isPackaged) {
        execPath = path.dirname(app.getPath("exe"))
      } else {
        execPath = __dirname
      }
      backend = path.join(execPath, "backend", "LMTService", "LMTService.exe")
      proc = spawn(backend, args, {
        cwd: path.join(execPath, "backend", "LMTService"),
      })
    }

    proc.stdout.on("data", function (data) {
      if (isPackaged) {
        log.info(`stdout: ${data}`)
      } else {
        if (developmentMode) console.log("data: ", data.toString("utf8"))
      }
    })
    proc.stderr.on("data", (data) => {
      if (isPackaged) {
        log.warn(`stderr: ${data}`)
      } else {
        console.log(`stderr: ${data}`) // when error
      }
    })

    proc.on("close", (code) => {
      if (isPackaged) {
        log.warn(`Child process close all stdio with code ${code}`)
      } else {
        console.log(`Child process close all stdio with code ${code}`)
      }

      lmtServiceStarted = false

      if (lmstServiceRetryCount < lmstServiceRetryLimit) {
        lmstServiceRetryCount += 1
        console.log(`Retrying ${lmstServiceRetryCount} time`)
        startLMTService(port)
      }

      if (mainWindow) {
        mainWindow.webContents.send("backend-closed")
      }
    })
    proc.on("exit", (code) => {
      console.log(`Child process exited with code ${code}`)
    })
  } catch (err) {
    lmtServiceStarted = false
    if (isPackaged) {
      log.error(err)
    } else {
      console.log(err)
    }
  }
}

ipcMain.on("backend-restart", (event, enable) => {
  lmstServiceRetryCount = 0
  detectPortAndStartService()
})

// -----------------------------------------------
// --- BrowserWindows ---
// -----------------------------------------------

let deckWindow = null
let infoWindow = null
let mainWindow = null

let allWindows = []

function newMainWindow() {
  if (mainWindow) {
    mainWindow.show()
    return
  }

  let { width, height } = electron.screen.getPrimaryDisplay().workAreaSize

  // --- mainWindow ---
  let windowWidth = Math.min(width, 1440) // (335)
  let windowMaxWidth = 1920
  let windowMinWidth = 800
  let windowMinHeight = 730
  let windowHeight = Math.min(height, 900)

  mainWindow = new BrowserWindow({
    maxWidth: windowMaxWidth,
    minWidth: windowMinWidth,
    minHeight: windowMinHeight,
    width: windowWidth,
    height: windowHeight,
    x: (width - windowWidth) / 2,
    y: (height - windowHeight) / 2,
    frame: false,
    resizable: true,
    show: false,
    backgroundColor: "#1c1c1f",
    webPreferences: {
      // nodeIntegration: true,
      // enableRemoteModule: true,
      contextIsolation: false,
      preload: __dirname + "/src/preload.js",
    },
  })

  remote.enable(mainWindow.webContents)

  const mainWindowUrl = require("url").format({
    protocol: "file",
    slashes: true,
    pathname: require("path").join(__dirname, "dist", "index.html"),
  })

  if (developmentMode && !useFile) {
    mainWindow.loadURL("http://localhost:8080/index.html")
  } else {
    mainWindow.loadURL(mainWindowUrl)
  }

  // mainWindow.setAlwaysOnTop(true, level = "pop-up-menu")
  mainWindow.on("closed", () => {
    mainWindow = null
    // app.quit()
  })

  mainWindow.on("hide", () => {})

  mainWindow.on("focus", () => {
    // console.log("Main window Focus")
    processClipboard()
  })

  mainWindow.once("ready-to-show", () => {
    if (!startHidden) mainWindow.show()
    console.log("-- Main Window Ready -- ")
    mainWindow.webContents.send("app-version", currentVersion)
    mainWindow.webContents.send("debug-info-display", process.argv)
  })

  if (developmentMode) mainWindow.webContents.openDevTools({ mode: "undocked" })

  allWindows.push(mainWindow)
}

function newDeckWindow() {
  const { width, height } = electron.screen.getPrimaryDisplay().workAreaSize

  const defaultTrackerWidth = width > 1920 ? 230 : 200
  const defaultTrackerHeight = Math.floor(height * 0.7)
  const defaultTrackerX = 20
  const defaultTrackerY = Math.floor(height / 2 - defaultTrackerHeight / 2)
  const defaultTrackerMaxWidth = 290
  const defaultTrackerMinWidth = 170

  const devConsoleWidth = 400

  function resetDeckWindowBounds() {
    let defaultBounds = {
      x: defaultTrackerX,
      y: defaultTrackerY,
      width: defaultTrackerWidth,
      height: defaultTrackerHeight,
    }
    if (deckWindow) deckWindow.setBounds(defaultBounds)
    console.log("Reset UI Deck Bounds")
    store.set("ui-deck-bounds", defaultBounds)
  }

  ipcMain.on("reset-deck-window-bounds", resetDeckWindowBounds)

  if (deckWindow) {
    deckWindow.show()
    return
  }

  // --- deckWindow ---
  let windowMaxWidth = defaultTrackerMaxWidth
  let windowMinWidth = defaultTrackerMinWidth

  let bounds = store.get("ui-deck-bounds")
  let windowX, windowY, windowWidth, windowHeight

  if (bounds == null) {
    // Default
    windowX = defaultTrackerX
    windowY = defaultTrackerY
    windowWidth = defaultTrackerWidth
    windowHeight = defaultTrackerHeight
    resetDeckWindowBounds()
  } else {
    windowX = bounds.x ?? defaultTrackerX
    windowY = bounds.y ?? defaultTrackerY
    windowWidth = bounds.width ?? defaultTrackerWidth
    windowHeight = bounds.height ?? defaultTrackerHeight
  }

  deckWindow = new BrowserWindow({
    maxWidth: windowMaxWidth,
    minWidth: windowMinWidth,
    minHeight: headerHeight,
    x: windowX,
    y: windowY,
    width: windowWidth,
    height: windowHeight,
    frame: false,
    resizable: true,
    skipTaskbar: true,
    show: false,
    webPreferences: {
      contextIsolation: false,
      preload: __dirname + "/src/preload.js",
    },
  })

  remote.enable(deckWindow.webContents)

  if (developmentMode && !useFile) {
    deckWindow.loadURL("http://localhost:8080/deck.html")
  } else {
    deckWindow.loadURL(`file://${__dirname}/dist/deck.html`)
  }

  deckWindow.setAlwaysOnTop(true, "pop-up-menu")
  deckWindow.on("closed", () => {
    deckWindow = null
  })

  deckWindow.on("restore", () => {
    deckWindow.setSkipTaskbar(true)
  })

  deckWindow.on("minimize", () => {
    deckWindow.setSkipTaskbar(false)
  })

  const handleMoveResize = () => {
    let bounds = deckWindow.getBounds()
    console.log("Tracker Window Moved or Resized", bounds)
    store.set("ui-deck-bounds", {
      x: bounds.x,
      y: bounds.y,
      width: bounds.width,
      height: bounds.height,
    })
  }

  deckWindow.on("moved", handleMoveResize)
  deckWindow.on("resized", handleMoveResize)

  if (developmentMode) deckWindow.webContents.openDevTools({ mode: "undocked" })

  allWindows.push(deckWindow)
}

function newInfoWindow() {
  if (infoWindow) {
    infoWindow.show()
    return
  }

  let { width, height } = electron.screen.getPrimaryDisplay().workAreaSize
  // let factor = electron.screen.getPrimaryDisplay().scaleFactor

  // --- infoWindow ---
  let windowWidth = 270
  let windowHeight = 270

  if (developmentMode) {
    windowWidth = windowWidth + 400
  }

  infoWindow = new BrowserWindow({
    width: windowWidth,
    height: windowHeight,
    x: width / 2 - windowWidth / 2,
    y: height / 2 - windowHeight / 2,
    frame: false,
    resizable: false,
    webPreferences: {
      // nodeIntegration: true,
      // enableRemoteModule: true,
      contextIsolation: false,
      preload: __dirname + "/src/preload.js",
    },
    // titleBarStyle: 'hiddenInset'
  })

  remote.enable(infoWindow.webContents)

  infoWindow.loadURL(`file://${__dirname}/dist/info.html`)
  // console.log("Is development?", process.env.NODE_ENV === 'development')

  infoWindow.setAlwaysOnTop(true, "pop-up-menu")
  infoWindow.on("closed", () => {
    infoWindow = null
  })

  if (developmentMode) infoWindow.webContents.openDevTools()

  allWindows.push(infoWindow)
}

function showDeckWindow() {
  try {
    deckWindow.webContents.executeJavaScript("window.showWindow()")
  } catch (e) {
    console.log(e)
  }
}

function toggleMinDeckWindow() {
  if (deckWindow.isMinimized()) {
    deckWindow.restore()
  } else {
    deckWindow.minimize()
  }
}

function toggleDeckWindow() {
  try {
    deckWindow.webContents.executeJavaScript("window.toggleWindow()")
  } catch (e) {
    console.log(e)
  }
}

// -----------------------------------------------
// --- Alerts ---
// -----------------------------------------------

function newAlert() {}

// ipcMain.on('custom-alert', (event, args) => {
//   console.log("Alert", args)
//   // autoUpdater.quitAndInstall(true, true)
// })

// setInterval(() => {
//   newAlert("LoR Master Tracker Hidden", "Click on icon to show, Right click for more")
// }, 1000 * 5)

// -----------------------------------------------
// --- Auto Launch ---
// -----------------------------------------------

var AutoLaunch = require("auto-launch")
var autoLauncher = new AutoLaunch({
  name: "LoR Master Tracker",
  isHidden: true,
})

function checkAutoLaunch() {
  autoLauncher
    .isEnabled()
    .then(function (isEnabled) {
      console.log("Auto Launch Enabled: ", isEnabled)
      sendAutoLaunchToMain(isEnabled)
    })
    .catch(function (err) {
      console.log(err)
    })
}

function sendAutoLaunchToMain(isEnabled) {
  if (mainWindow) mainWindow.webContents.send("check-auto-launch-return", isEnabled)
}

ipcMain.on("check-auto-launch", (event, args) => {
  checkAutoLaunch()
})

ipcMain.on("set-auto-launch", (event, enable) => {
  if (enable) {
    enableAutoLaunch()
  } else {
    disableAutoLaunch()
  }
  checkAutoLaunch()
})

// var quitOnClose = false

// ipcMain.on('set-quit-on-close', (event, enable) => {

// })

function enableAutoLaunch() {
  autoLauncher.enable()
}

function disableAutoLaunch() {
  autoLauncher.disable()
}

// -----------------------------------------------
// --- Store ---
// -----------------------------------------------

const Store = require("electron-store")
const store = new Store()

console.log("Storing data at", app.getPath("userData"))

if (store.get("ui-locale") == null) {
  // First time language setting
  var systemLang = getEnvLocale()
  console.log("No Language Set | System Locale", systemLang)

  var newLocale = ""

  if (!systemLang) {
    newLocale = "English"
  } else if (systemLang.includes("zh_CN")) {
    // 简体中文
    newLocale = "简体中文"
  } else if (systemLang.includes("zh")) {
    // 繁体中文
    newLocale = "繁體中文"
  }

  if (newLocale != "") {
    store.set("ui-locale", newLocale)

    BrowserWindow.getAllWindows().forEach((bw) => {
      console.log("-- sending to", bw.id)
      bw.webContents.send("to-change-locale", newLocale)
    })
  }
} else {
  console.log("Language set to", store.get("ui-locale"), " | System Locale", getEnvLocale())
}

ipcMain.on("request-store", (event, key) => {
  event.sender.send(`reply-store-${key}`, store.get(key))
})

ipcMain.on("save-store", (event, key, val) => {
  console.log(`Saving to Store | Key: ${key}`)
  store.set(key, val)
})

// -----------------------------------------------
// --- Locale ---
// -----------------------------------------------

ipcMain.on("changed-locale", (event, newLocale) => {
  console.log("Changing Locale to", newLocale, ", from", event.sender.id)
  store.set("ui-locale", newLocale)

  BrowserWindow.getAllWindows().forEach((bw) => {
    if (bw && bw.webContents.id != event.sender.id) {
      console.log("-- sending to", bw.webContents.id)
      bw.webContents.send("to-change-locale", newLocale)
    } else {
      console.log("-- not sending to", bw.webContents.id)
    }
  })
})

ipcMain.on("changed-card-locale", (event, newLocale) => {
  console.log("Changing Card Locale to", newLocale, ", from", event.sender.id)
  store.set("card-locale", newLocale)

  BrowserWindow.getAllWindows().forEach((bw) => {
    if (bw && bw.webContents.id != event.sender.id) {
      console.log("-- sending to", bw.webContents.id)
      bw.webContents.send("to-change-card-locale", newLocale)
    } else {
      console.log("-- not sending to", bw.webContents.id)
    }
  })
})

function getEnvLocale(env) {
  env = env || process.env

  return env.LC_ALL || env.LC_MESSAGES || env.LANG || env.LANGUAGE
}

// -----------------------------------------------
// --- Clipboard ---
// -----------------------------------------------

function processClipboard() {
  const { clipboard } = require("electron")

  const code = clipboard.readText()

  // Maybe put this into Renderer?
  const encoder = require("./src/modules/runeterra/DeckEncoder")

  try {
    let deck = encoder.decode(code)
    console.log("Clip board has a deck")
    if (mainWindow) mainWindow.webContents.send("handle-clipboard-deck", code)

    clipboard.writeText("")
  } catch (error) {
    // console.log("Clip board doesn't have a deck")
  }
}

// --- Use these to check for old running python app ---

// const tasklist = require("tasklist")
// const { cp } = require("fs")
/*
	[
		{
			imageName: 'taskhostex.exe',
			pid: 1820,
			sessionName: 'Console',
			sessionNumber: 1,
			memUsage: 4415488
		},
		…
	]
	*/

// var isCheckingTracker = false
// async function checkTracker() {
//   isCheckingTracker = true

//   // Check Python Process with window name containing LoR Master Tracker
//   var pythonList = await tasklist({
//     filter: ["IMAGENAME eq python.exe"],
//     verbose: true,
//   })
//   pythonList = pythonList.filter((ps) => ps.windowTitle.indexOf("LoR Master Tracker") != -1)

//   // Check LoRMasterTracker.exe process
//   var trackerList = await tasklist({
//     filter: ["IMAGENAME eq LoRMasterTracker.exe"],
//     verbose: false,
//   })

// tasklist /fi "IMAGENAME eq LoR.exe"

//   // console.log(list.filter(ps => ps.imageName.indexOf('python') != -1))
//   // console.log("\n pythonList", pythonList.length)
//   // console.log("trackerList", trackerList.length)

//   if (pythonList.length + trackerList.length <= 0) {
//     // There is no tracker running
//     console.log("No tracker running")
//     // app.quit()
//     if (deckWindow) deckWindow.close()
//     // app.exit()
//   } else {
//     // if (!deckWindow) appReady()
//   }

//   setTimeout(checkTracker, 1000)
// }

// checkTracker()
