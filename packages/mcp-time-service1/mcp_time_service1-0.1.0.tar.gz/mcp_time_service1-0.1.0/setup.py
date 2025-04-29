from setuptools import setup, find_packages
import os

# 读取 README 文件作为长描述
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "MCP时间服务 - 一个简单的提供时间功能的MCP服务器"

setup(
    name="mcp-time-service1",  # PyPI上的包名，必须唯一
    version="0.1.0",         # 版本号
    packages=find_packages(), # 自动查找包目录
    author="MCP时间服务",     # 作者名字
    author_email="your.email@example.com", # 邮箱
    description="一个实现MCP协议的时间服务器示例", # 简短描述
    long_description=long_description,          # 详细描述
    long_description_content_type="text/markdown", # 描述格式
    url="https://github.com/yourusername/mcp-time-service1", # 项目主页URL（可选）
    classifiers=[ # 包的分类信息
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7", # 要求的Python最低版本
    install_requires=[       # 核心依赖项
        "mcp>=1.6.0",        # 依赖MCP SDK
    ],
    entry_points={           # 定义命令行入口点
        "console_scripts": [
            "mcp-time-service1=mcp_time_service1.__main__:main", # 命令名=模块路径:函数名
        ],
    },
) 