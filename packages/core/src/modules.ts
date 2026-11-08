export type ModuleId = "0" | "1" | "2" | "3" | "4" | "5" | "6";

export interface ModuleMeta {
  id: ModuleId;
  slug: string;
  title: string;
  titleZh: string;
  hours: number;
  unlocks: ModuleId | null;
}

/** Ordered curriculum. Module 0 is unlocked by default after init. */
export const MODULES: ModuleMeta[] = [
  {
    id: "0",
    slug: "orient",
    title: "How to learn",
    titleZh: "学法：能 / 不能 / 成本",
    hours: 2,
    unlocks: "1",
  },
  {
    id: "1",
    slug: "tool-agent",
    title: "Tool-using Agent",
    titleZh: "工具循环 Agent",
    hours: 8,
    unlocks: "2",
  },
  {
    id: "2",
    slug: "mcp-server",
    title: "Ship an MCP Server",
    titleZh: "交付一个 MCP Server",
    hours: 8,
    unlocks: "3",
  },
  {
    id: "3",
    slug: "rag-agent",
    title: "RAG Agent",
    titleZh: "检索增强 Agent",
    hours: 8,
    unlocks: "4",
  },
  {
    id: "4",
    slug: "eval-obs",
    title: "Eval & Observability",
    titleZh: "评测与可观测性",
    hours: 6,
    unlocks: "5",
  },
  {
    id: "5",
    slug: "guardrails",
    title: "Production Guardrails",
    titleZh: "生产护栏与部署",
    hours: 6,
    unlocks: "6",
  },
  {
    id: "6",
    slug: "capstone",
    title: "Capstone",
    titleZh: "毕业作品集",
    hours: 12,
    unlocks: null,
  },
];

export function moduleById(id: string): ModuleMeta | undefined {
  return MODULES.find((m) => m.id === id || m.slug === id);
}

export function moduleDirName(m: ModuleMeta): string {
  return `${m.id.padStart(2, "0")}-${m.slug}`;
}
