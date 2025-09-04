const { loadSettings } = require("../utils/settings.js");
const { app } = require("electron");
const { spawn } = require("child_process");
const chokidar = require("chokidar");

const backendSrcFolder = path.join(__dirname, "../../backend");
let backendProcess;

function killBackend() {
  if (backendProcess) {
    backendProcess.kill();
  }
}

function startBackend() {
  killBackend();

  const pyPath = path.join(__dirname, "../../.venv/bin/python");
  const script = path.join(backendSrcFolder, "server.py");
  const settings = loadSettings();

  backendProcess = spawn(pyPath, [script], {
    cwd: path.join(__dirname, "../../backend"),
    env: {
      ...process.env,
      SAVE_PATH: settings.savePath,
      DATA_DIR: app.getAppPath("userData"),
    },
  });

  backendProcess.stdout.on("data", (data) => {
    console.log(`[BACKEND]: ${data}`);
  });

  backendProcess.stderr.on("data", (data) => {
    console.error(`[BACKEND]: ${data}`);
  });

  backendProcess.on("close", (code) => {
    console.log(`Backend Python process exited with code ${code}`);
  });
}

function watchBackend() {
  const watcher = chokidar.watch(backendSrcFolder, {
    ignored: (path, stats) => stats?.isFile() && !path.endsWith(".py"),
    ignoreInitial: true,
  });

  watcher.on("all", (event, filePath) => {
    console.log(`Backend source file changed: ${filePath} (${event})`);
    console.log("Restarting backend...");
    startBackend();
  });

  watcher.on("ready", () => {
    console.log("Watching backend files for changes...");
  });
}

module.exports = { killBackend, startBackend, watchBackend };
