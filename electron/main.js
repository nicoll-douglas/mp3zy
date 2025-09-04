require("dotenv").config();

const { app, BrowserWindow } = require("electron");

const { createMainWindow } = require("./windows/mainWindow.js");
const {
  startBackend,
  killBackend,
  watchBackend,
} = require("./processes/backend.js");

app.whenReady().then(() => {
  startBackend();
  if (process.env.APP_ENV === "development") {
    watchBackend();
  }
  createMainWindow();
});

app.on("will-quit", () => {
  killBackend();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createMainWindow();
  }
});
