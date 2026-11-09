# Curriculum Authoring

每个模块：`curriculum/NN-slug/`，与 `@agent-bridge/core` 的 `MODULES` 一致。

## 必需要素

| 文件 | 作用 |
|------|------|
| `README.md` | 目标、Chat 交互说明、验收 |
| `starter/answers.json` | 空壳；**由 Coach 在 Chat 里按学员回答写入** |
| `tests/test_module.py` + `grade.sh` | 客观门禁 |
| `rubric.md` / `hints.md` | 主观与提示 |

## 交互约定

- README 必须写明：作业在 Chat 完成，不要求学员手改 starter
- 不在课文里罗列「不能做」清单；边界用证据个案
- 结业代码落在 workspace 的 `my-agent/`，不要把完整 reference 放进模块目录

## 改完后

```bash
pnpm -r run build
agent-bridge init            # sync 课程；保留已有 starter
agent-bridge install-skill
```

可用 `scripts/write_curriculum_v2.py` 作为批量生成参考（改模块后以目录内文件为准）。
