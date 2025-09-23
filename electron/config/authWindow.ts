import { BrowserWindowConstructorOptions } from "electron";

// configuration for the window where service authentication happens
const authWindowConfig: BrowserWindowConstructorOptions = {
  width: 500,
  height: 600,
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
  },
};

export default authWindowConfig;
