"""MinerU PDF转Markdown转换的API客户端。"""
import requests
import os
import re
import time
import json
import asyncio
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import aiohttp
from . import config

class MinerUClient:
    """
    用于与 MinerU API 交互以将 PDF 转换为 Markdown 的客户端。
    """

    def __init__(self, api_base: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化 MinerU API 客户端。
        
        Args:
            api_base: MinerU API 的基础 URL (默认: 从环境变量获取)
            api_key: 用于向 MinerU 进行身份验证的 API 密钥 (默认: 从环境变量获取)
        """
        self.api_base = api_base or config.MINERU_API_BASE
        self.api_key = api_key or config.MINERU_API_KEY
        
        if not self.api_key:
            raise ValueError("需要 MINERU_API_KEY 但未提供")
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        向 MinerU API 发出请求。
        
        Args:
            method: HTTP 方法 (GET, POST 等)
            endpoint: API 端点路径 (不含基础 URL)
            **kwargs: 传递给 aiohttp 请求的其他参数
            
        Returns:
            dict: API 响应 (JSON 格式)
        """
        url = f"{self.api_base}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers
            
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
    
    async def submit_pdf_url_task(
        self, 
        pdf_url: str, 
        enable_ocr: bool = True
    ) -> Dict[str, Any]:
        """
        提交 PDF URL 以转换为 Markdown。
        
        Args:
            pdf_url: 要转换的 PDF 文件的 URL
            enable_ocr: 是否为转换启用 OCR
            
        Returns:
            dict: 任务信息，包括任务 ID
        """
        payload = {
            "url": pdf_url,
            "enable_formula": True,
            "language": "auto",
            "layout_model": "doclayout_yolo",
            "enable_table": True,
            "is_ocr": enable_ocr
        }
        
        response = await self._request(
            "POST", 
            "/api/v4/extract/task", 
            json=payload
        )
        
        return response
    
    async def submit_pdf_file_task(
        self, 
        file_path: str, 
        enable_ocr: bool = True
    ) -> Dict[str, Any]:
        """
        提交本地 PDF 文件以转换为 Markdown。
        
        Args:
            file_path: 本地 PDF 文件的路径
            enable_ocr: 是否为转换启用 OCR
            
        Returns:
            dict: 任务信息，包括batch_id
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"未找到 PDF 文件: {file_path}")
        
        # 步骤1: 获取文件上传URL
        payload = {
            "enable_formula": True,
            "language": "auto",  # 自动检测语言
            "layout_model": "doclayout_yolo",
            "enable_table": True,
            "files": [
                {
                    "name": file_path.name,
                    "is_ocr": enable_ocr,
                    "data_id": f"mineru_pdf2md_{int(time.time())}"  # 生成唯一ID
                }
            ]
        }
        
        response = await self._request(
            "POST",
            "/api/v4/file-urls/batch",
            json=payload
        )
        
        # 检查响应
        if "data" not in response or "batch_id" not in response["data"] or "file_urls" not in response["data"]:
            raise ValueError(f"获取上传URL失败: {response}")
        
        batch_id = response["data"]["batch_id"]
        upload_url = response["data"]["file_urls"][0]
        
        print("获取上传URL成功", response)
        
        # 步骤2: 上传文件 - 使用requests库直接上传，而非aiohttp
        
        
        try:
            with open(file_path, 'rb') as f:
                # 重要：不设置Content-Type，让OSS自动处理
                response = requests.put(upload_url, data=f)
                
                if response.status_code != 200:
                    raise ValueError(f"文件上传失败，状态码: {response.status_code}, 响应: {response.text}")
                
                print(f"文件 {file_path.name} 上传成功")
        except Exception as e:
            raise ValueError(f"文件上传失败: {str(e)}")
        
        # 返回包含batch_id的响应
        return {"data": {"batch_id": batch_id, "file_name": file_path.name}}
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        获取转换任务的状态。
        
        Args:
            task_id: 要检查的任务 ID
            
        Returns:
            dict: 任务状态信息
        """
        response = await self._request(
            "GET", 
            f"/api/v4/extract/task/{task_id}"
        )

        
        return response
    
    async def download_task_result(
        self, 
        task_id: str, 
        output_dir: Optional[str] = None
    ) -> str:
        """
        下载已完成转换任务的结果。
        
        Args:
            task_id: 已完成任务的 ID
            output_dir: 保存下载结果的目录
            
        Returns:
            str: 包含提取文件的目录路径
        """
        output_path = config.ensure_output_dir(output_dir)
        
        # 获取下载 URL
        task_info = await self.get_task_status(task_id)
        
        # 从响应数据字段中提取状态和下载 URL
        full_zip_url = None
        if "data" in task_info:
            status = task_info["data"].get("state")
            # 尝试从不同的字段获取下载URL
            full_zip_url = (
                task_info["data"].get("full_zip_url") or 
                task_info["data"].get("download_url")
            )
        else:
            status = task_info.get("status") or task_info.get("state")
            full_zip_url = task_info.get("download_url") or task_info.get("full_zip_url")
            
        if status != "done":
            raise ValueError(f"任务 {task_id} 未完成。状态: {status}")
        
        if not full_zip_url:
            raise ValueError(f"任务 {task_id} 没有可用的下载 URL")
        
        # 下载 ZIP 文件
        zip_path = output_path / f"{task_id}.zip"
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(full_zip_url, headers=headers) as response:
                response.raise_for_status()
                with open(zip_path, "wb") as f:
                    f.write(await response.read())
        
        # 解压到子文件夹
        extract_dir = output_path / task_id
        extract_dir.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # 解压后删除 ZIP 文件
        zip_path.unlink()
        
        return str(extract_dir)
    
    async def get_batch_task_status(self, batch_id: str) -> Dict[str, Any]:
        """
        获取批量转换任务的状态。
        
        Args:
            batch_id: 批量任务的ID
            
        Returns:
            dict: 批量任务状态信息
        """
        response = await self._request(
            "GET",
            f"/api/v4/extract-results/batch/{batch_id}"
        )
        
        return response
        
    async def process_pdf_to_markdown(
        self, 
        task_fn, 
        task_arg: str, 
        enable_ocr: bool = True,
        output_dir: Optional[str] = None,
        max_retries: int = 60,
        retry_interval: int = 5
    ) -> str:
        """
        从开始到结束处理 PDF 到 Markdown 的转换。
        
        Args:
            task_fn: 提交任务的函数 (submit_pdf_url_task 或 submit_pdf_file_task)
            task_arg: 任务函数的参数 (URL 或文件路径)
            enable_ocr: 是否启用 OCR
            output_dir: 结果的输出目录
            max_retries: 最大状态检查重试次数
            retry_interval: 状态检查之间的时间间隔 (秒)
            
        Returns:
            str: 包含提取的 Markdown 文件的目录路径
        """
        try:
            # 提交任务
            task_info = await task_fn(task_arg, enable_ocr)
            
            # 检查是否为批量任务（文件上传）或单个URL任务
            is_batch_task = "data" in task_info and "batch_id" in task_info["data"]
            
            if is_batch_task:
                # 批量任务处理
                batch_id = task_info["data"]["batch_id"]
                file_name = task_info["data"]["file_name"]
                print(f"批量任务提交成功。Batch ID: {batch_id}")
                
                # 轮询任务完成情况
                for i in range(max_retries):
                    status_info = await self.get_batch_task_status(batch_id)
                    
                    if "data" not in status_info or "extract_result" not in status_info["data"]:
                        print(f"获取批量任务状态失败: {status_info}")
                        await asyncio.sleep(retry_interval)
                        continue
                    
                    # 查找当前文件的状态
                    extract_result = None
                    for result in status_info["data"]["extract_result"]:
                        if result.get("file_name") == file_name:
                            extract_result = result
                            break
                    
                    if not extract_result:
                        print(f"在批量任务结果中未找到文件 {file_name}，等待 {retry_interval} 秒...")
                        await asyncio.sleep(retry_interval)
                        continue
                    
                    state = extract_result.get("state")
                    print(f"文件 {file_name} 状态: {state}")
                    
                    if state == "done":
                        # 获取下载链接
                        full_zip_url = extract_result.get("full_zip_url")
                        if not full_zip_url:
                            raise ValueError(f"任务完成但没有下载链接: {extract_result}")
                        
                        print(f"文件 {file_name} 处理完成")
                        
                        # 下载并解压结果
                        output_path = config.ensure_output_dir(output_dir)
                        zip_path = output_path / f"{batch_id}.zip"
                        
                        # 下载ZIP文件
                        async with aiohttp.ClientSession() as session:
                            async with session.get(full_zip_url) as response:
                                response.raise_for_status()
                                with open(zip_path, "wb") as f:
                                    f.write(await response.read())
                        
                        # 解压到子文件夹
                        extract_dir = output_path / batch_id
                        extract_dir.mkdir(exist_ok=True)
                        
                        with zipfile.ZipFile(zip_path, "r") as zip_ref:
                            zip_ref.extractall(extract_dir)
                        
                        # 解压后删除ZIP文件
                        zip_path.unlink()
                        
                        print(f"任务结果下载并提取到: {extract_dir}")
                        return str(extract_dir)
                    
                    elif state in ["failed", "error"]:
                        err_msg = extract_result.get("err_msg", "未知错误")
                        raise ValueError(f"文件 {file_name} 处理失败: {err_msg}")
                    
                    elif state in ["pending", "running", "converting"]:
                        # 如果是running状态，显示进度信息
                        if state == "running" and "extract_progress" in extract_result:
                            progress = extract_result["extract_progress"]
                            extracted = progress.get("extracted_pages", 0)
                            total = progress.get("total_pages", 0)
                            if total > 0:
                                percent = (extracted / total) * 100
                                print(f"处理进度: {extracted}/{total} 页 ({percent:.1f}%)")
                        
                        print(f"等待 {retry_interval} 秒...")
                        await asyncio.sleep(retry_interval)
                    else:
                        print(f"未知状态 '{state}'，等待 {retry_interval} 秒...")
                        await asyncio.sleep(retry_interval)
                
                raise TimeoutError(f"批量任务 {batch_id} 未在允许的时间内完成")
            
            else:
                # 旧的URL任务处理流程
                # 从响应数据字段中提取 task_id
                if "data" in task_info and "task_id" in task_info["data"]:
                    task_id = task_info["data"]["task_id"]
                else:
                    task_id = task_info.get("task_id")
                
                if not task_id:
                    raise ValueError(f"未能从响应中获取任务 ID: {task_info}")
                
                print(f"任务提交成功。任务 ID: {task_id}")
                
                # 轮询任务完成情况
                for i in range(max_retries):
                    status_info = await self.get_task_status(task_id)
                    
                    # 从响应数据字段中提取状态
                    if "data" in status_info:
                        status = status_info["data"].get("state")
                    else:
                        status = status_info.get("status") or status_info.get("state")
                    
                    if status == "done":
                        print(f"任务 {task_id} 完成成功")
                        break
                        
                    if status in ["failed", "error"]:
                        error_message = status_info.get("msg") or status_info.get("message", "Unknown error")
                        if "data" in status_info and "err_msg" in status_info["data"]:
                            error_message = status_info["data"]["err_msg"] or error_message
                        raise ValueError(f"任务 {task_id} 失败: {error_message}")
                    
                    print(f"任务 {task_id} 状态: {status}. 等待 {retry_interval} 秒...")
                    await asyncio.sleep(retry_interval)
                else:
                    raise TimeoutError(f"任务 {task_id} 未在允许的时间内完成")
                
                # 下载并提取结果
                result_path = await self.download_task_result(task_id, output_dir)
                print(f"任务结果下载并提取到: {result_path}")
                
                return result_path
            
        except Exception as e:
            print(f"处理 PDF 到 Markdown 失败: {str(e)}")
            raise 