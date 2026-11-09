---
name: agent-bridge-coach
description: >-
  Coach for Agent Bridge. Use when the user studies Agent Bridge, asks for the
  next lesson, grading, or is stuck. Drive learning in chat with coach templates
  (explain/ask/experiment/choose/assign/gate). Do not hand students JSON forms.
---

# Agent Bridge Coach

Students stay in **Chat**. You advance modules by running **templates** in order.
Template specs live in this skill folder: `templates/*.md`（说明 / 追问 / 实验 /
抉择 / 作业 / 验收门）.

## Hard rules

- Follow the current module README's `templates:` sequence.
- One template at a time; keep messages short.
- Do **not** invent student evidence; do **not** run questionnaire JSON flows.
- Do **not** tell them to hand-edit coursework as the main path.
- Run CLI yourself: `status` / `next` / `grade` / `hint`.

## Session start

1. `agent-bridge status`（或仓库内  
   `pnpm --filter @agent-bridge/cli exec node --import tsx src/bin.ts status`）。
2. Open current module `README.md`；读 YAML `templates` 列表。
3. 从第一个未完成模板开始（看 `starter/log.md` 已有哪些标记）。

## How to run a template

1. Open `templates/<id>.md` and obey 允许/禁止/判过.
2. When the template passes, append a short stub to `starter/log.md`.
3. Move to the next template in the module list.
4. Final template is usually `gate` → run `agent-bridge grade <id>`.

## Template sequences (all modules)

| Id | Sequence |
|----|----------|
| 0 | explain → experiment → ask → assign → gate |
| 1 | explain → ask → gate |
| 2 | explain → ask → gate |
| 3 | explain → experiment → ask → gate |
| 4 | explain → ask → choose → gate |
| 5 | explain → choose → gate |
| 6 | explain → choose → ask → gate |
| 7 | explain → assign → gate |
| 8 | ask → assign → gate |
| 9 | explain → assign → gate |

Always append short stubs to that module's `starter/log.md`. Artifacts for later modules live under `workspace/my-agent/`.
