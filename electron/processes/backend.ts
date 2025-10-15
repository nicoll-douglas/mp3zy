import { app } from "electron";
import { ChildProcessWithoutNullStreams, spawn } from "child_process";
import chokidar from "chokidar";
import path from "path";
import logger from "../services/logger";

const backendSrcFolder = path.join(__dirname, "../../../backend");
let backendProcess: ChildProcessWithoutNullStreams | null = null;

/**
 * Kill the backend Python process of the application.
 */
function killBackend() {
  if (backendProcess) {
    logger.debug("Killing existing backend process...");
    backendProcess.kill();
  }
}

/**
 * Registers event handlers for the backend process.
 *
 * @param proc The backend process.
 */
function registerBackendEventHandlers(proc: ChildProcessWithoutNullStreams) {
  proc.stdout.pipe(process.stdout);
  proc.stderr.pipe(process.stderr);

  proc.on("error", logger.error);
  proc.stdout.on("error", logger.error);

  proc.on("spawn", () => {
    logger.info("Backend process spawned.");
  });

  proc.on("close", (code, signal) => {
    if (code) {
      logger.info(`Backend process exited with code ${code}.`);
      return;
    }

    if (signal) {
      logger.info(`Backend process terminated with signal ${signal}.`);
      return;
    }

    logger.warn(
      "Abnormal termination of backend process, no code or signal was captured."
    );
  });
}

/**
 * Starts the backend Python process of the application.
 */
function startBackend() {
  killBackend();

  const pyPath = path.join(__dirname, "../../../.venv/bin/python");
  const script = path.join(backendSrcFolder, "app.py");
  const spawnOptions = {
    cwd: backendSrcFolder,
    env: {
      USER_DATA_DIR: app.getPath("userData"),
      APP_NAME: process.env.VITE_APP_NAME,
      FRONTEND_APP_URL: process.env.VITE_APP_URL,
      APP_ENV: process.env.APP_ENV,
      SPOTIFY_CLIENT_ID: process.env.SPOTIFY_CLIENT_ID,
      SPOTIFY_REDIRECT_URI: process.env.SPOTIFY_REDIRECT_URI,
    },
  };

  backendProcess = spawn(pyPath, [script], spawnOptions);
  registerBackendEventHandlers(backendProcess);
}

/**
 * Starts the backend Python process of the application in watch mode.
 */
function watchBackend() {
  const watcher = chokidar.watch(backendSrcFolder, {
    ignored: (path, stats) => !!stats?.isFile() && !path.endsWith(".py"),
    ignoreInitial: true,
  });

  watcher.on("all", (event, filePath) => {
    logger.info(
      `Backend source file ${filePath} changed with event ${event}, restarting backend...`
    );
    startBackend();
  });

  watcher.on("ready", () => {
    logger.info("Watching backend source files for changes...");
  });
}

export { killBackend, startBackend, watchBackend };
