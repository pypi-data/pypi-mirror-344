"""MCP服务器主入口点"""

import datetime
from mcp.server.fastmcp import FastMCP

# 创建MCP服务器
mcp = FastMCP("GXB时间服务器")

@mcp.tool()
def get_current_time() -> str:
    """获取当前时间"""
    now = datetime.datetime.now()
    return f"当前时间是: {now.strftime('%Y-%m-%d %H:%M:%S')}"

@mcp.tool()
def format_date(format_string: str = "%Y年%m月%d日") -> str:
    """按照指定格式返回当前日期
    
    参数:
        format_string: 日期格式字符串，例如"%Y年%m月%d日"
    """
    now = datetime.datetime.now()
    return now.strftime(format_string)

@mcp.resource("time://current")
def current_time_resource() -> str:
    """当前时间资源"""
    now = datetime.datetime.now()
    return f"资源访问时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"

@mcp.resource("time://zone/{timezone}")
def timezone_resource(timezone: str) -> str:
    """指定时区的时间资源
    
    参数:
        timezone: 时区名称，例如"Asia/Shanghai"
    """
    try:
        import zoneinfo
        now = datetime.datetime.now(tz=zoneinfo.ZoneInfo(timezone))
        return f"{timezone}的当前时间是: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except ImportError:
        return f"无法获取时区{timezone}的时间，此功能需要Python 3.9+的zoneinfo模块"
    except Exception as e:
        return f"获取{timezone}时区时间失败: {str(e)}"

def main():
    """MCP服务器入口函数"""
    mcp.run()

if __name__ == "__main__":
    main() 