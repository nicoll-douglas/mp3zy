const { BrowserWindow } = require("electron");
const mainWindowConfig = require("../config/mainWindow.js");

function createMainWindow() {
  const mainWindow = new BrowserWindow(mainWindowConfig);

  if (process.env.APP_ENV === "development") {
    mainWindow.once("ready-to-show", () => {
      mainWindow.showInactive();
      mainWindow.minimize();
    });

    mainWindow.loadURL("http://127.0.0.1:5173");
  } else {
    mainWindow.loadFile(path.join(__dirname, "../../dist/index.html"));
  }
}

module.exports = { createMainWindow };
