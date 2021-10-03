
const electron = require('electron')
const { app, Tray, Menu, MenuItem, globalShortcut , ipcMain} = require('electron')
const { autoUpdater } = require('electron-updater')
// const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')
const remote = require('@electron/remote/main')
remote.initialize()

const developmentMode = true && !(process.env.IS_PUBLISH)

const closeWithoutTracker = false
const headerHeight = 45 // Repeated in preload.js
const defaultRatio = 2.3 // Repeated in preload.js

const defaultPort = '26531'

const spawnService = true || process.env.IS_PUBLISH
const spawnPython = true && !(process.env.IS_PUBLISH)

let currentVersion = ""
var startHidden = false

var isWin = process.platform === "win32"
var port = defaultPort

// -----------------------------------------------
// --- app entry points ---
// -----------------------------------------------

const gotTheLock = app.requestSingleInstanceLock()

// Set up single instance
if (!gotTheLock) {
  console.log("Another Instance is alreaedy running")
  app.quit()
} else {
  app.on('second-instance', (event, commandLine, workingDirectory) => {
    // Someone tried to run a second instance, we should focus our window.
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore()
      if (!mainWindow.isVisible()) mainWindow.show()
      mainWindow.focus()
    }
  })
}

app.on('ready', () => {
  // --- registers global shortcuts ---
  globalShortcut.register('Alt+CommandOrControl+E', () => {
    // console.log('Electron loves global shortcuts!')
    toggleDeckWindow()
  })

  globalShortcut.register('Alt+CommandOrControl+W', () => {
    toggleMinDeckWindow()
  })
  
  if (developmentMode) {
    globalShortcut.register('Alt+CommandOrControl+T', () => {
      requestTestHistory()
    })
  }

  if (app.isPackaged) {
    currentVersion = app.getVersion()
  } else {
    currentVersion = require('./package.json').version
    autoUpdater.autoDownload = false
    autoUpdater.currentVersion = require('./package.json').version
  }

  appReady()
})

app.on('window-all-closed', () => {
  // console.log("All Window Closed")
  // if (process.platform !== 'darwin') {
  // app.quit()
  // }
})

// app.on("browser-window-blur", (event, window) => {
//   console.log("Window Blur", window)
// })

app.on('activate', () => {
  newMainWindow()
})

function showAlert(title, message) {
  const { dialog } = require('electron')
  dialog.showMessageBox({
    title: title,
    message: message
  })
}

const appReady = () => {

  const detect = require('detect-port')
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

      if (mainWindow) mainWindow.webContents.send('return-port', port)
      if (deckWindow) deckWindow.webContents.send('return-port', port)

      startLMTService(port)
    }
  })

  if (closeWithoutTracker && !isCheckingTracker) checkTracker()

  console.log("Process Args:")
  console.log(process.argv)

  startHidden = process.argv.includes('--hidden')

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
    deckWindow.webContents.send('request-test-history')
  }
}


// -----------------------------------------------
// --- Auto Updater --- 
// -----------------------------------------------

autoUpdater.logger = require('electron-log')
autoUpdater.logger.transports.file.level = 'info'

autoUpdater.on('checking-for-update', () => {
  console.log("Checking for Update...")
  if (mainWindow) mainWindow.webContents.send('checking-for-update')
})

autoUpdater.on('update-available', (info) => {
  console.log("Update available")
  console.log("Version", info.version)
  console.log("Release Data", info.releaseDate)
  if (mainWindow) mainWindow.webContents.send('update-available', info)
})

autoUpdater.on('update-not-available', () => {
  console.log('Update not available')
  if (mainWindow) mainWindow.webContents.send('update-not-available')
})

autoUpdater.on('download-progress', (progress) => {
  console.log(`Progress ${Math.floor(progress.percent)}`)
  if (mainWindow) mainWindow.webContents.send('download-process', progress)
})

autoUpdater.on('update-downloaded', (info) => {
  console.log("Update downloaded")
  // autoUpdater.quitAndInstall(true)
  if (mainWindow) mainWindow.webContents.send('update-downloaded', info)
})

autoUpdater.on('error', (err) => {
  console.log(err)
})

ipcMain.on('check-update', (event) => {
  checkForUpdates()
})

ipcMain.on('install-update', (event) => {
  autoUpdater.quitAndInstall(true, true)
})

ipcMain.on('game-end-trigger', () => {
  console.log("Handling Game End")
  if (mainWindow) mainWindow.webContents.send('game-end-handle')
})

ipcMain.on('get-port', (event, args) => {

  event.sender.send('return-port', port)
  // if (mainWindow) mainWindow.webContents.send('return-port', port)
  // if (deckWindow) deckWindow.webContents.send('return-port', port)
})

setInterval(() => {
  checkForUpdates()
}, 1000 * 60 * 15)

function checkForUpdates() {
  if (isWin) autoUpdater.checkForUpdates()
}

// -----------------------------------------------
// --- Tray ---
// -----------------------------------------------

let tray = null
function initTray() {
  tray = new Tray(__dirname + '/image.ico')
  const contextMenu = Menu.buildFromTemplate([
    // { label: 'Item1', type: 'radio' },
    // { label: 'Item2', type: 'radio' },
    // { label: 'Item3', type: 'radio', checked: true },
    // { label: 'Item4', type: 'radio' },
    { 
      label: 'Open',
      click: () => {
        newMainWindow()
      }
    },
    {
      label: 'About',
      click: () => { newInfoWindow() }
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => { app.quit() }
    }
  ])
  tray.setToolTip('LoR Master Tracker')
  tray.on('click', ()=>{
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
menu.append(new MenuItem({
  label: 'Electron',
  submenu: [{
    role: 'help',
    accelerator: process.platform === 'darwin' ? 'Alt+Cmd+I' : 'Alt+Shift+I',
    click: () => { 
      console.log('New Info Window') 
      newInfoWindow()
    }
  }]
}))

Menu.setApplicationMenu(menu)

// -----------------------------------------------
// --- Backend Service ---
// -----------------------------------------------

function startLMTService(port) {

  console.log("--------------------")
  console.log("Starting LMT Service", "Port equals to: ", port)
  console.log("--------------------")

  const { spawn } = require('child_process')

  var proc

  if (spawnPython) {
    proc = spawn('python', ['./LMTService.py', `--port=${port}`], {cwd: '../'})
  } else {
    var backend
    if (app.isPackaged) {
      var execPath = path.dirname(app.getPath('exe'))
      backend = path.join(execPath, 'backend', 'LMTService', 'LMTService.exe')
      proc = spawn(backend, [`--port=${port}`], {cwd: path.join(execPath, 'backend', 'LMTService')})
      
    } else {
      backend = path.join(__dirname, 'backend', 'LMTService', 'LMTService.exe')
      proc = spawn(backend, [`--port=${port}`], {cwd: path.join(__dirname, 'backend', 'LMTService')})
    }
  }
  
  proc.stdout.on('data', function (data) {
    console.log("data: ", data.toString('utf8'))
  })
  proc.stderr.on('data', (data) => {
    // console.log(`stderr: ${data}`) // when error
  })

  proc.on('close', (code) => {
    console.log(`Child process close all stdio with code ${code}`)
    startLMTService(port)
  })
  proc.on('exit', (code) => {
    console.log(`Child process exited with code ${code}`)
  })

}

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

  let {width, height} = electron.screen.getPrimaryDisplay().workAreaSize

  // --- mainWindow ---
  let windowWidth = 800 // (335)
  let windowMaxWidth = 1200
  let windowMinWidth = 700
  let windowHeight = height * 0.7
  // let windowXPadding = 200
  // let windowYPadding = 20
  let xOffSet = 0

  if (developmentMode) {
    windowWidth = windowWidth + 400
    windowMaxWidth = windowWidth + 400
    xOffSet = 350
  }

  mainWindow = new BrowserWindow({
    maxWidth: windowMaxWidth,
    minWidth: windowMinWidth,
    minHeight: headerHeight,
    width: windowWidth, 
    height: windowHeight, 
    x: (width - windowWidth) / 2 + xOffSet,
    y: (height - windowHeight) / 2,
    frame: false,
    resizable: true,
    show: false,
    backgroundColor: '#1c1c1f',
    webPreferences: {
      // nodeIntegration: true,
      // enableRemoteModule: true,
      contextIsolation: false,
      preload: __dirname + '/appsrc/preload.js',
    }
  })

  remote.enable(mainWindow.webContents)

  const mainWindowUrl = require('url').format({
    protocol: 'file',
    slashes: true,
    pathname: require('path').join(__dirname, 'dist', 'index.html')
  })

  // console.log(mainWindowUrl)
  // mainWindow.loadURL(`file://${__dirname}/dist/index.html`)
  mainWindow.loadURL(mainWindowUrl)
  
  // mainWindow.setAlwaysOnTop(true, level = "pop-up-menu")
  mainWindow.on('closed', () => {
    mainWindow = null
    // app.quit()
  })

  mainWindow.on('hide', () => {
  })

  mainWindow.once('ready-to-show', () => {
    
    if (!startHidden) mainWindow.show()

    mainWindow.webContents.send('app-version', currentVersion)
    mainWindow.webContents.send('debug-info-display', process.argv)
  })

  if (developmentMode) mainWindow.webContents.openDevTools()

  allWindows.push(mainWindow)
}

function newDeckWindow() {

  if (deckWindow) {
    deckWindow.show()
    return
  }

  let {width, height} = electron.screen.getPrimaryDisplay().workAreaSize
  // let factor = electron.screen.getPrimaryDisplay().scaleFactor
  // console.log("Scale Factor:", factor)

  // --- deckWindow ---
  let windowWidth = 240 // (335)
  let windowMaxWidth = 290
  let windowMinWidth = 170
  // let window.windowWidth = windowWidth
  let windowHeight = height * 0.7
  let windowPadding = 20

  if (developmentMode) {
    windowWidth = windowWidth + 400
    windowMaxWidth = windowWidth + 400
  }

  deckWindow = new BrowserWindow({
    maxWidth: windowMaxWidth,
    minWidth: windowMinWidth,
    minHeight: headerHeight,
    width: windowWidth, 
    height: windowHeight, 
    // x: width - windowWidth - windowPadding,
    // y: height - windowHeight - windowPadding,
    x: windowPadding,
    y: height / 2 - windowHeight / 2,
    frame: false,
    resizable: true,
    skipTaskbar: true,
    show: false,
    webPreferences: {
      // nodeIntegration: true,
      // enableRemoteModule: true,
      contextIsolation: false,
      preload: __dirname + '/appsrc/preload.js',
    },
    // show: false
    // titleBarStyle: 'hiddenInset'
  })

  remote.enable(deckWindow.webContents)
  // deckWindow.loadURL(require('url').format({
  //   pathname: path.join(__dirname, 'dist/index.html'),
  //   protocol: 'file:',
  //   slashes: true
  // }))
  // deckWindow.hide()
  
  deckWindow.loadURL(`file://${__dirname}/dist/deck.html`)
  
  // console.log("Is development?", process.env.NODE_ENV === 'development')

  // Attempted to use a bug? to turn off snapAssist on Windows
  // if (!snapAssist) { 
  //   var minSize = deckWindow.getMinimumSize()
  //   var maxSize = deckWindow.getMaximumSize()
    
  //   deckWindow.setResizable(true)
  //   deckWindow.setMinimumSize(minSize[0], minSize[1])
  //   deckWindow.setMaximumSize(maxSize[0], maxSize[1])
  //   // deckWindow.setMinimumSize
  // }

  // deckWindow.removeMenu()
  deckWindow.setAlwaysOnTop(true, level = "pop-up-menu")
  deckWindow.on('closed', () => {
    deckWindow = null
  })

  deckWindow.on('restore', () => {
    deckWindow.setSkipTaskbar(true)
  })

  deckWindow.on('minimize', () => {
    deckWindow.setSkipTaskbar(false)
  })

  if (developmentMode) deckWindow.webContents.openDevTools()

  allWindows.push(deckWindow)
}

function newInfoWindow() {

  if (infoWindow) {
    infoWindow.show()
    return
  }

  let {width, height} = electron.screen.getPrimaryDisplay().workAreaSize
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
      preload: __dirname + '/appsrc/preload.js',
    }
    // titleBarStyle: 'hiddenInset'
  })

  remote.enable(infoWindow.webContents)

  infoWindow.loadURL(`file://${__dirname}/dist/info.html`)
  // console.log("Is development?", process.env.NODE_ENV === 'development')

  infoWindow.setAlwaysOnTop(true, level = "pop-up-menu")
  infoWindow.on('closed', () => {
    infoWindow = null
  })

  if (developmentMode) infoWindow.webContents.openDevTools()

  allWindows.push(infoWindow)
}

function showDeckWindow() {
  try {
    deckWindow.webContents.executeJavaScript('window.showWindow()')  
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
    deckWindow.webContents.executeJavaScript('window.toggleWindow()')  
  } catch (e) {
    console.log(e)
  }
}


// -----------------------------------------------
// --- Alerts ---
// -----------------------------------------------

function newAlert() {


}

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

var AutoLaunch = require('auto-launch')
var autoLauncher = new AutoLaunch({
    name: 'LoR Master Tracker',
    isHidden: true
})

function checkAutoLaunch() {

  autoLauncher.isEnabled().then(
    function(isEnabled) {
      console.log("Auto Launch Enabled: ", isEnabled)
      sendAutoLaunchToMain(isEnabled)
    }
  ).catch(function(err){
      console.log(err)
  })
}

function sendAutoLaunchToMain(isEnabled) {
  if (mainWindow) (mainWindow.webContents.send('check-auto-launch-return', isEnabled))
}

ipcMain.on('check-auto-launch', (event, args) => {
  checkAutoLaunch()
})

ipcMain.on('set-auto-launch', (event, enable) => {
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

const Store = require('electron-store');
const store = new Store();

console.log("Storing data at", app.getPath('userData'))

if (store.get('ui-locale') == null) {
  // First time language setting
  var systemLang = getEnvLocale()
  console.log("No Language Set | System Locale", systemLang)

  var newLocale = ""

  if (!systemLang) {
    newLocale = 'English'
  } else if (systemLang.includes('zh_CN')) {
    // 简体中文
    newLocale = '简体中文'
  } else if (systemLang.includes('zh')) {
    // 繁体中文
    newLocale = '繁體中文'
  }

  if (newLocale != "") {
    store.set('ui-locale', newLocale)

    BrowserWindow.getAllWindows().forEach(bw => {
        console.log("-- sending to", bw.id)
        bw.webContents.send('to-change-locale', newLocale) 
    });
  }
  

} else {
  console.log('Language set to', store.get('ui-locale'), " | System Locale", getEnvLocale())
}

ipcMain.on('request-store', (event, key) => {
  event.sender.send('reply-store', key, store.get(key));
});

ipcMain.on('save-store', (event, key, val) => {
  store.set(key, val)
});

// -----------------------------------------------
// --- Locale ---
// -----------------------------------------------

ipcMain.on('changed-locale', (event, newLocale) => {
  console.log("Changing Locale to", newLocale, ", from", event.sender.id)
  store.set('ui-locale', newLocale)

  BrowserWindow.getAllWindows().forEach(bw => {
    if (bw && bw.webContents.id != event.sender.id) {
      console.log("-- sending to", bw.webContents.id)
      bw.webContents.send('to-change-locale', newLocale)
    } else {
      console.log("-- not sending to", bw.webContents.id)
    }
  });
})

function getEnvLocale(env) {
  env = env || process.env;

  return env.LC_ALL || env.LC_MESSAGES || env.LANG || env.LANGUAGE;
}

// --- Use these to check for old running python app ---

const tasklist = require('tasklist')
const { cp } = require('fs')
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

var isCheckingTracker = false
async function checkTracker() {

  isCheckingTracker = true
  
  // Check Python Process with window name containing LoR Master Tracker
  var pythonList = await tasklist({filter: ["IMAGENAME eq python.exe"], verbose: true})
  pythonList = pythonList.filter(ps => ps.windowTitle.indexOf("LoR Master Tracker") != -1)

  // Check LoRMasterTracker.exe process
  var trackerList = await tasklist({filter: ["IMAGENAME eq LoRMasterTracker.exe"], verbose: false})
  
  // console.log(list.filter(ps => ps.imageName.indexOf('python') != -1))
  // console.log("\n pythonList", pythonList.length)
  // console.log("trackerList", trackerList.length)

  if (pythonList.length + trackerList.length <= 0) {
    // There is no tracker running
    console.log("No tracker running")
    // app.quit()
    if (deckWindow) deckWindow.close()
    // app.exit()
  } else {
    // if (!deckWindow) appReady()
  }

  setTimeout(checkTracker, 1000)
}

// checkTracker()