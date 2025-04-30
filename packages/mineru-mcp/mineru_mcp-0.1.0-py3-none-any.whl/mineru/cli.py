"""MinerU PDF转Markdown服务的命令行界面。"""

import os
import sys
import argparse
from pathlib import Path

from . import config
from . import server

def main():
    """命令行界面的入口点。"""
    parser = argparse.ArgumentParser(
        description="MinerU PDF转Markdown转换服务"
    )
    
    parser.add_argument(
        "--output-dir", 
        "-o", 
        type=str,
        help="保存转换后文件的目录 (默认: ./downloads)"
    )

    parser.add_argument(
        "--transport",
        "-t",
        type=str,
        help="协议类型 (默认: stdio,可选: sse)"
    )
    
    args = parser.parse_args()
    
    # 如果提供了输出目录，则进行设置
    if args.output_dir:
        server.set_output_dir(args.output_dir)

    # 默认使用stdio协议
    transport = "stdio"
    if args.transport:
        transport = args.transport

    # 验证API密钥
    if not config.MINERU_API_KEY:
        print("错误: MINERU_API_KEY 环境变量未设置。")
        print("请使用以下命令设置: export MINERU_API_KEY=your_api_key")
        print("或将其添加到当前目录的 .env 文件中。")
        sys.exit(1)
    
    # 打印配置信息
    print(f"MinerU PDF转Markdown转换服务")
    print(f"API 基础 URL: {config.MINERU_API_BASE}")
    print(f"API 密钥: {'已设置' if config.MINERU_API_KEY else '未设置'}")
    print(f"输出目录: {server.output_dir}")
    
    # 运行服务器
    server.mcp.run(transport=transport)

if __name__ == "__main__":
    main() 