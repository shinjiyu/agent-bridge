# Module 2 — Ship an MCP Server

**时长**：约 8 小时  
**目标**：实现一个 **stdio JSON-RPC** 工具服务器（MCP 精简子集），可被测试客户端调用。

## 为什么学这个

Cursor / Claude Code 通过 **MCP** 挂本地工具。你需要理解：工具描述、调用、错误与边界。

本模块不强制安装官方 SDK；实现精简协议即可（字段对齐 MCP 习惯）。

## 协议（JSON Lines / 每行一个 JSON-RPC 2.0 对象）

请求：

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":2}}}
```

`tools/list` 响应 `result.tools`：数组，每项含 `name`, `description`, `inputSchema`（JSON Schema 对象）。

`tools/call` 响应 `result.content`：`[{"type":"text","text":"..."}]`。

未知 method → JSON-RPC error `code: -32601`。  
未知 tool → error `code: -32000` message 含 `unknown tool`。

## 必须提供的工具

| name | 行为 |
|------|------|
| `echo` | arguments.text → 原样返回 |
| `add` | arguments.a + arguments.b → 数字字符串 |

## 实现位置

- `starter/server.py`：`handle_message(obj) -> obj`，以及 `__main__` 读写 stdin/stdout
- 可选：`starter/manifest.json` 列出工具（若存在，测试会核对名称）

## 本地手测

```bash
cd 02-mcp-server
PYTHONPATH=starter python3 -c "from server import handle_message; print(handle_message({'jsonrpc':'2.0','id':1,'method':'tools/list','params':{}}))"
```

## 验收

`agent-bridge grade 2`
