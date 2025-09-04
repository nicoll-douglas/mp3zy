const fs = require("fs");
const { app } = require("electron");
let savePath = app.getPath("music");

if (!fs.existsSync(savePath)) {
  savePath = app.getPath("home");
}

const defaultSettings = {
  savePath,
};

module.exports = defaultSettings;
