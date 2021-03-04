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

let mainWindow = null
const createWindow = () => {
  let {width, height} = electron.screen.getPrimaryDisplay().workAreaSize;
  let factor = electron.screen.getPrimaryDisplay().scaleFactor
  // console.log(width)
  let windowWidth = 360
  let windowHeight = Math.floor(windowWidth*1.666)


  mainWindow = new BrowserWindow({ 
    width: windowWidth, 
    height: windowHeight, 
    x: width,
    y: height - windowHeight,
    frame: false,
    webPreferences: {
      preload: __dirname + '/preload.js',
      enableRemoteModule: true,
      // nodeIntegration: true,
    }
    // titleBarStyle: 'hiddenInset'
  })
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'dist/index.html'),
    protocol: 'file:',
    slashes: true
  }))
  // console.log("Is development?", process.env.NODE_ENV === 'development')
  // mainWindow.webContents.openDevTools()
  mainWindow.removeMenu()
  mainWindow.on('closed', () => {
    mainWindow = null
  })
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