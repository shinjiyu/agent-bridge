# Coach 模板（核心 6 个）

每种模板只干一件事。模块用「模板序列」编排，不要把填表当课。

| Id | 名称 | 一句话 |
|----|------|--------|
| `explain` | 说明型 | 展示短资料让学生读 |
| `ask` | 追问型 | 只问，逼出三问/范围 |
| `experiment` | 实验型 | 当场试一下，口述现象 |
| `choose` | 抉择型 | 给选项，学生选 + 一句理由 |
| `assign` | 作业型 | 做一个小产物，Coach 审核 |
| `gate` | 验收门 | 跑检查，通/断 |

可选加分（未进核心）：`demo` 演示型、`contrast` 对照型、`recap` 收束型。

模块 README 用 YAML 头声明序列，例如：

```yaml
templates:
  - explain
  - experiment
  - ask
  - assign
  - gate
```

Coach 按序执行；未完成当前模板不跳到下一模板（除非学生明确跳过且模板允许）。
