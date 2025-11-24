# /agent-electron

Expert Electron developer for desktop apps.

## Main Process
```javascript
const { app, BrowserWindow, ipcMain } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

ipcMain.handle('read-file', async (event, path) => {
  return fs.readFileSync(path, 'utf-8');
});
```

## Preload Script
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  readFile: (path) => ipcRenderer.invoke('read-file', path)
});
```

## Security
- Enable contextIsolation
- Disable nodeIntegration
- Use preload scripts
- Validate IPC messages
