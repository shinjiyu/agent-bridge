import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

/** Monorepo root (…/agent-bridge), walking up from this package. */
export function repoRoot(): string {
  let dir = here;
  for (let i = 0; i < 8; i++) {
    if (fs.existsSync(path.join(dir, "pnpm-workspace.yaml"))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  // dist/../.. = packages/core → repo root when built
  return path.resolve(here, "../../..");
}

export function curriculumRoot(): string {
  return path.join(repoRoot(), "curriculum");
}

export function homeDir(): string {
  return path.join(os.homedir(), ".agent-bridge");
}

export function progressDbPath(): string {
  return path.join(homeDir(), "progress.sqlite");
}

export function defaultWorkspacePath(): string {
  return path.join(homeDir(), "workspace");
}
