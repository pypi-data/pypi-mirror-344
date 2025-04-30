"""OpenAI图像生成MCP服务器主入口"""

import sys
import traceback
import requests
import base64
import os
from typing import Optional, Literal

try:
    from mcp.server.fastmcp import FastMCP, Context
except ImportError:
    print("错误：需要安装 'mcp' 包才能运行此服务器。", file=sys.stderr)
    print("请运行: pip install mcp", file=sys.stderr)
    sys.exit(1)

# 创建FastMCP服务器实例
mcp = FastMCP("OpenAI图像生成服务", instructions="这个服务器提供OpenAI图像生成API的访问功能。")

# 默认API密钥和代理地址
DEFAULT_API_KEY = "sk-KohA4NPkpBqo6mmNO175JaGsJMiKplTmemchA64oUW1CCy9q"
DEFAULT_BASE_URL = "https://api.ssopen.top"

# 定义图像生成工具
@mcp.tool()
def generate_image(
    ctx: Context,
    prompt: str,
    size: str = "1024x1024", 
    quality: str = "medium", 
    model: str = "gpt-image-1"
) -> str:
    """生成图像并返回Base64编码的图像数据
    
    参数:
        prompt: 描述想要生成的图像的文本提示
        size: 图像尺寸，可选 "1024x1024"(默认), "1024x1536", "1536x1024"
        quality: 图像质量，可选 "low", "medium"(默认), "high", "auto"
        model: 使用的模型，默认为 "gpt-image-1"
    """
    # 使用默认值
    api_key = DEFAULT_API_KEY
    base_url = DEFAULT_BASE_URL
    
    # 日志记录
    if ctx:
        ctx.info(f"开始生成图像: {prompt[:50]}...")
        ctx.info(f"使用参数: 尺寸={size}, 质量={quality}, 模型={model}")
    else:
        print(f"开始生成图像: {prompt[:50]}...", file=sys.stderr)
    
    # 构建请求URL和头信息
    url = f"{base_url}/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 请求正文
    data = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality
    }
    
    try:
        # 发送请求
        if ctx:
            ctx.info("正在发送API请求...")
        else:
            print("正在发送API请求...", file=sys.stderr)
            
        response = requests.post(url, headers=headers, json=data)
        
        # 检查响应
        if response.status_code == 200:
            if ctx:
                ctx.info(f"请求成功! 状态码: {response.status_code}")
            else:
                print(f"请求成功! 状态码: {response.status_code}", file=sys.stderr)
                
            response_data = response.json()
            
            # 获取图像URL或base64数据 (根据API返回格式调整)
            if "data" in response_data and len(response_data["data"]) > 0:
                # 先尝试获取b64_json
                if "b64_json" in response_data["data"][0]:
                    image_data = response_data["data"][0]["b64_json"]
                # 如果没有b64_json，尝试获取url
                elif "url" in response_data["data"][0]:
                    image_url = response_data["data"][0]["url"]
                    # 下载图像并转换为base64
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        image_bytes = img_response.content
                        image_data = base64.b64encode(image_bytes).decode('utf-8')
                    else:
                        return f"Error: 无法下载图像，状态码: {img_response.status_code}"
                else:
                    return f"Error: 响应中没有找到图像数据: {response_data}"
            else:
                return f"Error: 响应格式不正确: {response_data}"
            
            if ctx:
                ctx.info("图像生成成功!")
            else:
                print("图像生成成功!", file=sys.stderr)
            
            return image_data
        else:
            error_msg = f"请求失败! 状态码: {response.status_code}. 错误: {response.text}"
            if ctx:
                ctx.error(error_msg)
            else:
                print(error_msg, file=sys.stderr)
            return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"图像生成过程中发生错误: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        else:
            print(error_msg, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
        return f"Error: {error_msg}"

# 定义图像保存工具
@mcp.tool()
def save_image_base64(
    ctx: Context,
    base64_data: str, 
    filename: str = "generated_image.png"
) -> str:
    """将Base64编码的图像数据保存为文件
    
    参数:
        base64_data: Base64编码的图像数据
        filename: 要保存的文件名
    
    返回:
        保存结果消息
    """
    try:
        if ctx:
            ctx.info(f"正在保存图像到: {filename}")
        else:
            print(f"正在保存图像到: {filename}", file=sys.stderr)
            
        # 解码base64数据并保存为图像文件
        image_bytes = base64.b64decode(base64_data)
        with open(filename, "wb") as f:
            f.write(image_bytes)
        
        success_msg = f"图像已成功保存为: {filename}"
        if ctx:
            ctx.info(success_msg)
        else:
            print(success_msg, file=sys.stderr)
        return success_msg
    except Exception as e:
        error_msg = f"保存图像过程中发生错误: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        else:
            print(error_msg, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
        return f"Error: {error_msg}"

# 定义资源：API状态检查
@mcp.resource("openai://api/status")
def check_api_status() -> dict:
    """检查OpenAI API状态
    
    返回:
        API状态信息
    """
    # 使用默认值
    api_key = DEFAULT_API_KEY
    base_url = DEFAULT_BASE_URL
    
    print(f"检查API状态: {base_url}", file=sys.stderr)
    
    try:
        # 构建请求URL和头信息 - 使用简单的models接口检查
        url = f"{base_url}/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 发送请求
        response = requests.get(url, headers=headers)
        
        # 检查响应
        if response.status_code == 200:
            return {
                "status": "online",
                "message": "API可用",
                "http_status": response.status_code
            }
        else:
            return {
                "status": "error",
                "message": f"API请求失败: {response.text}",
                "http_status": response.status_code
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"API检查过程中发生错误: {str(e)}",
            "http_status": None
        }

# 服务器启动入口
def main():
    """MCP服务器入口函数，供命令行或uvx调用"""
    try:
        print("OpenAI图像生成MCP服务正在启动...", file=sys.stderr)
        mcp.run()  # 启动服务器，此函数会阻塞直到服务器停止
        print("OpenAI图像生成MCP服务已停止。", file=sys.stderr)
    except Exception as e:
        print(f"启动或运行时发生错误: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

# 允许直接通过 python -m mcp_image_gen 运行
if __name__ == "__main__":
    main() 