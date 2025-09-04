import path from "path";

const mainWindowConfig = {
  width: 1000,
  height: 800,
  show: process.env.APP_ENV !== "development",
  webPreferences: {
    contextIsolation: true,
    nodeIntegration: false,
    preload: path.join(__dirname, "../preload/mainWindow.js"),
  },
};

export default mainWindowConfig;
