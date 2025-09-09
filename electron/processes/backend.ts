import { app } from "electron";
import { ChildProcessWithoutNullStreams, spawn } from "child_process";
import chokidar from "chokidar";
import path from "path";

const backendSrcFolder = path.join(__dirname, "../../../backend");
let backendProcess: ChildProcessWithoutNullStreams | null = null;

function killBackend() {
  if (backendProcess) {
    backendProcess.kill();
  }
}

function startBackend() {
  killBackend();

  const pyPath = path.join(__dirname, "../../../.venv/bin/python");
  const script = path.join(backendSrcFolder, "server.py");

  backendProcess = spawn(pyPath, [script], {
    cwd: backendSrcFolder,
    env: {
      ...process.env,
      DATA_DIR: app.getPath("userData"),
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
    ignored: (path, stats) => !!stats?.isFile() && !path.endsWith(".py"),
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

export { killBackend, startBackend, watchBackend };
