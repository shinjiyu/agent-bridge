# Hints — Module 1

1. 先让三个 tool 函数单独可测，再写 `decide`。
2. `run_agent` 循环：`decide` → 若有 tool 则执行并 append observation → 否则 break。
3. calc：用 `ast.parse` + 只允许 `BinOp/UnaryOp/Constant/Num` 节点，拒绝名称与属性。
