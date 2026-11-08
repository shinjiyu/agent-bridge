#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import {
  MODULES,
  ProgressStore,
  curriculumRoot,
  defaultWorkspacePath,
  homeDir,
  moduleById,
  moduleDirName,
  repoRoot,
} from "@agent-bridge/core";
import { gradeModule } from "@agent-bridge/grader";

function usage(): never {
  console.log(`Agent Bridge CLI

Usage:
  agent-bridge init [--dir <workspace>]
  agent-bridge status
  agent-bridge next
  agent-bridge grade [moduleId|slug]
  agent-bridge hint [moduleId|slug]
  agent-bridge install-skill [--cursor-dir <path>]
  agent-bridge help
`);
  process.exit(1);
}

function copyDir(src: string, dest: string): void {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (entry.name === "__pycache__" || entry.name === ".pytest_cache") continue;
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(from, to);
    else fs.copyFileSync(from, to);
  }
}

function syncCurriculum(workspace: string): void {
  const root = curriculumRoot();
  for (const m of MODULES) {
    const name = moduleDirName(m);
    const src = path.join(root, name);
    if (!fs.existsSync(src)) continue;
    const dest = path.join(workspace, name);
    // Always refresh lessons/tests/rubric; preserve student starter edits if present
    const studentStarter = path.join(dest, "starter");
    const hadStarter = fs.existsSync(studentStarter);
    const tmpStarter = hadStarter ? `${studentStarter}.bak` : null;
    if (tmpStarter) {
      fs.rmSync(tmpStarter, { recursive: true, force: true });
      fs.renameSync(studentStarter, tmpStarter);
    }
    fs.rmSync(dest, { recursive: true, force: true });
    copyDir(src, dest);
    if (tmpStarter && fs.existsSync(tmpStarter)) {
      fs.rmSync(studentStarter, { recursive: true, force: true });
      fs.renameSync(tmpStarter, studentStarter);
    }
  }
}

function installSkill(cursorSkillsDir?: string): string {
  const dest =
    cursorSkillsDir ??
    path.join(homeDir(), "skills", "agent-bridge-coach");
  const src = path.join(repoRoot(), "packages", "coach-skill");
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.rmSync(dest, { recursive: true, force: true });
  copyDir(src, dest);

  // Also try user Cursor skills if present
  const userSkills = path.join(
    process.env.HOME ?? "",
    ".cursor",
    "skills",
    "agent-bridge-coach",
  );
  if (process.env.HOME) {
    try {
      fs.mkdirSync(path.dirname(userSkills), { recursive: true });
      fs.rmSync(userSkills, { recursive: true, force: true });
      copyDir(src, userSkills);
    } catch {
      /* optional */
    }
  }
  return dest;
}

function cmdInit(args: string[]): void {
  let dir = defaultWorkspacePath();
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--dir" && args[i + 1]) {
      dir = path.resolve(args[++i]);
    }
  }
  fs.mkdirSync(dir, { recursive: true });
  syncCurriculum(dir);
  const store = new ProgressStore();
  store.init(dir);
  store.close();
  const skillPath = installSkill();
  console.log(`Workspace: ${dir}`);
  console.log(`Progress:  ~/.agent-bridge/progress.sqlite`);
  console.log(`Coach skill installed: ${skillPath}`);
  console.log(`Also mirrored to ~/.cursor/skills/agent-bridge-coach (if possible)`);
  console.log(`\nNext: open the workspace in Cursor, then run:\n  agent-bridge next\n  # or ask Coach: 「继续下一课」`);
}

function cmdStatus(): void {
  const store = new ProgressStore();
  const snap = store.snapshot();
  store.close();
  if (!snap.workspace) {
    console.log("尚未 init。先运行: agent-bridge init");
    process.exit(1);
  }
  console.log(`Workspace: ${snap.workspace}`);
  console.log(`Current:   ${snap.current ?? "(none)"}`);
  console.log("");
  for (const m of MODULES) {
    const u = snap.unlocked.includes(m.id) ? "unlocked" : "locked";
    const p = snap.passed.includes(m.id) ? "passed" : "—";
    const h = snap.hints[m.id] ? `hints=${snap.hints[m.id]}` : "";
    console.log(`[${m.id}] ${m.titleZh.padEnd(18)} ${u.padEnd(10)} ${p.padEnd(8)} ${h}`);
  }
}

function cmdNext(): void {
  const store = new ProgressStore();
  const snap = store.snapshot();
  const cur = snap.current;
  if (!cur) {
    console.log("没有进行中的模块。全部通过或尚未 init。");
    store.close();
    return;
  }
  const meta = moduleById(cur)!;
  const dir = path.join(snap.workspace, moduleDirName(meta));
  store.close();
  console.log(`当前模块 ${meta.id}: ${meta.title} / ${meta.titleZh}`);
  console.log(`目录: ${dir}`);
  console.log(`预计: ~${meta.hours}h`);
  console.log(`\n阅读: ${path.join(dir, "README.md")}`);
  console.log(`实现: ${path.join(dir, "starter")}`);
  console.log(`验收: agent-bridge grade ${meta.id}`);
}

function resolveModuleArg(arg: string | undefined, store: ProgressStore): string {
  if (!arg) {
    const cur = store.currentModule();
    if (!cur) throw new Error("没有可评分的当前模块");
    return cur;
  }
  const meta = moduleById(arg);
  if (!meta) throw new Error(`未知模块: ${arg}`);
  return meta.id;
}

function cmdGrade(args: string[]): void {
  const store = new ProgressStore();
  const workspace = store.workspace();
  if (!workspace) {
    console.log("尚未 init。先运行: agent-bridge init");
    store.close();
    process.exit(1);
  }
  let moduleId: string;
  try {
    moduleId = resolveModuleArg(args[0], store);
  } catch (e) {
    console.error(String(e));
    store.close();
    process.exit(1);
  }
  if (!store.isUnlocked(moduleId)) {
    console.error(`模块 ${moduleId} 尚未解锁`);
    store.close();
    process.exit(1);
  }
  const result = gradeModule(moduleId, workspace);
  store.recordGrade(moduleId, result.passed, result.output.slice(0, 8000));
  const snap = store.snapshot();
  store.close();
  console.log(result.summary);
  if (result.output) {
    console.log("\n--- grader output ---\n");
    console.log(result.output);
  }
  if (result.passed) {
    const meta = moduleById(moduleId)!;
    if (meta.unlocks) {
      console.log(`\n已解锁模块 ${meta.unlocks}。运行: agent-bridge next`);
    } else {
      console.log("\n恭喜，这是最后一课轨模块。");
    }
  } else {
    console.log("\n未通过。可向 Coach 请求提示（会记 hint），或再改再 grade。");
  }
  void snap;
}

function cmdHint(args: string[]): void {
  const store = new ProgressStore();
  let moduleId: string;
  try {
    moduleId = resolveModuleArg(args[0], store);
  } catch (e) {
    console.error(String(e));
    store.close();
    process.exit(1);
  }
  const n = store.bumpHint(moduleId);
  const workspace = store.workspace();
  store.close();
  const meta = moduleById(moduleId)!;
  const hintsPath = workspace
    ? path.join(workspace, moduleDirName(meta), "hints.md")
    : "";
  console.log(`Hint count for module ${moduleId}: ${n}`);
  if (n <= 2 && hintsPath && fs.existsSync(hintsPath)) {
    console.log("\n" + fs.readFileSync(hintsPath, "utf8"));
  } else if (n <= 2) {
    console.log("暂无 hints.md。请阅读 README 验收标准，向 Coach 描述卡点（不要要求贴完整答案）。");
  } else {
    const partial = workspace
      ? path.join(workspace, moduleDirName(meta), "partial.diff")
      : "";
    if (partial && fs.existsSync(partial)) {
      console.log("\n已超过 2 次提示，放出 partial.diff（仍非完整答案）：\n");
      console.log(fs.readFileSync(partial, "utf8"));
    } else {
      console.log("提示次数较多。请缩小问题范围，或对照 tests/ 里的行为断言逐步实现。");
    }
  }
}

function cmdInstallSkill(args: string[]): void {
  let dir: string | undefined;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--cursor-dir" && args[i + 1]) dir = path.resolve(args[++i]);
  }
  const dest = installSkill(dir);
  console.log(`Installed Coach skill → ${dest}`);
}

function main(): void {
  const [, , cmd, ...rest] = process.argv;
  switch (cmd) {
    case "init":
      cmdInit(rest);
      break;
    case "status":
      cmdStatus();
      break;
    case "next":
      cmdNext();
      break;
    case "grade":
      cmdGrade(rest);
      break;
    case "hint":
      cmdHint(rest);
      break;
    case "install-skill":
      cmdInstallSkill(rest);
      break;
    case "help":
    case undefined:
      usage();
      break;
    default:
      console.error(`Unknown command: ${cmd}`);
      usage();
  }
}

main();
