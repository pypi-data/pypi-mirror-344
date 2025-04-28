# GXB MCP时间服务器

这是一个实现MCP协议的时间服务器，提供获取当前时间和格式化日期等功能。
通过MCP协议，大语言模型可以使用这个服务器来获取实时时间信息。

## 安装

```bash
pip install mcp-server-gxb
```

## 功能

### 工具

- `get_current_time`: 获取当前时间
- `format_date`: 按照指定格式格式化日期

### 资源

- `time://current`: 获取当前时间资源
- `time://zone/{timezone}`: 获取指定时区的时间资源

## 在阿里云百炼中使用

在阿里云百炼平台中，您可以使用以下配置来部署这个MCP服务器：

```json
{
  "mcpServers": {
    "time-server": {
      "command": "uvx",
      "args": ["mcp-server-gxb"]
    }
  }
}
```

## 本地运行

您也可以在本地运行这个MCP服务器：

```bash
# 直接运行
mcp-server-gxb

# 或者使用Python模块
python -m mcp_server_gxb
```

## 许可证

MIT 