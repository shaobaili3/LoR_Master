// const electron = require('electron')
// const app = electron.app
// const BrowserWindow = electron.BrowserWindow

// let url
// if (!process.env.NODE_ENV === 'production') {
//   url = 'http://localhost:8080/'
// } else {
//   url = `file://${process.cwd()}/dist/index.html`
// }

// app.on('ready', () => {
//   let window = new BrowserWindow({width: 800, height: 600})
//   window.loadURL(url)
// })


const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')

// const server = require('./appsrc/server.js')
// server.run

const developmentMode = false
const snapAssist = false
const headerHeight = 45 // Repeated in preload.js
const defaultRatio = 2.3 // Repeated in preload.js

// const client = require('./appsrc/client.js')

const zmq = require("zeromq")

// async function runClient() {
//     const sock = new zmq.Subscriber
  
//     sock.connect("tcp://127.0.0.1:3000")
//     sock.subscribe("kitty cats")
//     console.log("Subscriber connected to port 3000")
  
//     for await (const [topic, msg] of sock) {
//       console.log("received a message related to:", topic.toString(), "containing message:", msg.toString())
//       mainWindow.clientData = "CATAT"
//       // console.log(mainWindow)
//     }
// }

let mainWindow = null
const createWindow = () => {


  let {width, height} = electron.screen.getPrimaryDisplay().workAreaSize;
  let factor = electron.screen.getPrimaryDisplay().scaleFactor
  // console.log(width)
  let windowWidth = 335
  // let window.windowWidth = windowWidth
  let windowHeight = Math.floor(windowWidth*defaultRatio)
  let windowPadding = 20

  if (developmentMode) {
    windowWidth = windowWidth + 400
  }

  mainWindow = new BrowserWindow({
    maxWidth: windowWidth,
    minWidth: windowWidth,
    minHeight: headerHeight,
    width: windowWidth, 
    height: windowHeight, 
    x: width - windowWidth - windowPadding,
    y: height - windowHeight - windowPadding,
    frame: false,
    resizable: snapAssist,
    webPreferences: {
      preload: __dirname + '/appsrc/preload.js',
      enableRemoteModule: true,
      // nodeIntegration: true,
      nodeIntegrationInWorker: true,
    }
    // titleBarStyle: 'hiddenInset'
  })
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'dist/index.html'),
    protocol: 'file:',
    slashes: true
  }))
  // console.log("Is development?", process.env.NODE_ENV === 'development')
  
  if (!snapAssist) { 
    var minSize = mainWindow.getMinimumSize()
    var maxSize = mainWindow.getMaximumSize()
    
    mainWindow.setResizable(true)
    mainWindow.setMinimumSize(minSize[0], minSize[1])
    mainWindow.setMaximumSize(maxSize[0], maxSize[1])
    // mainWindow.setMinimumSize
  }
  mainWindow.removeMenu()
  mainWindow.setAlwaysOnTop(true, level = "pop-up-menu")
  mainWindow.on('closed', () => {
    mainWindow = null
  })

  if (developmentMode) mainWindow.webContents.openDevTools()
  
  mainWindow.webContents.on('new-window', function (evt, url, frameName, disposition, options, additionalFeatures) {
    if(options.width == 800 && options.height == 600){ //default size is 800x600
        
        options.width = windowWidth | 0;
        options.height = windowHeight | 0;
        
        options.x = 1440 - windowWidth * 2;
        // console.log(width);
        options.y = height - windowHeight;
        // options.titleBarStyle = 'hidden'
        options.frame = true;
    }
  });

  // const worker = new Worker(__dirname + '/electron/server.js')
  // server.run
  // runClient()
}

app.on('ready', createWindow)
app.on('window-all-closed', () => {
  // if (process.platform !== 'darwin') {
    app.quit()
  // }
})
app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

// console.log("Activated Electron");