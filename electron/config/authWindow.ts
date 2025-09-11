import { BrowserWindowConstructorOptions } from "electron";

const authWindowConfig: BrowserWindowConstructorOptions = {
  width: 500,
  height: 600,
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
  },
};

export default authWindowConfig;
