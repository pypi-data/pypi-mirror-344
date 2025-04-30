"""MinerU PDF转Markdown转换服务的配置工具。"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()

# API 配置
MINERU_API_BASE = os.getenv("MINERU_API_BASE", "https://mineru.net")
MINERU_API_KEY = os.getenv("MINERU_API_KEY", "")

# 转换后文件的默认输出目录
DEFAULT_OUTPUT_DIR = os.getenv("PDF2MD_OUTPUT_DIR", "./downloads")

# 如果输出目录不存在，则创建它
def ensure_output_dir(output_dir=None):
    """
    确保输出目录存在。
    
    Args:
        output_dir: 输出目录的可选路径。如果为 None，则使用 DEFAULT_OUTPUT_DIR。
    
    Returns:
        表示输出目录的 Path 对象。
    """
    output_path = Path(output_dir or DEFAULT_OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path

# 验证 API 配置
def validate_api_config():
    """
    验证是否已设置所需的 API 配置。
    
    Returns:
        dict: 配置状态。
    """
    return {
        "api_base": MINERU_API_BASE,
        "api_key_set": bool(MINERU_API_KEY),
        "output_dir": DEFAULT_OUTPUT_DIR
    } 