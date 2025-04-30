"""MinerU PDF转Markdown转换的FastMCP服务器实现。"""

import os
import re
from typing import List, Optional, Union, Dict, Any
from pathlib import Path

from fastmcp import FastMCP
from . import config
from .api import MinerUClient

# 初始化 FastMCP 服务器
mcp = FastMCP("MinerU PDF to Markdown Conversion")

# 初始化 MinerU 客户端
client = MinerUClient()

# Markdown 文件的输出目录
output_dir = config.DEFAULT_OUTPUT_DIR

def set_output_dir(dir_path: str):
    """设置转换后文件的输出目录。"""
    global output_dir
    output_dir = dir_path
    config.ensure_output_dir(output_dir)
    return output_dir

def parse_list_input(input_str: str) -> List[str]:
    """
    解析可能包含由逗号或换行符分隔的多个项目的字符串输入。
    
    Args:
        input_str: 可能包含多个项目的字符串
        
    Returns:
        解析出的项目列表
    """
    if not input_str:
        return []
    
    # 按逗号、换行符或空格分割
    items = re.split(r'[,\n\s]+', input_str)
    
    # 移除空项目并处理带引号的项目
    result = []
    for item in items:
        item = item.strip()
        # 如果存在引号，则移除
        if (item.startswith('"') and item.endswith('"')) or \
           (item.startswith("'") and item.endswith("'")):
            item = item[1:-1]
        
        if item:
            result.append(item)
    
    return result

@mcp.tool()
async def convert_pdf_url(
    url: str, 
    enable_ocr: bool = True
) -> Dict[str, Any]:
    """
    将来自 URL 的 PDF 转换为 Markdown。
    
    Args:
        url: 要转换的 PDF 的 URL。多个 URL 可以用逗号或换行符分隔。
        enable_ocr: 启用 OCR 以从扫描的 PDF 中更好地提取文本。
        
    Returns:
        包含转换后的 Markdown 文件路径的字典。
    """
    urls = parse_list_input(url)
    
    if not urls:
        raise ValueError("未提供有效的 URL")
    
    if len(urls) == 1:
        # 单个 URL 处理
        result_path = await client.process_pdf_to_markdown(
            client.submit_pdf_url_task,
            urls[0],
            enable_ocr,
            output_dir
        )
        return {"status": "success", "result_path": result_path}
    else:
        # 批量处理
        results = {}
        errors = {}
        
        for url in urls:
            try:
                result_path = await client.process_pdf_to_markdown(
                    client.submit_pdf_url_task,
                    url,
                    enable_ocr,
                    output_dir
                )
                results[url] = result_path
            except Exception as e:
                errors[url] = str(e)
        
        return {
            "status": "completed" if not errors else "completed_with_errors",
            "results": results,
            "errors": errors
        }

@mcp.tool()
async def convert_pdf_file(
    file_path: str, 
    enable_ocr: bool = True
) -> Dict[str, Any]:
    """
    将本地 PDF 文件转换为 Markdown。
    
    Args:
        file_path: 要转换的 PDF 文件的路径。多个路径可以用逗号或换行符分隔。
        enable_ocr: 启用 OCR 以从扫描的 PDF 中更好地提取文本。
        
    Returns:
        包含转换后的 Markdown 文件路径的字典。
    """
    file_paths = parse_list_input(file_path)
    
    if not file_paths:
        raise ValueError("未提供有效的文件路径")
    
    if len(file_paths) == 1:
        # 单个文件处理
        result_path = await client.process_pdf_to_markdown(
            client.submit_pdf_file_task,
            file_paths[0],
            enable_ocr,
            output_dir
        )
        return {"status": "success", "result_path": result_path}
    else:
        # 批量处理
        results = {}
        errors = {}
        
        for path in file_paths:
            try:
                result_path = await client.process_pdf_to_markdown(
                    client.submit_pdf_file_task,
                    path,
                    enable_ocr,
                    output_dir
                )
                results[path] = result_path
            except Exception as e:
                errors[path] = str(e)
        
        return {
            "status": "completed" if not errors else "completed_with_errors",
            "results": results,
            "errors": errors
        }

@mcp.resource("status://api")
def api_status() -> str:
    """
    获取 MinerU API 配置的状态。
    
    Returns:
        包含 API 配置状态的字典。
    """
    return f"API status: Configured\nAPI base URL: {config.MINERU_API_BASE}\nAPI key: {'已设置' if config.MINERU_API_KEY else '未设置'}"

@mcp.resource("help://usage")
def usage_help() -> str:
    """
    获取有关使用 MinerU PDF转Markdown服务的帮助信息。
    
    Returns:
        包含使用帮助的字符串。
    """
    return """
# PDF to Markdown Conversion Service

## Available tools:

1. **convert_pdf_url** - Convert PDF URL to Markdown, supports single or multiple URLs
   - Parameters:
     - url: PDF file URL or URL list, can be separated by spaces, commas, or newlines
     - enable_ocr: Whether to enable OCR (default: True)

2. **convert_pdf_file** - Convert local PDF file to Markdown, supports single or multiple file paths
   - Parameters:
     - file_path: PDF file local path or path list, can be separated by spaces, commas, or newlines
     - enable_ocr: Whether to enable OCR (default: True)

## Tool functions:

- **convert_pdf_url**: Specifically designed for handling URL links, suitable for single or multiple URL inputs
- **convert_pdf_file**: Specifically designed for handling local files, suitable for single or multiple file path inputs

## Mixed input handling:

When handling both URL and local file inputs, please call the above two tools separately to handle the corresponding input parts.

## Usage examples:

```python
# Convert single URL
result = await client.call("convert_pdf_url", 
                          url="https://example.com/document.pdf",
                          enable_ocr=True)

# Convert multiple URLs (batch processing)
urls = '''
https://example.com/document1.pdf
https://example.com/document2.pdf
https://example.com/document3.pdf
'''
result = await client.call("convert_pdf_url", url=urls, enable_ocr=True)

# Convert multiple URLs with comma separation
result = await client.call("convert_pdf_url", 
                          url="https://example.com/doc1.pdf, https://example.com/doc2.pdf",
                          enable_ocr=True)

# Convert single local file
result = await client.call("convert_pdf_file", 
                         file_path="/path/to/document.pdf",
                         enable_ocr=True)

# Convert multiple local files (batch processing)
files = '''
/path/to/document1.pdf
/path/to/document2.pdf
/path/to/document3.pdf
'''
result = await client.call("convert_pdf_file", file_path=files, enable_ocr=True)

# Mixed input handling (URLs and local files)
url_result = await client.call("convert_pdf_url", url='''
https://example.com/doc1.pdf
https://example.com/doc2.pdf
''', enable_ocr=True)

file_result = await client.call("convert_pdf_file", file_path='''
/path/to/doc1.pdf
/path/to/doc2.pdf
''', enable_ocr=True)
```

## Conversion results:
Successful conversion returns a dictionary containing conversion result information, and the converted Markdown files will be saved in the specified output directory, with temporary downloaded files automatically handled.

## Resources:

- `status://api` - Get API configuration status
- `help://usage` - Get this help information
"""

@mcp.prompt()
def conversion_prompt(input_content: str = "") -> str:
    """
    创建PDF转Markdown处理提示，指导AI如何使用转换工具。
    
    Args:
        input_content: 用户输入的内容，可能包含PDF路径或URL
        
    Returns:
        指导AI使用转换工具的提示字符串
    """
    return f"""
Please convert the following PDF(s) to Markdown format according to the request below:

{input_content}

Please select the appropriate tool based on the input type:
- If it is a single or multiple URL(s), use the convert_pdf_url tool
- If it is a single or multiple local file path(s), use the convert_pdf_file tool
- If both URLs and local files are included, please use the above tools separately for each part

Tool usage guidelines:
1. Batch processing is supported - you can convert multiple URLs or file paths at once (separated by commas, spaces, or newlines)
2. OCR is enabled by default for better handling of scanned PDFs
3. The converted Markdown files will be saved in the specified output directory
4. For URLs, the system will automatically download and clean up temporary files after processing

Example input formats:
- URL: https://example.com/document.pdf
- Local file: /path/to/document.pdf
- Multiple URLs: https://example.com/doc1.pdf, https://example.com/doc2.pdf
- Multiple files: /path/to/doc1.pdf, /path/to/doc2.pdf

If you have special requirements for the conversion process, please specify the relevant parameters when using the tool.
"""

def run_server(mode=None):
    """运行 FastMCP 服务器。"""
    # 确保输出目录存在
    config.ensure_output_dir(output_dir)
    
    # 检查是否设置了 API 密钥
    if not config.MINERU_API_KEY:
        print(f"警告: MINERU_API_KEY 环境变量未设置。")
        print(f"使用以下命令设置: export MINERU_API_KEY=your_api_key")
    
    # 运行服务器
    if mode:
        mcp.run(mode)
    else:
        mcp.run() 