# Curriculum Authoring

每个模块目录：`curriculum/NN-slug/`

## 必需要素

| 文件 | 作用 |
|------|------|
| `README.md` | 目标、时长、实现说明、验收方式 |
| `starter/` | 学员起点（可含 NotImplemented） |
| `tests/` 或 `grade.sh` | 客观门禁；`grade.sh` 优先 |
| `rubric.md` | 主观质量（不阻塞解锁） |
| `hints.md` | `agent-bridge hint` 前 1–2 次展示 |
| `partial.diff`（可选） | hint ≥ 3 时展示的局部提示 |

## 约定

- 模块 id 与文件夹：`00-orient` … 与 `@agent-bridge/core` 的 `MODULES` 一致
- 学员作业默认 Python；`grade.sh` 里设置 `PYTHONPATH=starter`
- 反剧透：正式答案不要放进 `starter/`；可用私有 `reference/`（不进 sync 也行，当前 init 会整目录复制——**不要把 reference 放进模块目录**，或放在仓库 `authors-only/`）

## 改完后

```bash
pnpm -r run build
# 已有 workspace 时重新 sync：再跑一次 init（会保留已有 starter 修改）
agent-bridge init
```

## Coach

更新 `packages/coach-skill/SKILL.md` 后执行 `agent-bridge install-skill`。
