export type ModuleId =
  | "0"
  | "1"
  | "2"
  | "3"
  | "4"
  | "5"
  | "6"
  | "7"
  | "8"
  | "9";

export interface ModuleMeta {
  id: ModuleId;
  slug: string;
  title: string;
  titleZh: string;
  hours: number;
  unlocks: ModuleId | null;
}

/** Ordered curriculum. Module 0 unlocked after init. Matches OUTLINE.md M0–M9. */
export const MODULES: ModuleMeta[] = [
  {
    id: "0",
    slug: "method",
    title: "Learning method & shell",
    titleZh: "学法与结业壳",
    hours: 1,
    unlocks: "1",
  },
  {
    id: "1",
    slug: "ask",
    title: "Question practice",
    titleZh: "提问练习",
    hours: 1,
    unlocks: "2",
  },
  {
    id: "2",
    slug: "token",
    title: "Tokens & next-token models",
    titleZh: "Token 与逐 token 模型",
    hours: 2,
    unlocks: "3",
  },
  {
    id: "3",
    slug: "tools",
    title: "Tools into the prefix",
    titleZh: "工具入门",
    hours: 2,
    unlocks: "4",
  },
  {
    id: "4",
    slug: "agent-def",
    title: "General agent vs graph",
    titleZh: "通用 Agent 与 Graph",
    hours: 2,
    unlocks: "5",
  },
  {
    id: "5",
    slug: "structures",
    title: "Common agent structures",
    titleZh: "常见 Agent 结构",
    hours: 2,
    unlocks: "6",
  },
  {
    id: "6",
    slug: "harness-map",
    title: "Harness map & scope",
    titleZh: "Harness 地图与范围",
    hours: 2,
    unlocks: "7",
  },
  {
    id: "7",
    slug: "cost-context",
    title: "Cost & context in your system",
    titleZh: "成本与上下文进系统",
    hours: 4,
    unlocks: "8",
  },
  {
    id: "8",
    slug: "land",
    title: "Land your main structure",
    titleZh: "主结构落地",
    hours: 8,
    unlocks: "9",
  },
  {
    id: "9",
    slug: "smoke",
    title: "Contracts, safety & smoke",
    titleZh: "合约、安全与冒烟结业",
    hours: 6,
    unlocks: null,
  },
];

export function moduleById(id: string): ModuleMeta | undefined {
  return MODULES.find((m) => m.id === id || m.slug === id);
}

export function moduleDirName(m: ModuleMeta): string {
  return `${m.id.padStart(2, "0")}-${m.slug}`;
}
