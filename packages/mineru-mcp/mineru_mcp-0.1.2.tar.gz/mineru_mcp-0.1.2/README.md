# MinerU MCP-Server

## 1. 概述

这个项目提供了一个 **MinerU MCP 服务器** (`mineru-mcp`)，它基于 **FastMCP** 框架构建。其主要功能是作为 **MinerU API** 的接口，用于将 PDF 文档转换为 Markdown 格式。

该服务器通过 MCP 协议公开了两个主要工具：
1.  转换通过 **URL** 提供的 PDF。
2.  转换存储为**本地文件**的 PDF。

这使得其他应用程序或 MCP 客户端能够轻松地集成 MinerU 的 PDF 到 Markdown 转换功能。

## 2. 核心功能

* **PDF 转 Markdown**: 接收 PDF 文件输入（单个或多个 URL、单个或多个本地路径），调用 MinerU API 进行内容提取和格式转换，最终生成 Markdown 文件。
* **批量处理**: 支持同时处理多个 PDF 文件（通过提供由空格、逗号或换行符分隔的 URL 列表或文件路径列表）。
* **OCR 支持**: 可选启用 OCR 功能（默认开启），以处理扫描版或图片型 PDF。
* **自动化流程**: 自动处理与 MinerU API 的交互，包括任务提交、状态轮询、结果下载和解压。
* **结果存储**: 将转换后的 Markdown 文件（通常包含在一个 ZIP 包内）下载并解压到指定的输出目录中。每个任务的结果存储在以任务 ID 命名的子目录中。

## 3. 安装

### 3.1 使用 pip 安装 (推荐)

如果你的包已发布到 PyPI 或其他 Python 包索引，可以直接使用 pip 安装：

```bash
pip install mineru-mcp
```

这种方式适用于不需要修改源代码的普通用户。

### 3.2 环境要求
*   Python >= 3.12

### 3.3 从源码安装

如果你需要修改源代码或进行开发，可以从源码安装。

克隆仓库并进入项目目录：

```bash
git clone <repository-url> # 替换为你的仓库 URL
cd mineru-mcp
```

推荐使用 `uv` 或 `pip` 配合虚拟环境进行安装：

**使用 uv (推荐):**
```bash
# 安装 uv (如果尚未安装)
# pip install uv

# 创建并激活虚拟环境
uv venv

# Linux/macOS
source .venv/bin/activate 
# Windows
# .venv\\Scripts\\activate

# 安装依赖和项目
uv pip install -e .
```

**使用 pip:**
```bash
# 创建并激活虚拟环境
python -m venv .venv

# Linux/macOS
source .venv/bin/activate 
# Windows
# .venv\\Scripts\\activate

# 安装依赖和项目
pip install -e .
```

### 3.4 环境变量配置

服务运行需要配置以下环境变量，可以将它们设置在项目根目录下的 `.env` 文件中，或者直接导出到环境中：

| 环境变量              | 描述                                          | 默认值                 | 是否必须     |
| :-------------------- | :-------------------------------------------- | :--------------------- | :----------- |
| `MINERU_API_KEY`    | 用于访问 MinerU API 的授权密钥 (Bearer Token) | 空字符串               | **是** |
| `MINERU_API_BASE`   | MinerU API 的基础 URL                         | `https://mineru.net` | 否           |
| `PDF2MD_OUTPUT_DIR` | 转换结果的输出目录                            | `./downloads`        | 否           |

**注意**: `MINERU_API_KEY` 是服务正常运行的**关键**，必须正确配置。

## 4. 使用方法

### 4.1 运行 MCP 服务器

确保已设置 `MINERU_API_KEY` 环境变量，并且处于已安装项目的虚拟环境中。

使用以下命令启动 MCP 服务器：

```bash
mineru-mcp [OPTIONS]
```

**可选参数:**

*   `--output-dir` 或 `-o`: 指定保存转换后文件的目录 (覆盖 `PDF2MD_OUTPUT_DIR` 环境变量，默认: `./downloads`)。
*   `--transport` 或 `-t`: 指定 MCP 协议类型 (默认: `stdio`, 可选: `sse`)。

示例:
```bash
# 使用默认设置启动 (stdio transport, ./downloads output)
mineru-mcp

# 指定输出目录并使用 sse transport
mineru-mcp -o /path/to/custom/output --transport sse 
```

启动后，服务会监听 MCP 请求（通过 `stdio` 或 `sse`，取决于 `--transport` 参数）。

### 4.2 使用 Python MCP 客户端

需要安装 `fastmcp` 客户端库 (`pip install fastmcp`)。

```python
import asyncio
from mcp.client import MCPClient

async def main():
    # 注意：这里的 transport 参数需要与服务器启动时使用的 transport 匹配
    # 如果服务器使用默认的 stdio 启动，客户端通常不需要指定 transport 
    # (具体取决于你的环境和 MCPClient 的实现)
    # 如果服务器使用 --transport sse 启动，客户端需要配置 SSE 连接
    # 此处假设服务器以 stdio 运行，客户端将通过子进程与之交互
    
    # 假设 mineru-mcp 命令在 PATH 中，或者提供完整路径
    # MCPClient 会启动 mineru-mcp 进程并使用 stdio 通信
    async with MCPClient(cmd=["mineru-mcp"]) as client:
        print("MCP Client Connected.")
        
        # --- 示例 1: 从单个 URL 转换 PDF ---
        try:
            result_single_url = await client.call(
                "convert_pdf_url", 
                url="https://arxiv.org/pdf/1706.03762.pdf", # 示例 PDF URL
                enable_ocr=True
            )
            print(f"\\n--- Single URL Conversion Result ---")
            print(result_single_url)
            # Output like: {'status': 'success', 'result_path': 'downloads/5a5e...'}
        except Exception as e:
            print(f"\\nError converting single URL: {e}")

        # --- 示例 2: 批量转换多个 URL ---
        try:
            multi_urls = '''
            https://arxiv.org/pdf/1706.03762.pdf
            https://arxiv.org/pdf/2305.10601.pdf 
            ''' # 使用换行符分隔
            result_multi_url = await client.call(
                "convert_pdf_url", 
                url=multi_urls,
                enable_ocr=True
            )
            print(f"\\n--- Multiple URL Conversion Result ---")
            print(result_multi_url)
            # Output like: {'status': 'completed', 'results': {...}, 'errors': {}}
        except Exception as e:
            print(f"\\nError converting multiple URLs: {e}")

        # --- 示例 3: 转换本地单个 PDF 文件 ---
        # 需要将 /path/to/your/document.pdf 替换为实际存在的本地 PDF 文件路径
        local_pdf_path = "/path/to/your/document.pdf" 
        try:
            # 确保文件存在或处理 FileNotFoundError
            if os.path.exists(local_pdf_path):
                 result_local_file = await client.call(
                     "convert_pdf_file", 
                     file_path=local_pdf_path,
                     enable_ocr=True
                 )
                 print(f"\\n--- Local File Conversion Result ---")
                 print(result_local_file)
            else:
                 print(f"\\nSkipping local file test: {local_pdf_path} not found.")
        except Exception as e:
            print(f"\\nError converting local file: {e}")
            
        # --- 示例 4: 批量转换多个本地文件 ---
        # 需要将路径替换为实际存在的本地 PDF 文件路径
        local_files_paths = '''
        /path/to/your/document1.pdf
        /path/to/your/document2.pdf 
        ''' # 使用换行符分隔
        try:
            # 简单检查，实际应用中可能需要更复杂的路径验证
            paths_to_process = [p.strip() for p in local_files_paths.strip().split('\\n') if os.path.exists(p.strip())]
            if paths_to_process:
                 paths_string = '\\n'.join(paths_to_process)
                 result_multi_local = await client.call(
                     "convert_pdf_file", 
                     file_path=paths_string,
                     enable_ocr=True
                 )
                 print(f"\\n--- Multiple Local Files Conversion Result ---")
                 print(result_multi_local)
            else:
                 print(f"\\nSkipping multiple local files test: No valid paths found in list.")
        except Exception as e:
             print(f"\\nError converting multiple local files: {e}")

if __name__ == "__main__":
    # 添加必要的 import
    import os 
    # 运行主函数
    asyncio.run(main())
```
**注意:** 上述 Python 示例假设 `mineru-mcp` 命令在系统 PATH 中。如果不在，你需要调整 `MCPClient(cmd=["/full/path/to/mineru-mcp"])`。同时，请确保替换示例 URL 和本地文件路径为有效值。对于本地文件，启动客户端的 Python 脚本需要有读取这些文件的权限。

## 5. MCP 工具接口

服务通过 FastMCP 提供了以下工具接口：

### 5.1. `convert_pdf_url`

* **功能**: 处理来自一个或多个 URL 的 PDF 文件转换请求。
* **MCP 调用名**: `convert_pdf_url`
* **参数**:
    * `url` (str):
        * 描述: 需要转换的 PDF 文件的 URL。可以是单个 URL 字符串，也可以是包含多个 URL 的字符串。
        * 多 URL 格式: 在单个字符串参数中，URL 之间可以用空格、逗号 (`,`) 或换行符 (`\n`) 分隔。程序会自动解析。
        * 必需: 是
    * `enable_ocr` (bool):
        * 描述: 是否启用 OCR 功能以优化扫描版 PDF 的文本提取。
        * 必需: 否
        * 默认值: `True`
* **返回**:
    * 单个 URL: `Dict[str, Any]` - `{'status': 'success', 'result_path': 'path/to/output/dir'}` 或抛出异常。
    * 多个 URL: `Dict[str, Any]` - `{'status': 'completed'|'completed_with_errors', 'results': {'url1': 'path1', ...}, 'errors': {'url2': 'error msg', ...}}`

### 5.2. `convert_pdf_file`

* **功能**: 处理来自一个或多个本地文件路径的 PDF 文件转换请求。
* **MCP 调用名**: `convert_pdf_file`
* **参数**:
    * `file_path` (str):
        * 描述: 需要转换的本地 PDF 文件的绝对或相对路径。可以是单个路径字符串，也可以是包含多个路径的字符串。
        * 多路径格式: 在单个字符串参数中，路径之间可以用空格、逗号 (`,`) 或换行符 (`\n`) 分隔。程序会自动解析。
        * 必需: 是
    * `enable_ocr` (bool):
        * 描述: 是否启用 OCR 功能。
        * 必需: 否
        * 默认值: `True`
* **返回**:
    * 单个文件路径: `Dict[str, Any]` - `{'status': 'success', 'result_path': 'path/to/output/dir'}` 或抛出异常。
    * 多个文件路径: `Dict[str, Any]` - `{'status': 'completed'|'completed_with_errors', 'results': {'path1': 'output_path1', ...}, 'errors': {'path2': 'error msg', ...}}`

## 6. 输出目录

* 转换后的文件默认保存在 `./downloads` 目录中，可以通过 `PDF2MD_OUTPUT_DIR` 环境变量或 `--output-dir` 命令行参数修改。
* 每个成功的转换任务会在此输出目录下创建一个以 MinerU 返回的任务 ID 命名的子文件夹。该子文件夹内包含从 MinerU 下载并解压得到的 Markdown 文件（通常是 `_res.md`）以及可能的图片等资源。

## 7. MCP 资源接口

服务还提供了以下资源接口，用于获取状态和帮助信息：

### 7.1. `status://api`

* **功能**: 获取 MinerU API 的配置状态（包括 API Base URL 和 API Key 是否设置）。
* **调用**: 通过 MCP 客户端访问 `status://api` 资源。
* **返回**: 包含状态信息的字符串。

### 7.2. `help://usage`

* **功能**: 提供工具的详细使用说明、参数解释和示例。
* **调用**: 通过 MCP 客户端访问 `help://usage` 资源。
* **返回**: 包含帮助文档的字符串。
