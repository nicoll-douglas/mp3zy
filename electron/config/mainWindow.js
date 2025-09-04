const path = require("path");

const mainWindowConfig = {
  width: 1000,
  height: 800,
  webPreferences: {
    contextIsolation: true,
    nodeIntegration: false,
    preload: path.join(__dirname, "../preload/mainWindow.js"),
  },
};

module.exports = mainWindowConfig;
