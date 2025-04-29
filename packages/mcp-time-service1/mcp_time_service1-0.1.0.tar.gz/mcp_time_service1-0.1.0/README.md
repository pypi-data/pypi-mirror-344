# MCP时间服务 (v0.1.0)

这是一个基于MCP协议的时间服务器，提供获取当前时间和格式化日期等功能。
大语言模型可以通过这个服务获取实时时间信息。

## 安装

```bash
pip install mcp-time-service1
```

## 功能

### 工具 (Tools)

- `get_current_time`: 获取当前时间，精确到毫秒。
- `format_date(format_string: str)`: 按照指定格式返回当前日期。

### 资源 (Resources)

- `time://timezone_info`: 提供当前系统的时区信息。

## 在阿里云百炼中使用

在阿里云百炼平台的MCP服务配置中，使用以下JSON：

```json
{
  "mcpServers": {
    "time-service": {  // 服务名称，可自定义
      "command": "uvx",
      "args": ["mcp-time-service1"]
    }
  }
}
```

## 本地运行

安装后，您可以在本地通过以下方式运行：

```bash
# 使用uvx
uvx mcp-time-service1

# 使用包提供的命令
mcp-time-service1

# 使用Python -m
python -m mcp_time_service1
```

按 `Ctrl+C` 停止服务器。

## 许可证

MIT License 