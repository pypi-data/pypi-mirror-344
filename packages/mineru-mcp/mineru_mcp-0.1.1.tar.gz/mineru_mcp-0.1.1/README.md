# PDF 到 Markdown 转换服务 - 业务文档

## 1. 概述

本文档旨在详细说明 PDF 到 Markdown 转换服务 (`mineru-pdf2md`) 的功能、使用方式、接口规则以及相关的配置和依赖项。该服务利用 MinerU API 将指定的 PDF 文件（通过 URL 或本地文件路径提供）转换为 Markdown 格式，方便后续处理和使用。

该服务基于 FastMCP 框架构建，提供了两个核心工具接口，分别用于处理来自网络 URL 的 PDF 和本地存储的 PDF 文件。

## 2. 核心功能

* **PDF 转 Markdown**: 接收 PDF 文件输入（URL 或本地路径），调用 MinerU API 进行内容提取和格式转换，最终生成 Markdown 文件。
* **批量处理**: 支持同时处理单个或多个 PDF 文件（URL 列表或文件路径列表）。
* **OCR 支持**: 可选启用 OCR 功能，以处理扫描版或图片型 PDF。
* **自动化流程**: 自动处理与 MinerU API 的交互，包括任务提交、状态轮询、结果下载和解压。
* **结果存储**: 将转换后的 Markdown 文件（通常包含在一个 ZIP 包内）下载并解压到指定的输出目录中。

## 3. 安装

### 3.1 使用 pip 安装

```bash
pip install mineru
```

### 3.2 从源码安装

克隆仓库并安装：

```bash
git clone <repository-url>
cd mineru
pip install -e .
```

### 3.3 环境变量配置

服务运行需要配置以下环境变量，通常存储在 `.env` 文件中：

| 环境变量              | 描述                                          | 默认值                 | 是否必须     |
| :-------------------- | :-------------------------------------------- | :--------------------- | :----------- |
| `MINERU_API_KEY`    | 用于访问 MinerU API 的授权密钥 (Bearer Token) | 空字符串               | **是** |
| `MINERU_API_BASE`   | MinerU API 的基础 URL                         | `https://mineru.net` | 否           |
| `PDF2MD_OUTPUT_DIR` | 转换结果的输出目录                            | `./downloads`        | 否           |

**注意**: `MINERU_API_KEY` 是服务正常运行的**关键**，必须正确配置。

## 4. 使用方法

### 4.1 运行服务器

```bash
# 确保设置了 MINERU_API_KEY 环境变量
export MINERU_API_KEY="your-api-key"

# 使用命令行工具启动服务器
mineru-pdf2md
```

### 4.2 使用 Python API

```python
import asyncio
from mcp.client import MCPClient

async def main():
    # 连接到 MCP 服务器
    client = MCPClient("http://localhost:8000")
    
    # 从 URL 转换 PDF
    result = await client.call("convert_pdf_url", 
                              url="https://example.com/document.pdf",
                              enable_ocr=True)
    print(f"Conversion result: {result}")
    
    # 转换本地 PDF 文件
    local_result = await client.call("convert_pdf_file", 
                                   file_path="/path/to/document.pdf",
                                   enable_ocr=True)
    print(f"Local conversion result: {local_result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 5. MCP 工具接口

服务通过 FastMCP 提供了以下工具接口：

### 5.1. `convert_pdf_url`

* **功能**: 处理来自一个或多个 URL 的 PDF 文件转换请求。
* **MCP 调用名**: `convert_pdf_url`
* **参数**:
  * `url` (str):
    * 描述: 需要转换的 PDF 文件的 URL。可以是单个 URL，也可以是包含多个 URL 的字符串。
    * 多 URL 格式: URL 之间可以用空格、逗号 (`,`) 或换行符 (`\n`) 分隔。如果 URL 本身包含在引号内，引号会被移除。
    * 必需: 是
  * `enable_ocr` (bool):
    * 描述: 是否启用 OCR 功能。
    * 必需: 否
    * 默认值: `True`

### 5.2. `convert_pdf_file`

* **功能**: 处理来自一个或多个本地文件路径的 PDF 文件转换请求。
* **MCP 调用名**: `convert_pdf_file`
* **参数**:
  * `file_path` (str):
    * 描述: 需要转换的本地 PDF 文件的路径。可以是单个路径，也可以是包含多个路径的字符串。
    * 多路径格式: 路径之间可以用空格、逗号 (`,`) 或换行符 (`\n`) 分隔。如果路径本身包含在引号内，引号会被移除。
    * 必需: 是
  * `enable_ocr` (bool):
    * 描述: 是否启用 OCR 功能。
    * 必需: 否
    * 默认值: `True`

## 6. 输出目录

* 转换后的文件默认保存在工作目录下的 `./downloads` 文件夹中。
* 每个成功的转换任务会在此目录下创建一个以 PDF 文件基本名称（去除特殊字符并用下划线替换空格）命名的子文件夹，并将解压后的 Markdown 文件存放在该子文件夹内。
* 程序内部可以通过 `set_output_dir(output_dir: str)` 函数修改输出目录，但该函数未作为 MCP 工具接口暴露。

## 7. MCP 资源接口

服务还提供了以下资源接口，用于获取状态和帮助信息：

### 7.1. `status://api`

* **功能**: 获取 MinerU API 的配置状态。
* **调用**: 通过 MCP 客户端访问 `status://api` 资源。

### 7.2. `help://usage`

* **功能**: 提供详细的工具使用说明和示例。
* **调用**: 通过 MCP 客户端访问 `help://usage` 资源。
