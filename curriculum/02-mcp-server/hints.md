# Hints — Module 2

1. 先写 `handle_message` 的纯函数，再接线 stdin 循环。
2. `tools/list` 固定返回两个 tool 的 schema。
3. `tools/call`：用 dict 分发 `echo` / `add`；注意 a/b 可能是 int 或 float。
