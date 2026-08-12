#!/usr/bin/env node
// Cross-platform local runner for AI Solopreneur.
//
// One Node.js script replaces the previous Docker Compose path for learners:
// it installs the pinned n8n engine with npm, builds the dependency-free chat
// gateway and document reader, runs all three as background processes, and
// provides the same setup,
// import, diagnose, backup, restore, and reset helpers on macOS and Windows.
//
// Learners normally reach this through setup.command / setup-windows.cmd and
// friends. Technical users can call it directly:
//
//   node scripts/local.mjs help

import { spawn, spawnSync } from "node:child_process";
import {
  closeSync,
  cpSync,
  existsSync,
  mkdirSync,
  openSync,
  readFileSync,
  readdirSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { chmod, copyFile, mkdir, readFile, rm } from "node:fs/promises";
import { request as httpRequest } from "node:http";
import net from "node:net";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { createInterface } from "node:readline/promises";
import { fileURLToPath } from "node:url";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const isWindows = process.platform === "win32";

const rootPackage = JSON.parse(
  readFileSync(join(projectRoot, "package.json"), "utf8"),
);
const pinnedN8nVersion = rootPackage.dependencies.n8n;
const chatDatabaseSchemaVersion = 5;

const paths = {
  envFile: join(projectRoot, ".env"),
  dataDir: join(projectRoot, "data"),
  n8nUserFolder: join(projectRoot, "data", "n8n"),
  n8nDataDir: join(projectRoot, "data", "n8n", ".n8n"),
  logsDir: join(projectRoot, "data", "logs"),
  runDir: join(projectRoot, "data", "run"),
  tmpDir: join(projectRoot, "data", "tmp"),
  n8nBin: join(projectRoot, "node_modules", "n8n", "bin", "n8n"),
  n8nPackage: join(projectRoot, "node_modules", "n8n", "package.json"),
  chatDir: join(projectRoot, "apps", "chat"),
  chatServer: join(projectRoot, "apps", "chat", "dist", "server.js"),
  agentRegistry: join(projectRoot, "apps", "chat", "config", "agents.json"),
  chatDataDir: join(projectRoot, "data", "chat"),
  chatDatabase: join(projectRoot, "data", "chat", "chat.sqlite"),
  documentWorkerDir: join(projectRoot, "services", "document-worker"),
  documentWorkerServer: join(
    projectRoot,
    "services",
    "document-worker",
    "src",
    "server.mjs",
  ),
  documentWorkerDependency: join(
    projectRoot,
    "services",
    "document-worker",
    "node_modules",
    "jszip",
    "package.json",
  ),
  documentDataDir: join(projectRoot, "data", "documents"),
  workflowsDir: join(projectRoot, "n8n", "workflows"),
  backupsDir: join(projectRoot, "backups"),
};

const workflowIds = {
  main: "phase3StartHere",
  health: "phase3AgentHealth",
  checklist: "phase6LearnerChecklist",
  taskSetup: "phase4TaskSetup",
  skillSync: "phase5SyncEnabledSkills",
  tools: [
    "phase4ListTasks",
    "phase4CreateTask",
    "phase4UpdateTaskStatus",
    "phase5ProposeCreateTask",
    "phase5ProposeTaskStatus",
    "phase5ConfirmTaskWrite",
    "phase9StartDomainResearch",
    "phase9CompleteDomainResearch",
    "phase9GetBusinessMemory",
    "phase11StartPaidDomainResearch",
    "phase11CompletePaidDomainResearch",
    "phase11GetPaidDomainResearch",
    "phase13StartSeoArticle",
    "phase13WriteSeoArticle",
    "phase13GetSeoArticle",
  ],
};

const exportedWorkflowFiles = [
  ["phase3StartHere", "00-start-here-project-partner.json"],
  ["phase6LearnerChecklist", "01-start-here-learner-checklist.json"],
  ["phase4TaskSetup", "10-setup-local-task-data.json"],
  ["phase5SyncEnabledSkills", "11-setup-sync-enabled-skills.json"],
  ["phase4ListTasks", "20-tool-list-tasks.json"],
  ["phase4CreateTask", "21-tool-create-task.json"],
  ["phase4UpdateTaskStatus", "22-tool-update-task-status.json"],
  ["phase5ProposeCreateTask", "30-tool-propose-create-task.json"],
  ["phase5ProposeTaskStatus", "31-tool-propose-update-task-status.json"],
  ["phase5ConfirmTaskWrite", "40-confirm-task-write.json"],
  ["phase9StartDomainResearch", "50-tool-start-domain-research.json"],
  ["phase9CompleteDomainResearch", "51-tool-complete-domain-research.json"],
  ["phase9GetBusinessMemory", "52-tool-get-business-memory.json"],
  ["phase11StartPaidDomainResearch", "53-tool-start-paid-domain-research.json"],
  ["phase11CompletePaidDomainResearch", "54-tool-complete-paid-domain-research.json"],
  ["phase11GetPaidDomainResearch", "55-tool-get-paid-domain-research.json"],
  ["phase13StartSeoArticle", "56-tool-start-seo-article.json"],
  ["phase13WriteSeoArticle", "57-internal-write-seo-article.json"],
  ["phase13GetSeoArticle", "58-tool-get-seo-article.json"],
  ["phase3AgentHealth", "90-debug-agent-health.json"],
];

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

function readEnvFile() {
  const values = new Map();
  if (!existsSync(paths.envFile)) {
    return values;
  }
  for (const line of readFileSync(paths.envFile, "utf8").split(/\r?\n/)) {
    const match = /^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/.exec(line);
    if (match) {
      values.set(match[1], match[2]);
    }
  }
  return values;
}

function systemTimezone() {
  try {
    return (
      Intl.DateTimeFormat().resolvedOptions().timeZone || "Australia/Melbourne"
    );
  } catch {
    return "Australia/Melbourne";
  }
}

function config() {
  const file = readEnvFile();
  const value = (key, fallback) => {
    const fromProcess = process.env[key];
    if (fromProcess !== undefined && fromProcess !== "") {
      return fromProcess;
    }
    const fromFile = file.get(key);
    return fromFile !== undefined && fromFile !== "" ? fromFile : fallback;
  };

  const chatPort = Number(value("CHAT_PORT", "3000"));
  const n8nPort = Number(value("N8N_PORT", "5678"));
  const documentWorkerPort = Number(value("DOCUMENT_WORKER_PORT", "3100"));
  const timezone = value("GENERIC_TIMEZONE", systemTimezone());

  // The Docker path stored the n8n encryption key in .env. Native n8n manages
  // its own key inside data/n8n, but honouring an existing real key keeps old
  // backups restorable. Placeholders from .env.example are ignored.
  const envKey = value("N8N_ENCRYPTION_KEY", "");
  const encryptionKey =
    envKey.length >= 32 && !envKey.startsWith("replace-") ? envKey : "";

  return {
    chatPort,
    n8nPort,
    documentWorkerPort,
    timezone,
    encryptionKey,
  };
}

function validPort(port) {
  return Number.isInteger(port) && port >= 1 && port <= 65535;
}

function n8nEnv(cfg) {
  const env = {
    GENERIC_TIMEZONE: cfg.timezone,
    TZ: cfg.timezone,
    N8N_BLOCK_ENV_ACCESS_IN_NODE: "true",
    N8N_COMMUNITY_PACKAGES_ENABLED: "false",
    N8N_COMPRESSION_NODE_MAX_DECOMPRESSED_SIZE_BYTES: "268435456",
    N8N_COMPRESSION_NODE_MAX_ZIP_ENTRIES: "1000",
    N8N_DIAGNOSTICS_ENABLED: "false",
    N8N_EDITOR_BASE_URL: `http://localhost:${cfg.n8nPort}`,
    N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS: "true",
    N8N_HOST: "localhost",
    N8N_LISTEN_ADDRESS: "127.0.0.1",
    N8N_PERSONALIZATION_ENABLED: "false",
    N8N_PORT: String(cfg.n8nPort),
    N8N_PROTOCOL: "http",
    N8N_RUNNERS_TASK_TIMEOUT: "60",
    N8N_SECURE_COOKIE: "false",
    N8N_UNVERIFIED_PACKAGES_ENABLED: "false",
    N8N_USER_FOLDER: paths.n8nUserFolder,
    N8N_VERSION_NOTIFICATIONS_ENABLED: "false",
    N8N_WEBHOOK_URL: `http://localhost:${cfg.n8nPort}/`,
  };
  if (cfg.encryptionKey) {
    env.N8N_ENCRYPTION_KEY = cfg.encryptionKey;
  }
  return env;
}

function chatEnv(cfg) {
  return {
    NODE_ENV: "production",
    PORT: String(cfg.chatPort),
    AGENT_REGISTRY_PATH: paths.agentRegistry,
    CHAT_LISTEN_ADDRESS: "127.0.0.1",
    CHAT_REQUEST_TIMEOUT_MS: "120000",
    CHAT_DATA_DIRECTORY: paths.chatDataDir,
    DOCUMENT_DATA_DIRECTORY: paths.documentDataDir,
    DOCUMENT_WORKER_URL: `http://127.0.0.1:${cfg.documentWorkerPort}`,
    N8N_CHAT_WEBHOOK_URL: `http://127.0.0.1:${cfg.n8nPort}/webhook/chat`,
  };
}

function documentWorkerEnv(cfg) {
  return {
    NODE_ENV: "production",
    PORT: String(cfg.documentWorkerPort),
    DOCUMENT_LISTEN_ADDRESS: "127.0.0.1",
  };
}

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------

function print(message = "") {
  process.stdout.write(`${message}\n`);
}

function printError(message) {
  process.stderr.write(`${message}\n`);
}

function ensureDirs() {
  for (const dir of [
    paths.dataDir,
    paths.n8nUserFolder,
    paths.documentDataDir,
    paths.logsDir,
    paths.runDir,
    paths.tmpDir,
  ]) {
    mkdirSync(dir, { recursive: true });
  }
}

function sleep(ms) {
  return new Promise((resolveSleep) => setTimeout(resolveSleep, ms));
}

function tmpPath(name) {
  ensureDirs();
  return join(paths.tmpDir, name);
}

function timestamp() {
  const now = new Date();
  const pad = (part) => String(part).padStart(2, "0");
  return (
    `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}` +
    `-${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`
  );
}

function tailOfFile(path, lines = 30) {
  try {
    const content = readFileSync(path, "utf8");
    return content.split(/\r?\n/).slice(-lines).join("\n");
  } catch {
    return "(no log output captured yet)";
  }
}

async function confirmPhrase(prompt, phrase) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  try {
    const answer = (await rl.question(prompt)).trim();
    return answer === phrase;
  } finally {
    rl.close();
  }
}

function portInUse(port) {
  return new Promise((resolvePort) => {
    const socket = net.connect({ port, host: "127.0.0.1" });
    let settled = false;
    const finish = (result) => {
      if (!settled) {
        settled = true;
        socket.destroy();
        resolvePort(result);
      }
    };
    socket.once("connect", () => finish(true));
    socket.once("error", () => finish(false));
    socket.setTimeout(1_000, () => finish(false));
  });
}

function fetchStatus(url, options = {}, timeoutMs = 5_000) {
  return new Promise((resolveStatus) => {
    const body = options.body;
    const headers = { ...(options.headers ?? {}) };
    if (
      body !== undefined &&
      !Object.keys(headers).some((name) => name.toLowerCase() === "content-length")
    ) {
      headers["Content-Length"] = Buffer.byteLength(body);
    }
    let settled = false;
    const finish = (value) => {
      if (!settled) {
        settled = true;
        resolveStatus(value);
      }
    };
    const request = httpRequest(
      url,
      {
        method: options.method ?? "GET",
        headers,
      },
      (response) => {
        const chunks = [];
        response.setEncoding("utf8");
        response.on("data", (chunk) => chunks.push(chunk));
        response.on("end", () => {
          const status = response.statusCode ?? 0;
          finish({
            status,
            ok: status >= 200 && status < 300,
            body: chunks.join(""),
          });
        });
        response.on("error", () => finish(null));
      },
    );
    request.setTimeout(timeoutMs, () => {
      request.destroy(new Error("Local health request timed out"));
    });
    request.on("error", () => finish(null));
    if (body !== undefined) {
      request.write(body);
    }
    request.end();
  });
}

// ---------------------------------------------------------------------------
// Node and npm checks
// ---------------------------------------------------------------------------

const REQUIRED_NODE_MAJOR = 24;

function nodeMajor() {
  return Number(process.versions.node.split(".")[0]);
}

function assertNodeVersion() {
  if (nodeMajor() < REQUIRED_NODE_MAJOR) {
    printError(
      `This project needs Node.js ${REQUIRED_NODE_MAJOR} (LTS) or newer; ` +
        `this computer has ${process.versions.node}.`,
    );
    printError(
      "Run setup.command (macOS) or setup-windows.cmd (Windows) so the project can use its verified private Node.js copy.",
    );
    process.exit(1);
  }
}

function runNpm(args, { cwd, label }) {
  const result = spawnSync("npm", args, {
    cwd,
    stdio: "inherit",
    shell: isWindows,
    env: { ...process.env },
  });
  if (result.error) {
    throw new Error(
      `npm is not available (${result.error.message}). ` +
        "Rerun the command through the supplied project helper so it can use the matching private npm copy.",
    );
  }
  if (result.status !== 0) {
    throw new Error(`${label} did not finish successfully (npm exit ${result.status}).`);
  }
}

// ---------------------------------------------------------------------------
// n8n CLI
// ---------------------------------------------------------------------------

function requireLocalInstall() {
  if (!existsSync(paths.n8nBin)) {
    throw new Error(
      "Local setup has not been completed. " +
        "Double-click setup.command (macOS) or setup-windows.cmd (Windows) first.",
    );
  }
}

function ensureDocumentWorkerInstalled() {
  if (existsSync(paths.documentWorkerDependency)) {
    return;
  }
  print("Installing the local document reader...");
  runNpm(["ci", "--no-audit", "--no-fund", "--ignore-scripts"], {
    cwd: paths.documentWorkerDir,
    label: "Installing the local document reader",
  });
}

function chatBuildIsStale() {
  if (!existsSync(paths.chatServer)) {
    return true;
  }
  try {
    const builtAt = statSync(paths.chatServer).mtimeMs;
    const sourceDir = join(paths.chatDir, "src");
    return readdirSync(sourceDir).some(
      (entry) => statSync(join(sourceDir, entry)).mtimeMs > builtAt,
    );
  } catch {
    return true;
  }
}

function ensureChatBuilt() {
  if (!chatBuildIsStale()) {
    return;
  }
  print("Building the local chat app...");
  if (!existsSync(join(paths.chatDir, "node_modules", "typescript"))) {
    runNpm(["ci", "--no-audit", "--no-fund", "--ignore-scripts"], {
      cwd: paths.chatDir,
      label: "Installing the chat build tools",
    });
  }
  runNpm(["run", "build"], {
    cwd: paths.chatDir,
    label: "Building the chat app",
  });
}

function installedN8nVersion() {
  try {
    return JSON.parse(readFileSync(paths.n8nPackage, "utf8")).version;
  } catch {
    return null;
  }
}

function runN8nCli(args, { capture = false } = {}) {
  const cfg = config();
  const result = spawnSync(process.execPath, [paths.n8nBin, ...args], {
    env: { ...process.env, ...n8nEnv(cfg) },
    encoding: "utf8",
    stdio: capture ? ["ignore", "pipe", "pipe"] : ["ignore", "inherit", "inherit"],
    maxBuffer: 64 * 1024 * 1024,
  });
  return result;
}

function n8nCliOrThrow(args, label) {
  const result = runN8nCli(args, { capture: true });
  if (result.status !== 0) {
    const detail = `${result.stderr || ""}${result.stdout || ""}`
      .split(/\r?\n/)
      .filter(Boolean)
      .slice(-8)
      .join("\n");
    throw new Error(`${label} failed.\n${detail}`);
  }
  return result;
}

// ---------------------------------------------------------------------------
// Background services
// ---------------------------------------------------------------------------

const services = {
  n8n: {
    label: "n8n",
    pidFile: () => join(paths.runDir, "n8n.pid"),
    logFile: () => join(paths.logsDir, "n8n.log"),
    argv: () => [paths.n8nBin],
    env: (cfg) => n8nEnv(cfg),
    healthUrl: (cfg) => `http://127.0.0.1:${cfg.n8nPort}/healthz`,
    port: (cfg) => cfg.n8nPort,
  },
  documentWorker: {
    label: "document reader",
    pidFile: () => join(paths.runDir, "document-worker.pid"),
    logFile: () => join(paths.logsDir, "document-worker.log"),
    argv: () => [paths.documentWorkerServer],
    env: (cfg) => documentWorkerEnv(cfg),
    healthUrl: (cfg) =>
      `http://127.0.0.1:${cfg.documentWorkerPort}/health`,
    port: (cfg) => cfg.documentWorkerPort,
  },
  chat: {
    label: "chat",
    pidFile: () => join(paths.runDir, "chat.pid"),
    logFile: () => join(paths.logsDir, "chat.log"),
    argv: () => [paths.chatServer],
    env: (cfg) => chatEnv(cfg),
    healthUrl: (cfg) => `http://127.0.0.1:${cfg.chatPort}/health`,
    port: (cfg) => cfg.chatPort,
  },
};

function readPidRecord(service) {
  try {
    const record = JSON.parse(readFileSync(service.pidFile(), "utf8"));
    return Number.isInteger(record.pid) && record.pid > 1 ? record : null;
  } catch {
    return null;
  }
}

function pidIsRunning(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error.code === "EPERM";
  }
}

function serviceIsRunning(service) {
  const record = readPidRecord(service);
  return record !== null && pidIsRunning(record.pid);
}

function rotateLog(path) {
  try {
    if (existsSync(path) && statSync(path).size > 2 * 1024 * 1024) {
      renameSync(path, `${path}.old`);
    }
  } catch {
    // Log rotation is best-effort.
  }
}

function startService(name) {
  const service = services[name];
  const cfg = config();
  if (serviceIsRunning(service)) {
    return false;
  }
  ensureDirs();
  rotateLog(service.logFile());
  const logFd = openSync(service.logFile(), "a");
  // detached keeps the services alive after the setup window closes: a new
  // session on macOS/Linux, and a console-independent process on Windows.
  const child = spawn(process.execPath, service.argv(), {
    detached: true,
    windowsHide: true,
    stdio: ["ignore", logFd, logFd],
    env: { ...process.env, ...service.env(cfg) },
  });
  closeSync(logFd);
  writeFileSync(
    service.pidFile(),
    `${JSON.stringify({ pid: child.pid, port: service.port(cfg), startedAt: new Date().toISOString() })}\n`,
  );
  child.unref();
  return true;
}

async function stopService(name) {
  const service = services[name];
  const record = readPidRecord(service);
  if (record === null || !pidIsRunning(record.pid)) {
    rmSync(service.pidFile(), { force: true });
    return false;
  }

  const politeStop = () => {
    if (isWindows) {
      spawnSync("taskkill", ["/pid", String(record.pid), "/t"], {
        stdio: "ignore",
      });
    } else {
      try {
        process.kill(-record.pid, "SIGTERM");
      } catch {
        try {
          process.kill(record.pid, "SIGTERM");
        } catch {
          // Already gone.
        }
      }
    }
  };
  const forceStop = () => {
    if (isWindows) {
      spawnSync("taskkill", ["/pid", String(record.pid), "/t", "/f"], {
        stdio: "ignore",
      });
    } else {
      try {
        process.kill(-record.pid, "SIGKILL");
      } catch {
        try {
          process.kill(record.pid, "SIGKILL");
        } catch {
          // Already gone.
        }
      }
    }
  };

  politeStop();
  // taskkill without /f usually cannot stop console services, so Windows
  // moves to a forced, tree-wide stop quickly. POSIX gives n8n the same 30
  // seconds of graceful shutdown the Docker path allowed.
  const graceMs = isWindows ? 5_000 : 30_000;
  const deadline = Date.now() + graceMs;
  while (Date.now() < deadline && pidIsRunning(record.pid)) {
    await sleep(250);
  }
  if (pidIsRunning(record.pid)) {
    forceStop();
    const forcedDeadline = Date.now() + 10_000;
    while (Date.now() < forcedDeadline && pidIsRunning(record.pid)) {
      await sleep(250);
    }
  }
  rmSync(service.pidFile(), { force: true });
  return true;
}

async function waitForService(name, { timeoutMs = 240_000 } = {}) {
  const service = services[name];
  const cfg = config();
  const url = service.healthUrl(cfg);
  const deadline = Date.now() + timeoutMs;
  let lastNotice = Date.now();

  while (Date.now() < deadline) {
    const response = await fetchStatus(url, {}, 3_000);
    if (response !== null && response.ok) {
      return;
    }
    if (!serviceIsRunning(service)) {
      throw new Error(
        `The ${service.label} service stopped while starting. Last log lines:\n` +
          `${tailOfFile(service.logFile())}\n` +
          `Full log: ${service.logFile()}`,
      );
    }
    if (Date.now() - lastNotice > 15_000) {
      print(`  Still waiting for ${service.label} to become ready...`);
      lastNotice = Date.now();
    }
    await sleep(1_000);
  }
  throw new Error(
    `Timed out waiting for ${service.label} at ${url}. Last log lines:\n` +
      `${tailOfFile(service.logFile())}\n` +
      `Full log: ${service.logFile()}`,
  );
}

async function startStack({
  waitFor = ["n8n", "documentWorker", "chat"],
} = {}) {
  const started = [];
  if (startService("n8n")) {
    started.push("n8n");
  }
  if (waitFor.includes("n8n")) {
    await waitForService("n8n");
  }
  if (startService("documentWorker")) {
    started.push("documentWorker");
  }
  if (waitFor.includes("documentWorker")) {
    await waitForService("documentWorker");
  }
  if (startService("chat")) {
    started.push("chat");
  }
  if (waitFor.includes("chat")) {
    await waitForService("chat");
  }
  return started;
}

async function restartN8n() {
  await stopService("n8n");
  startService("n8n");
  await waitForService("n8n");
}

// ---------------------------------------------------------------------------
// Workflow helpers
// ---------------------------------------------------------------------------

function readExportedRows(path) {
  const raw = JSON.parse(readFileSync(path, "utf8"));
  return Array.isArray(raw) ? raw : [raw];
}

function exportedWorkflow(workflowId) {
  const out = tmpPath(`export-${workflowId}.json`);
  try {
    const result = runN8nCli(
      ["export:workflow", `--id=${workflowId}`, `--output=${out}`],
      { capture: true },
    );
    if (result.status !== 0) {
      return null;
    }
    const row = readExportedRows(out).find((entry) => entry.id === workflowId);
    return row ?? null;
  } catch {
    return null;
  } finally {
    rmSync(out, { force: true });
  }
}

function reviewedWorkflowsInstalled() {
  return exportedWorkflow(workflowIds.checklist) !== null;
}

async function postWebhook(pathName, body, { tries = 30 } = {}) {
  const cfg = config();
  const url = `http://127.0.0.1:${cfg.n8nPort}/webhook/${pathName}`;
  let last = null;
  for (let attempt = 0; attempt < tries; attempt += 1) {
    last = await fetchStatus(
      url,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
      },
      10_000,
    );
    if (last !== null && last.ok) {
      return last;
    }
    await sleep(1_000);
  }
  const detail = last === null ? "no response" : `${last.status} ${last.body}`;
  throw new Error(`POST /webhook/${pathName} failed (${detail}).`);
}

function validateWorkflowFiles() {
  const result = spawnSync(
    process.execPath,
    [join(projectRoot, "scripts", "validate-workflows.mjs")],
    { stdio: "inherit" },
  );
  if (result.status !== 0) {
    throw new Error("The committed workflow files failed validation.");
  }
}

async function compileSkillBundle() {
  const { compileSkills } = await import(
    new URL("./compile-skills.mjs", import.meta.url)
  );
  return JSON.stringify(await compileSkills());
}

// n8n's Overview page is always a flat list of every workflow, so the skill
// folders only show up inside the local owner's Personal project. Grouping the
// workflows is what makes that page worth opening; skillsUrl is how a learner
// finds it.
// Returns false when grouping was skipped for a good reason, most often an n8n
// with no folder licence. Only a real failure throws.
function applyWorkflowFolders(extraArgs = []) {
  const result = spawnSync(
    process.execPath,
    [
      "--no-warnings",
      join(projectRoot, "scripts", "apply-workflow-folders.mjs"),
      `--database=${join(paths.n8nDataDir, "database.sqlite")}`,
      ...extraArgs,
    ],
    { stdio: "inherit" },
  );
  if (result.status === 3) {
    return false;
  }
  if (result.status !== 0) {
    throw new Error("Grouping the workflows into skill folders failed.");
  }
  return true;
}

function personalProjectId() {
  const databasePath = join(paths.n8nDataDir, "database.sqlite");
  if (!existsSync(databasePath)) {
    return null;
  }
  const script = [
    "const { DatabaseSync } = require('node:sqlite');",
    "const database = new DatabaseSync(process.argv[1], { readOnly: true });",
    "const row = database.prepare(\"SELECT id FROM project WHERE type = 'personal' ORDER BY createdAt ASC LIMIT 1\").get();",
    "database.close();",
    "if (row) process.stdout.write(row.id);",
  ].join(" ");
  const result = spawnSync(process.execPath, ["-e", script, databasePath], {
    encoding: "utf8",
    env: process.env,
  });
  const id = result.status === 0 ? result.stdout.trim() : "";
  return /^[A-Za-z0-9_-]+$/.test(id) ? id : null;
}

function skillsUrl(cfg) {
  const projectId = personalProjectId();
  const base = `http://localhost:${cfg.n8nPort}`;
  return projectId ? `${base}/projects/${projectId}/workflows` : null;
}

async function importReviewedWorkflows() {
  validateWorkflowFiles();

  if (!serviceIsRunning(services.n8n)) {
    print("\nStarting n8n...");
    startService("n8n");
    await waitForService("n8n");
  }

  print("\nImporting the reviewed workflows as inactive drafts...");
  n8nCliOrThrow(
    ["import:workflow", "--separate", `--input=${paths.workflowsDir}`],
    "Workflow import",
  );

  print("\nPreparing local data, enabled skills, and reviewed tool dependencies...");
  const published = [];
  let groupedIntoFolders = false;
  try {
    for (const id of [workflowIds.taskSetup, workflowIds.skillSync]) {
      n8nCliOrThrow(["publish:workflow", `--id=${id}`], `Publishing ${id}`);
      published.push(id);
    }
    for (const id of workflowIds.tools) {
      n8nCliOrThrow(["publish:workflow", `--id=${id}`], `Publishing ${id}`);
    }

    await restartN8n();

    const setupResponse = await postWebhook("setup-task-data", "{}");
    if (!setupResponse.body.includes('"ok":true')) {
      throw new Error(
        `Local task setup returned an unexpected response: ${setupResponse.body}`,
      );
    }

    const bundle = await compileSkillBundle();
    const skillResponse = await postWebhook("sync-enabled-skills", bundle);
    if (!skillResponse.body.includes('"ok":true')) {
      throw new Error(
        `Enabled skill sync returned an unexpected response: ${skillResponse.body}`,
      );
    }

    print("\nGrouping the workflows into skill folders...");
    groupedIntoFolders = applyWorkflowFolders();
  } finally {
    for (const id of published) {
      runN8nCli(["unpublish:workflow", `--id=${id}`], { capture: true });
    }
    await restartN8n();
  }

  print("\nWorkflows imported successfully.");
  print("Local task tables and three sample tasks are ready.");
  print("Enabled Markdown skills are synced into the agent.");
  if (groupedIntoFolders) {
    print("The workflows are grouped into five skill folders.");
  }
  const cfg = config();
  const skills = skillsUrl(cfg);
  print(
    `Open ${skills ?? `http://localhost:${cfg.n8nPort}`} and follow docs/N8N_AGENT_SETUP.md.`,
  );
  print(
    "The main agent stays inactive until you select your Anthropic credential and publish it.",
  );
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function commandPreflight() {
  let failures = 0;
  const ok = (message) => print(`  [ok] ${message}`);
  const failure = (message) => {
    printError(`  [!!] ${message}`);
    failures += 1;
  };
  const note = (message) => print(`       ${message}`);

  print("AI Solopreneur local preflight\n");

  if (nodeMajor() >= REQUIRED_NODE_MAJOR) {
    ok(`Node.js ${process.versions.node} is available.`);
    if (nodeMajor() > REQUIRED_NODE_MAJOR) {
      note(
        `This project is tested with Node.js ${REQUIRED_NODE_MAJOR} (LTS); newer versions usually work.`,
      );
    }
  } else {
    failure(
      `Node.js ${REQUIRED_NODE_MAJOR} (LTS) or newer is required; found ${process.versions.node}.`,
    );
    note("Run the supplied setup helper to download the verified project-local runtime.");
  }

  const npmCheck = spawnSync("npm", ["--version"], {
    shell: isWindows,
    stdio: "ignore",
  });
  if (npmCheck.error || npmCheck.status !== 0) {
    failure("npm is not available. It is installed together with Node.js.");
  } else {
    ok("npm is available.");
  }

  const cfg = config();
  for (const [port, name] of [
    [cfg.chatPort, "chat"],
    [cfg.n8nPort, "n8n"],
    [cfg.documentWorkerPort, "documentWorker"],
  ]) {
    if (!validPort(port)) {
      failure(
        `${
          name === "chat"
            ? "CHAT_PORT"
            : name === "n8n"
              ? "N8N_PORT"
              : "DOCUMENT_WORKER_PORT"
        } must be a number between 1 and 65535.`,
      );
      continue;
    }
    if (serviceIsRunning(services[name])) {
      ok(`Port ${port} is owned by the running ${services[name].label} service.`);
    } else if (await portInUse(port)) {
      failure(`Port ${port} is already in use by another application.`);
      note("Close that application or change the matching value in .env.");
    } else {
      ok(`Port ${port} is available.`);
    }
  }

  print("");
  if (failures > 0) {
    printError(`Preflight failed with ${failures} problem(s).`);
    return 1;
  }
  print("Preflight passed. This computer is ready for the local agent.");
  return 0;
}

async function commandSetup() {
  print("AI Solopreneur local setup\n");

  const preflightStatus = await commandPreflight();
  if (preflightStatus !== 0) {
    return 1;
  }

  // Stop an existing stack before replacing dependencies or rebuilding the
  // chat so a repeated setup also activates newly pulled project code.
  await stopService("chat");
  await stopService("documentWorker");
  await stopService("n8n");

  ensureDirs();

  if (installedN8nVersion() === pinnedN8nVersion) {
    print(`\nThe pinned local n8n engine (${pinnedN8nVersion}) is already installed.`);
  } else {
    print(`\nDownloading the pinned local n8n engine (${pinnedN8nVersion}) with npm...`);
    print("The first download is large; this can take several minutes.");
    const rootInstallArgs = existsSync(join(projectRoot, "package-lock.json"))
      ? ["ci", "--no-audit", "--no-fund"]
      : ["install", "--no-audit", "--no-fund"];
    runNpm(rootInstallArgs, {
      cwd: projectRoot,
      label: "Installing the local n8n engine",
    });
  }

  print("\nInstalling the local document reader...");
  runNpm(["ci", "--no-audit", "--no-fund", "--ignore-scripts"], {
    cwd: paths.documentWorkerDir,
    label: "Installing the local document reader",
  });

  print("\nBuilding the local chat app...");
  runNpm(["ci", "--no-audit", "--no-fund", "--ignore-scripts"], {
    cwd: paths.chatDir,
    label: "Installing the chat build tools",
  });
  runNpm(["run", "build"], {
    cwd: paths.chatDir,
    label: "Building the chat app",
  });

  print("\nChecking the workflow exports...");
  validateWorkflowFiles();

  print("\nStarting AI Solopreneur...");
  startService("n8n");
  await waitForService("n8n");
  startService("documentWorker");
  await waitForService("documentWorker");

  if (reviewedWorkflowsInstalled()) {
    print("\nThe reviewed workflows are already installed; keeping local edits unchanged.");
  } else {
    print("\nInstalling the reviewed workflows, sample data, and enabled skills...");
    await importReviewedWorkflows();
  }

  startService("chat");
  await waitForService("chat");

  const cfg = config();
  const skills = skillsUrl(cfg);
  print("\nLocal stack is healthy.");
  print(`  Chat app:          http://localhost:${cfg.chatPort}`);
  print(`  n8n editor:        http://localhost:${cfg.n8nPort}`);
  if (skills) {
    print(`  Your agent's skills: ${skills}`);
  }
  print("  Next: create the local n8n owner, then open 01 - START HERE - Learner Checklist.");
  return 0;
}

async function commandStart() {
  requireLocalInstall();
  ensureDocumentWorkerInstalled();
  ensureChatBuilt();

  await startStack();

  const cfg = config();
  const skills = skillsUrl(cfg);
  print("AI Solopreneur is healthy.");
  print(`  Chat app:          http://localhost:${cfg.chatPort}`);
  print(`  n8n editor:        http://localhost:${cfg.n8nPort}`);
  if (skills) {
    print(`  Your agent's skills: ${skills}`);
  }
  return 0;
}

async function commandStop() {
  const stoppedChat = await stopService("chat");
  const stoppedDocumentWorker = await stopService("documentWorker");
  const stoppedN8n = await stopService("n8n");
  if (stoppedChat || stoppedDocumentWorker || stoppedN8n) {
    print("AI Solopreneur is stopped. Local data is preserved.");
  } else {
    print("AI Solopreneur is not running. Local data is preserved.");
  }
  return 0;
}

async function commandRestart() {
  await commandStop();
  return commandStart();
}

async function commandStatus() {
  const cfg = config();
  print("AI Solopreneur local status\n");
  for (const name of ["n8n", "documentWorker", "chat"]) {
    const service = services[name];
    const record = readPidRecord(service);
    const running = record !== null && pidIsRunning(record.pid);
    const health = running
      ? await fetchStatus(service.healthUrl(cfg), {}, 3_000)
      : null;
    const healthText =
      health !== null && health.ok ? "healthy" : running ? "starting or unhealthy" : "stopped";
    print(
      `  ${service.label.padEnd(15)} ${healthText.padEnd(24)} ` +
        `http://localhost:${service.port(cfg)}  ` +
        (running ? `(pid ${record.pid})` : ""),
    );
  }
  print(`\n  Data folder: ${paths.n8nDataDir}`);
  print(`  Logs:        ${paths.logsDir}`);
  return 0;
}

function commandLogs(target = "n8n", lineCount = "100") {
  if (target === "documents") {
    target = "documentWorker";
  }
  const service = services[target];
  if (!service) {
    printError(
      'Usage: node scripts/local.mjs logs [n8n|chat|documents] [lines]',
    );
    return 1;
  }
  print(tailOfFile(service.logFile(), Number(lineCount) || 100));
  return 0;
}

async function commandImportWorkflows() {
  requireLocalInstall();
  await importReviewedWorkflows();
  return 0;
}

async function commandGroupWorkflows(args = []) {
  requireLocalInstall();
  const grouped = applyWorkflowFolders(
    args.includes("--undo") ? ["--undo"] : [],
  );
  const cfg = config();
  const skills = skillsUrl(cfg);
  if (grouped && skills) {
    print(`Open ${skills} to see your agent's skills.`);
  } else if (skills) {
    print(`Your workflows are at ${skills}.`);
  }
  print("Refresh n8n if it is already open in a browser tab.");
  return 0;
}

async function commandSyncSkills() {
  requireLocalInstall();

  if (!serviceIsRunning(services.n8n)) {
    printError("n8n is not running. Start the local stack first.");
    return 1;
  }

  print("Validating and compiling enabled skills...");
  const bundle = await compileSkillBundle();

  print("Opening the temporary localhost skill-sync endpoint...");
  let publishedSync = false;
  try {
    n8nCliOrThrow(
      ["publish:workflow", `--id=${workflowIds.skillSync}`],
      "Publishing the skill-sync workflow",
    );
    publishedSync = true;
    await restartN8n();

    const response = await postWebhook("sync-enabled-skills", bundle);
    if (!response.body.includes('"ok":true')) {
      throw new Error(
        `Enabled skill sync returned an unexpected response: ${response.body}`,
      );
    }
  } finally {
    if (publishedSync) {
      runN8nCli(["unpublish:workflow", `--id=${workflowIds.skillSync}`], {
        capture: true,
      });
      await restartN8n();
    }
  }

  const cfg = config();
  print("Enabled skills synced successfully.");
  print(`Open http://localhost:${cfg.chatPort} and start a new browser conversation.`);
  return 0;
}

async function commandExportWorkflows() {
  requireLocalInstall();
  if (!serviceIsRunning(services.n8n)) {
    printError("n8n is not running. Start the local stack first.");
    return 1;
  }

  const exportDirectory = join(projectRoot, "n8n", "exports", timestamp());
  await mkdir(exportDirectory, { recursive: true });

  for (const [workflowId, outputName] of exportedWorkflowFiles) {
    const temp = tmpPath(`${workflowId}-export.json`);
    n8nCliOrThrow(
      ["export:workflow", `--id=${workflowId}`, "--pretty", `--output=${temp}`],
      `Exporting ${workflowId}`,
    );
    await copyFile(temp, join(exportDirectory, outputName));
    await rm(temp, { force: true });
  }

  const result = spawnSync(
    process.execPath,
    [
      join(projectRoot, "scripts", "normalise-workflow-exports.mjs"),
      exportDirectory,
      paths.workflowsDir,
    ],
    { stdio: "inherit" },
  );
  if (result.status !== 0) {
    throw new Error("Normalising the exported workflows failed.");
  }

  print("Workflow copies exported to:");
  print(`  ${exportDirectory}`);
  print(
    "This folder is ignored by Git. The copies are normalised for review, but still inspect credential references and every diff before promotion.",
  );
  return 0;
}

function sqliteQuickCheck(databasePath) {
  const script = [
    "const { DatabaseSync } = require('node:sqlite');",
    "const database = new DatabaseSync(process.argv[1], { readOnly: true });",
    "const row = database.prepare('PRAGMA quick_check').get();",
    "const version = database.prepare('PRAGMA user_version').get();",
    "database.close();",
    "if (row.quick_check !== 'ok') process.exit(2);",
    "process.stdout.write(String(version.user_version));",
  ].join(" ");
  const result = spawnSync(process.execPath, ["-e", script, databasePath], {
    encoding: "utf8",
    env: process.env,
  });
  return {
    ok: result.status === 0,
    schemaVersion:
      result.status === 0 && /^\d+$/.test(result.stdout.trim())
        ? Number(result.stdout.trim())
        : null,
  };
}

async function commandBackup() {
  requireLocalInstall();
  if (!existsSync(paths.n8nDataDir)) {
    printError("There is no local n8n data to back up yet. Run setup first.");
    return 1;
  }
  if (!existsSync(paths.chatDatabase)) {
    printError("There is no local chat database to back up yet. Start the local app once, then try again.");
    return 1;
  }

  const backupDir = join(paths.backupsDir, timestamp());
  await mkdir(backupDir, { recursive: true });
  if (!isWindows) {
    await chmod(backupDir, 0o700);
  }

  const wasChatRunning = serviceIsRunning(services.chat);
  const wasN8nRunning = serviceIsRunning(services.n8n);
  if (wasChatRunning) {
    print("Briefly stopping chat for a consistent history backup...");
    await stopService("chat");
  }
  if (wasN8nRunning) {
    print("Briefly stopping n8n for a consistent backup...");
    await stopService("n8n");
  }

  try {
    const archive = join(backupDir, "n8n-data.tar.gz");
    const tar = spawnSync("tar", ["-czf", archive, "-C", paths.n8nDataDir, "."], {
      stdio: "inherit",
    });
    if (tar.error || tar.status !== 0) {
      // tar ships with macOS and Windows 10+; fall back to a plain copy.
      rmSync(archive, { force: true });
      cpSync(paths.n8nDataDir, join(backupDir, "n8n-data"), { recursive: true });
    } else if (!isWindows) {
      await chmod(archive, 0o600);
    }

    if (existsSync(paths.envFile)) {
      await copyFile(paths.envFile, join(backupDir, "env.backup"));
      if (!isWindows) {
        await chmod(join(backupDir, "env.backup"), 0o600);
      }
    }

    cpSync(paths.chatDataDir, join(backupDir, "chat-data"), {
      recursive: true,
    });
    writeFileSync(
      join(backupDir, "backup.json"),
      `${JSON.stringify(
        {
          schemaVersion: 2,
          createdAt: new Date().toISOString(),
          contains: {
            n8n: true,
            chatHistory: true,
            environment: existsSync(paths.envFile),
          },
        },
        null,
        2,
      )}\n`,
      { encoding: "utf8", mode: 0o600 },
    );
  } finally {
    if (wasN8nRunning) {
      startService("n8n");
      await waitForService("n8n");
    }
    if (wasChatRunning) {
      startService("chat");
      await waitForService("chat");
    }
  }

  print("Backup created at:");
  print(`  ${backupDir}`);
  print("It contains plaintext chat transcripts, encrypted credentials, and local settings. Keep it private.");
  return 0;
}

async function commandRestore(args) {
  requireLocalInstall();
  const positional = args.filter((arg) => arg !== "--yes");
  const assumeYes = args.includes("--yes");
  const target = positional[0];
  if (!target) {
    printError("Usage: node scripts/local.mjs restore backups/YYYYMMDD-HHMMSS");
    return 1;
  }
  const backupDir = isAbsolute(target) ? target : resolve(process.cwd(), target);
  const archive = join(backupDir, "n8n-data.tar.gz");
  const plainCopy = join(backupDir, "n8n-data");
  const manifestPath = join(backupDir, "backup.json");
  const chatBackupDir = join(backupDir, "chat-data");
  const chatBackupDatabase = join(chatBackupDir, "chat.sqlite");
  if (!existsSync(archive) && !existsSync(plainCopy)) {
    printError("Backup is incomplete. Expected n8n-data.tar.gz (or an n8n-data folder).");
    return 1;
  }

  const hasManifest = existsSync(manifestPath);
  if (hasManifest) {
    let manifest;
    try {
      manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
    } catch {
      printError("Backup manifest is invalid. No local data was changed.");
      return 1;
    }
    if (
      manifest.schemaVersion !== 2 ||
      manifest.contains?.n8n !== true ||
      manifest.contains?.chatHistory !== true ||
      !existsSync(chatBackupDatabase)
    ) {
      printError("Backup is incomplete. Expected a version 2 manifest and chat-data/chat.sqlite.");
      return 1;
    }
    const chatCheck = sqliteQuickCheck(chatBackupDatabase);
    if (!chatCheck.ok || chatCheck.schemaVersion !== chatDatabaseSchemaVersion) {
      printError("The backed-up chat database failed its integrity or schema check. No local data was changed.");
      return 1;
    }
  }

  print(
    hasManifest
      ? "This replaces current local chats, n8n users, credentials, workflows, and history."
      : "This is an older n8n-only backup. It replaces n8n users, credentials, workflows, and history, but leaves current saved chats unchanged.",
  );
  if (!assumeYes && !(await confirmPhrase("Type RESTORE to continue: ", "RESTORE"))) {
    print("Restore cancelled.");
    return 0;
  }

  const restoreStagingDir = join(paths.tmpDir, `restore-${timestamp()}`);
  const stagedN8nData = join(restoreStagingDir, "n8n-data");
  const stagedChatData = join(restoreStagingDir, "chat-data");
  rmSync(restoreStagingDir, { recursive: true, force: true });
  mkdirSync(stagedN8nData, { recursive: true });

  if (existsSync(archive)) {
    const tar = spawnSync("tar", ["-xzf", archive, "-C", stagedN8nData], {
      stdio: "inherit",
    });
    if (tar.error || tar.status !== 0) {
      rmSync(restoreStagingDir, { recursive: true, force: true });
      throw new Error("Unpacking the backup archive failed. Current local data was not changed.");
    }
  } else {
    rmSync(stagedN8nData, { recursive: true, force: true });
    cpSync(plainCopy, stagedN8nData, { recursive: true });
  }
  if (hasManifest) {
    cpSync(chatBackupDir, stagedChatData, { recursive: true });
  }

  await stopService("chat");
  await stopService("documentWorker");
  await stopService("n8n");

  rmSync(paths.n8nDataDir, { recursive: true, force: true });
  mkdirSync(paths.n8nUserFolder, { recursive: true });
  renameSync(stagedN8nData, paths.n8nDataDir);

  if (hasManifest) {
    rmSync(paths.chatDataDir, { recursive: true, force: true });
    mkdirSync(dirname(paths.chatDataDir), { recursive: true });
    renameSync(stagedChatData, paths.chatDataDir);
  }
  rmSync(restoreStagingDir, { recursive: true, force: true });

  const envBackup = join(backupDir, "env.backup");
  if (existsSync(envBackup)) {
    await copyFile(envBackup, paths.envFile);
    if (!isWindows) {
      await chmod(paths.envFile, 0o600);
    }
  }

  await startStack();
  print(
    hasManifest
      ? "Backup restored, including saved chats, and the local stack is healthy."
      : "Older n8n backup restored. Current saved chats were preserved and the local stack is healthy.",
  );
  return 0;
}

async function commandReset(args) {
  const assumeYes = args.includes("--yes");
  if (
    !existsSync(paths.n8nDataDir) &&
    !existsSync(paths.chatDataDir) &&
    !existsSync(paths.documentDataDir) &&
    !serviceIsRunning(services.n8n)
  ) {
    print("Nothing to reset because local setup has not created data yet.");
    return 0;
  }

  if (!assumeYes) {
    print(
      "This permanently removes saved chat transcripts, search data, local n8n users, credentials, workflows, execution history, and extracted document context.",
    );
    print("Create a backup first if any of that data matters.");
    if (!(await confirmPhrase("Type RESET to continue: ", "RESET"))) {
      print("Reset cancelled.");
      return 0;
    }
  }

  await stopService("chat");
  await stopService("documentWorker");
  await stopService("n8n");
  rmSync(paths.n8nUserFolder, { recursive: true, force: true });
  rmSync(paths.chatDataDir, { recursive: true, force: true });
  rmSync(paths.documentDataDir, { recursive: true, force: true });
  rmSync(paths.tmpDir, { recursive: true, force: true });

  print(
    "Saved chats, local n8n data, and extracted document data have been removed. The private .env file was preserved.",
  );
  print("Run ./start.command to create a fresh local instance.");
  return 0;
}

async function commandDiagnose() {
  let failures = 0;
  let actions = 0;
  const ok = (message) => print(`  [ok]   ${message}`);
  const action = (message) => {
    print(`  [next] ${message}`);
    actions += 1;
  };
  const failure = (message) => {
    printError(`  [!!]   ${message}`);
    failures += 1;
  };

  print("AI Solopreneur diagnostics");
  print("This check never calls Claude or DataForSEO and never displays credential values.\n");

  ok(`Node.js ${process.versions.node} is available.`);

  if (existsSync(paths.n8nBin)) {
    const version = installedN8nVersion();
    if (version === pinnedN8nVersion) {
      ok(`The pinned local n8n engine (${pinnedN8nVersion}) is installed.`);
    } else {
      ok(`A local n8n engine (${version}) is installed.`);
    }
  } else {
    failure(
      "Local setup has not run. Double-click setup.command (macOS) or setup-windows.cmd (Windows) first.",
    );
  }

  const cfg = config();
  const n8nRunning = serviceIsRunning(services.n8n);
  if (n8nRunning) {
    ok("The n8n service is running.");
  } else {
    failure("n8n is not running. Double-click start.command or start-windows.cmd, then rerun diagnostics.");
  }
  if (serviceIsRunning(services.chat)) {
    ok("The chat service is running.");
  } else {
    failure("The chat service is not running. Double-click start.command or start-windows.cmd, then rerun diagnostics.");
  }
  if (serviceIsRunning(services.documentWorker)) {
    ok("The document reader is running.");
  } else {
    failure(
      "The document reader is not running. Double-click start.command or start-windows.cmd, then rerun diagnostics.",
    );
  }

  const n8nHealth = await fetchStatus(`http://127.0.0.1:${cfg.n8nPort}/healthz`);
  if (n8nHealth !== null && n8nHealth.ok) {
    ok("n8n health endpoint responds.");
  } else {
    failure(`n8n is not healthy at localhost:${cfg.n8nPort}.`);
  }

  const chatHealth = await fetchStatus(`http://127.0.0.1:${cfg.chatPort}/health`);
  if (chatHealth !== null && chatHealth.ok) {
    ok("Chat health endpoint responds.");
  } else {
    failure(`The chat is not healthy at localhost:${cfg.chatPort}.`);
  }
  if (existsSync(paths.chatDatabase)) {
    const chatDatabaseCheck = sqliteQuickCheck(paths.chatDatabase);
    if (
      chatDatabaseCheck.ok &&
      chatDatabaseCheck.schemaVersion === chatDatabaseSchemaVersion
    ) {
      ok(
        `The local chat database and search index are ready (schema ${chatDatabaseSchemaVersion}).`,
      );
    } else {
      failure(
        "The local chat database failed its integrity or schema check. Create a private backup before troubleshooting it.",
      );
    }
  } else {
    failure("The local chat database is missing. Restart the local stack to create it.");
  }
  const documentHealth = await fetchStatus(
    `http://127.0.0.1:${cfg.documentWorkerPort}/health`,
  );
  if (documentHealth !== null && documentHealth.ok) {
    ok("Document reader health endpoint responds.");
  } else {
    failure("The internal document reader is not healthy.");
  }

  if (n8nRunning && n8nHealth !== null && n8nHealth.ok && existsSync(paths.n8nBin)) {
    if (exportedWorkflow(workflowIds.checklist) !== null) {
      ok("The learner checklist is installed.");
    } else {
      action("Install the reviewed workflows by double-clicking import-workflows.command or import-workflows-windows.cmd.");
    }

    const mainWorkflow = exportedWorkflow(workflowIds.main);
    if (mainWorkflow !== null) {
      ok("The Project Partner workflow is installed.");
    } else {
      action("Install the Project Partner workflow with import-workflows.command or import-workflows-windows.cmd.");
    }

    if (mainWorkflow !== null) {
      if (mainWorkflow.active === true) {
        ok("The Project Partner workflow is published.");
      } else {
        action("Open 00 - START HERE - Project Partner in n8n, select the Claude credential, and publish it.");
      }

      const credentialExport = tmpPath("diagnostic-credentials.json");
      let credentialSelected = false;
      try {
        const result = runN8nCli(
          ["export:credentials", "--all", `--output=${credentialExport}`],
          { capture: true },
        );
        if (result.status === 0) {
          const articleWorkflow = exportedWorkflow("phase13WriteSeoArticle");
          const references = [
            mainWorkflow.nodes?.find((node) => node.name === "Claude - Sonnet 4.6")
              ?.credentials?.anthropicApi,
            articleWorkflow?.nodes?.find((node) => node.name === "Draft With Claude")
              ?.credentials?.anthropicApi,
            articleWorkflow?.nodes?.find((node) => node.name === "Repair With Claude")
              ?.credentials?.anthropicApi,
          ].filter(Boolean);
          const credentials = readExportedRows(credentialExport);
          credentialSelected = references.length === 3 && references.every(
            (reference) =>
              reference?.id &&
              credentials.some(
                (credential) =>
                  credential.id === reference.id &&
                  credential.type === "anthropicApi",
              ),
          );
        }
      } catch {
        credentialSelected = false;
      } finally {
        rmSync(credentialExport, { force: true });
      }
      if (credentialSelected) {
        ok("An Anthropic credential is selected by the agent and article writer.");
      } else {
        action("Create an Anthropic credential named Anthropic account and select it in the agent plus both Claude nodes in workflow 57.");
      }

      const paidWorkflow = exportedWorkflow("phase11StartPaidDomainResearch");
      const dataForSeoCredentialExport = tmpPath("diagnostic-dataforseo-credentials.json");
      let dataForSeoCredentialSelected = false;
      try {
        const result = runN8nCli(
          ["export:credentials", "--all", `--output=${dataForSeoCredentialExport}`],
          { capture: true },
        );
        if (result.status === 0 && paidWorkflow !== null) {
          const reference = paidWorkflow.nodes?.find(
            (node) => node.name === "DataForSEO Ranked Keywords",
          )?.credentials?.httpBasicAuth;
          const credentials = readExportedRows(dataForSeoCredentialExport);
          dataForSeoCredentialSelected = Boolean(
            reference?.id &&
              credentials.some(
                (credential) =>
                  credential.id === reference.id &&
                  credential.type === "httpBasicAuth",
              ),
          );
        }
      } catch {
        dataForSeoCredentialSelected = false;
      } finally {
        rmSync(dataForSeoCredentialExport, { force: true });
      }
      if (dataForSeoCredentialSelected) {
        ok("A DataForSEO Basic Auth credential is selected by the paid research workflow.");
      } else {
        action("Create an HTTP Basic Auth credential named DataForSEO API with your API login and API password, then select it on every DataForSEO node in workflow 53.");
      }
    }

    // The earlier CLI spawns block long enough for n8n to close the pooled
    // keep-alive socket, so a first attempt can fail on the stale connection.
    // A second attempt opens a fresh socket.
    let agentHealth = await fetchStatus(
      `http://127.0.0.1:${cfg.n8nPort}/webhook/agent-health`,
    );
    if (agentHealth === null || !agentHealth.ok) {
      agentHealth = await fetchStatus(
        `http://127.0.0.1:${cfg.n8nPort}/webhook/agent-health`,
      );
    }
    if (agentHealth !== null && agentHealth.ok) {
      ok("The optional agent-health workflow is published.");
    } else {
      action("Publish 90 - DEBUG - Agent Health for the safe local health check.");
    }
  }

  print("");
  if (failures > 0) {
    printError(
      `Diagnostics found ${failures} local service problem(s) and ${actions} setup action(s).`,
    );
    printError("Start with the [!!] lines, then run this helper again.");
    return 1;
  }
  if (actions > 0) {
    print(
      `The local services are healthy. Complete ${actions} [next] action(s), then run diagnostics again.`,
    );
    return 1;
  }
  print("All checks are green. The local agent is ready for a real Claude message.");
  return 0;
}

function commandN8nPassthrough(args) {
  requireLocalInstall();
  const cfg = config();
  const result = spawnSync(process.execPath, [paths.n8nBin, ...args], {
    env: { ...process.env, ...n8nEnv(cfg) },
    stdio: "inherit",
  });
  return result.status ?? 1;
}

function commandHelp() {
  print(`AI Solopreneur local runner

Usage: node scripts/local.mjs <command>

Everyday commands (also available as double-click files in the project folder):
  setup              Install the pinned n8n engine, build the chat app, start
                     everything, and import the reviewed workflows once.
  start              Start n8n, the document reader, and chat in the background.
  stop               Stop all local services. Local data is preserved.
  restart            Stop, then start.
  status             Show whether each service is running and healthy.
  diagnose           Friendly readiness checks. Never calls Claude.

Maintenance commands:
  import-workflows   Re-import the reviewed workflows, sample data, and skills.
  sync-skills        Validate and load the enabled Markdown skills.
  group-workflows [--undo]
                     File the workflows into their skill folders in n8n, or put
                     them all back at the top level. Needs an n8n folder licence.
  export-workflows   Export normalised workflow copies for Git review.
  backup             Save a private copy of chats, n8n data, and settings.
  restore <folder>   Restore chats and n8n data from a saved backup.
  reset [--yes]      Permanently remove chats, local n8n, and document data.
  preflight          Check Node.js, npm, and the three local ports.
  logs [n8n|chat|documents]
                     Show the last lines of a service log.
  n8n <args...>      Run the pinned n8n CLI with this project's settings.`);
  return 0;
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

async function main() {
  assertNodeVersion();
  const [, , command, ...rest] = process.argv;

  switch (command) {
    case "preflight":
      return commandPreflight();
    case "setup":
      return commandSetup();
    case "start":
      return commandStart();
    case "stop":
      return commandStop();
    case "restart":
      return commandRestart();
    case "status":
      return commandStatus();
    case "logs":
      return commandLogs(rest[0], rest[1]);
    case "import-workflows":
      return commandImportWorkflows();
    case "sync-skills":
      return commandSyncSkills();
    case "group-workflows":
      return commandGroupWorkflows(rest);
    case "export-workflows":
      return commandExportWorkflows();
    case "backup":
      return commandBackup();
    case "restore":
      return commandRestore(rest);
    case "reset":
      return commandReset(rest);
    case "diagnose":
      return commandDiagnose();
    case "n8n":
      return commandN8nPassthrough(rest);
    case "help":
    case "--help":
    case undefined:
      return commandHelp();
    default:
      printError(`Unknown command: ${command}\n`);
      commandHelp();
      return 1;
  }
}

try {
  const status = await main();
  process.exit(typeof status === "number" ? status : 0);
} catch (error) {
  printError(`\n${error.message}`);
  process.exit(1);
}
