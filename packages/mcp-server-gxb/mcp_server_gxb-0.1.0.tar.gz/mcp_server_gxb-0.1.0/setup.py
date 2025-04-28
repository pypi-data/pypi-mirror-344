from setuptools import setup, find_packages

setup(
    name="mcp-server-gxb",
    version="0.1.0",
    packages=find_packages(),
    author="GXB",
    author_email="example@example.com",
    description="一个实现MCP协议的时间服务器",
    long_description="""
# GXB MCP时间服务器

这是一个实现MCP协议的时间服务器，提供获取当前时间和格式化日期等功能。

## 功能

- 获取当前时间
- 按照指定格式格式化日期
- 提供时间资源服务

## 在阿里云百炼中使用

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
""",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-server-gxb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp>=0.1.0",  # MCP SDK依赖
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-server-gxb=mcp_server_gxb.__main__:main",
        ],
    },
) 