#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const skillName = "obsidian-ai-vault-installer";
const repoRoot = path.resolve(__dirname, "..");
const source = path.join(repoRoot, "skills", skillName);
const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), ".codex");
const installDir = process.env.CODEX_SKILLS_DIR || path.join(codexHome, "skills");
const target = path.join(installDir, skillName);

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const item of fs.readdirSync(src)) {
      copyRecursive(path.join(src, item), path.join(dest, item));
    }
    return;
  }
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

function timestamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return [
    d.getFullYear(),
    pad(d.getMonth() + 1),
    pad(d.getDate()),
    "-",
    pad(d.getHours()),
    pad(d.getMinutes()),
    pad(d.getSeconds()),
  ].join("");
}

function removeRecursive(targetPath) {
  if (!fs.existsSync(targetPath)) return;
  fs.rmSync(targetPath, { recursive: true, force: true });
}

if (!fs.existsSync(source)) {
  console.error(`Cannot find skill source folder: ${source}`);
  process.exit(1);
}

fs.mkdirSync(installDir, { recursive: true });

if (fs.existsSync(target)) {
  console.log(`Updating existing skill at: ${target}`);
  removeRecursive(target);
}

copyRecursive(source, target);

console.log(`Installed skill to: ${target}`);
console.log("Restart Codex / Claude Code to pick up new skills.");
console.log("Use prompt: 帮我搭建知识库");
