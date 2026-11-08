import fs from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { MODULES, type ModuleId } from "./modules.js";
import { homeDir, progressDbPath } from "./paths.js";

export interface GradeRow {
  moduleId: string;
  passed: number;
  score: number | null;
  detail: string;
  createdAt: string;
}

export interface ProgressSnapshot {
  workspace: string;
  unlocked: string[];
  passed: string[];
  current: string | null;
  hints: Record<string, number>;
  grades: GradeRow[];
}

export class ProgressStore {
  private db: DatabaseSync;

  constructor(dbPath = progressDbPath()) {
    fs.mkdirSync(homeDir(), { recursive: true });
    this.db = new DatabaseSync(dbPath);
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS unlocked (
        module_id TEXT PRIMARY KEY
      );
      CREATE TABLE IF NOT EXISTS passed (
        module_id TEXT PRIMARY KEY,
        passed_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_id TEXT NOT NULL,
        passed INTEGER NOT NULL,
        score REAL,
        detail TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS hints (
        module_id TEXT PRIMARY KEY,
        count INTEGER NOT NULL DEFAULT 0
      );
    `);
  }

  getMeta(key: string): string | null {
    const row = this.db.prepare("SELECT value FROM meta WHERE key = ?").get(key) as
      | { value: string }
      | undefined;
    return row?.value ?? null;
  }

  setMeta(key: string, value: string): void {
    this.db.prepare(
      "INSERT INTO meta(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
    ).run(key, value);
  }

  init(workspace: string): void {
    this.setMeta("workspace", workspace);
    this.setMeta("initialized_at", new Date().toISOString());
    this.db.prepare("INSERT OR IGNORE INTO unlocked(module_id) VALUES (?)").run("0");
  }

  workspace(): string | null {
    return this.getMeta("workspace");
  }

  isUnlocked(id: string): boolean {
    const row = this.db.prepare("SELECT 1 AS ok FROM unlocked WHERE module_id = ?").get(id);
    return Boolean(row);
  }

  isPassed(id: string): boolean {
    const row = this.db.prepare("SELECT 1 AS ok FROM passed WHERE module_id = ?").get(id);
    return Boolean(row);
  }

  unlock(id: string): void {
    this.db.prepare("INSERT OR IGNORE INTO unlocked(module_id) VALUES (?)").run(id);
  }

  markPassed(id: string): void {
    this.db
      .prepare(
        "INSERT INTO passed(module_id, passed_at) VALUES (?, ?) ON CONFLICT(module_id) DO UPDATE SET passed_at = excluded.passed_at",
      )
      .run(id, new Date().toISOString());
  }

  recordGrade(moduleId: string, passed: boolean, detail: string, score: number | null = null): void {
    this.db
      .prepare(
        "INSERT INTO grades(module_id, passed, score, detail, created_at) VALUES (?, ?, ?, ?, ?)",
      )
      .run(moduleId, passed ? 1 : 0, score, detail, new Date().toISOString());
    if (passed) {
      this.markPassed(moduleId);
      const mod = MODULES.find((m) => m.id === moduleId);
      if (mod?.unlocks) this.unlock(mod.unlocks);
    }
  }

  bumpHint(moduleId: string): number {
    this.db
      .prepare(
        "INSERT INTO hints(module_id, count) VALUES (?, 1) ON CONFLICT(module_id) DO UPDATE SET count = count + 1",
      )
      .run(moduleId);
    const row = this.db.prepare("SELECT count FROM hints WHERE module_id = ?").get(moduleId) as {
      count: number;
    };
    return row.count;
  }

  hintCount(moduleId: string): number {
    const row = this.db.prepare("SELECT count FROM hints WHERE module_id = ?").get(moduleId) as
      | { count: number }
      | undefined;
    return row?.count ?? 0;
  }

  /** First unlocked module that is not yet passed; else last unlocked. */
  currentModule(): ModuleId | null {
    for (const m of MODULES) {
      if (this.isUnlocked(m.id) && !this.isPassed(m.id)) return m.id;
    }
    const unlocked = MODULES.filter((m) => this.isUnlocked(m.id));
    return unlocked.length ? unlocked[unlocked.length - 1].id : null;
  }

  snapshot(): ProgressSnapshot {
    const unlocked = (
      this.db.prepare("SELECT module_id FROM unlocked").all() as { module_id: string }[]
    ).map((r) => r.module_id);
    const passed = (
      this.db.prepare("SELECT module_id FROM passed").all() as { module_id: string }[]
    ).map((r) => r.module_id);
    const hintRows = this.db.prepare("SELECT module_id, count FROM hints").all() as {
      module_id: string;
      count: number;
    }[];
    const hints: Record<string, number> = {};
    for (const h of hintRows) hints[h.module_id] = h.count;
    const grades = this.db
      .prepare(
        "SELECT module_id AS moduleId, passed, score, detail, created_at AS createdAt FROM grades ORDER BY id DESC LIMIT 20",
      )
      .all() as unknown as GradeRow[];
    return {
      workspace: this.workspace() ?? "",
      unlocked,
      passed,
      current: this.currentModule(),
      hints,
      grades,
    };
  }

  close(): void {
    this.db.close();
  }
}
