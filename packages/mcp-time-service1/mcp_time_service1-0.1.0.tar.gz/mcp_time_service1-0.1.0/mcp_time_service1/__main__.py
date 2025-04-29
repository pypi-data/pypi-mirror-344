"""MCP时间服务主入口"""

import sys
import traceback
import datetime
try:
    from mcp.server.fastmcp import FastMCP, Context
except ImportError:
    print("错误：需要安装 'mcp' 包才能运行此服务器。", file=sys.stderr)
    print("请运行: pip install mcp", file=sys.stderr)
    sys.exit(1)

# 创建FastMCP服务器实例
mcp = FastMCP("MCP时间服务", instructions="这个服务器提供基本的时间和日期功能。")

# 定义获取当前时间的工具
@mcp.tool()
def get_current_time() -> str:
    """获取当前时间，精确到毫秒"""
    now = datetime.datetime.now()
    print(f"工具 'get_current_time' 被调用", file=sys.stderr)
    return f"当前时间是: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"

# 定义格式化日期的工具
@mcp.tool()
def format_date(format_string: str = "%Y年%m月%d日") -> str:
    """按照指定格式返回当前日期
    
    参数:
        format_string: Python strftime 格式字符串 (例如 "%Y-%m-%d")
    """
    now = datetime.datetime.now()
    print(f"工具 'format_date' 被调用，格式: {format_string}", file=sys.stderr)
    return now.strftime(format_string)

# 定义一个提供时区信息的资源
@mcp.resource("time://timezone_info")
def timezone_info() -> dict:
    """提供当前时区信息"""
    now = datetime.datetime.now()
    tzinfo = now.astimezone().tzinfo
    print(f"资源 'time://timezone_info' 被访问", file=sys.stderr)
    return {
        "name": str(tzinfo),
        "utc_offset": str(now.astimezone().utcoffset()),
        "dst": str(now.astimezone().dst())
    }

# 服务器启动入口
def main():
    """MCP服务器入口函数，供命令行或uvx调用"""
    try:
        print("MCP时间服务正在启动...", file=sys.stderr)
        mcp.run()  # 启动服务器，此函数会阻塞直到服务器停止
        print("MCP时间服务已停止。", file=sys.stderr)
    except Exception as e:
        print(f"启动或运行时发生错误: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

# 允许直接通过 python -m mcp_time_service1 运行
if __name__ == "__main__":
    main() 