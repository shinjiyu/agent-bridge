import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import {
  curriculumRoot,
  moduleById,
  moduleDirName,
  type ModuleMeta,
} from "@agent-bridge/core";

export interface GradeResult {
  moduleId: string;
  passed: boolean;
  summary: string;
  output: string;
}

function modulePath(meta: ModuleMeta, workspace: string): string {
  const name = moduleDirName(meta);
  const inWorkspace = path.join(workspace, name);
  if (fs.existsSync(inWorkspace)) return inWorkspace;
  return path.join(curriculumRoot(), name);
}

/** Run module-local grade.sh if present, else pytest on tests/. */
export function gradeModule(moduleId: string, workspace: string): GradeResult {
  const meta = moduleById(moduleId);
  if (!meta) {
    return {
      moduleId,
      passed: false,
      summary: `未知模块: ${moduleId}`,
      output: "",
    };
  }
  const dir = modulePath(meta, workspace);
  if (!fs.existsSync(dir)) {
    return {
      moduleId: meta.id,
      passed: false,
      summary: `找不到模块目录: ${dir}`,
      output: "",
    };
  }

  const gradeSh = path.join(dir, "grade.sh");
  let result;
  if (fs.existsSync(gradeSh)) {
    result = spawnSync("bash", [gradeSh], {
      cwd: dir,
      encoding: "utf8",
      env: { ...process.env, AGENT_BRIDGE_WORKSPACE: workspace },
    });
  } else {
    const tests = path.join(dir, "tests");
    if (!fs.existsSync(tests)) {
      return {
        moduleId: meta.id,
        passed: false,
        summary: "模块缺少 grade.sh 与 tests/",
        output: "",
      };
    }
    result = spawnSync(
      "python3",
      ["-m", "pytest", "-q", "--tb=short", "tests"],
      {
        cwd: dir,
        encoding: "utf8",
        env: { ...process.env, PYTHONPATH: path.join(dir, "starter") },
      },
    );
  }

  const output = `${result.stdout ?? ""}${result.stderr ?? ""}`.trim();
  const passed = result.status === 0;
  const summary = passed
    ? `模块 ${meta.id}（${meta.titleZh}）通过`
    : `模块 ${meta.id}（${meta.titleZh}）未通过（exit ${result.status ?? "?"}）`;
  return { moduleId: meta.id, passed, summary, output };
}
