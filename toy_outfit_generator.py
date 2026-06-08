#!/usr/bin/env python3
"""
潮玩穿搭图生成工具
专为潮玩博主设计的通用穿搭图生成工具
"""

__version__ = "3.3.0"

import argparse
import base64
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import requests
except ImportError:
    print("Error: requests library not installed.")
    print("Run: pip install requests")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_API_URL = "https://api.1openapi.com/v1"
DEFAULT_MODEL = "openai/gpt-image-2"
DEFAULT_RATIO = "3:4"
# 常见比例对应的固定尺寸（根据API实际输出调整）
DIMENSIONS = {
    "1:1": "1088x1088",
    "3:4": "1086x1448",
    "4:3": "1448x1086",
    "9:16": "1088x1934",
    "16:9": "1934x1088",
}
DEFAULT_DIMENSION = "1086x1448"


def encode_image_to_base64(image_path: str) -> str:
    """将图片文件编码为 base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def download_image_from_url(url: str, output_path: str) -> bool:
    """从 URL 下载图片到本地"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        logger.info(f"   Downloaded reference image: {url}")
        return True
    except Exception as e:
        logger.error(f"   Failed to download image: {e}")
        return False


def extract_image_url_from_markdown(content: str) -> Optional[str]:
    """从 Markdown 内容中提取图片 URL"""
    pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
    match = re.search(pattern, content)
    return match.group(1) if match else None


def ensure_output_dir(output_path: str) -> None:
    """确保输出目录存在"""
    output_dir = Path(output_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"   Created output directory: {output_dir}")


def build_prompt(
    product_name: str,
    product_desc: str = "",
    random_seed: Optional[int] = None,
    ratio: str = DEFAULT_RATIO
) -> Tuple[str, int]:
    """构建生成图片的提示词"""
    if random_seed is None:
        random_seed = int(time.time() * 1000000) % 100000000

    # 获取固定尺寸
    dimension = DIMENSIONS.get(ratio, DEFAULT_DIMENSION)

    prompt_parts = [
        f"（随机种子: {random_seed}）",
        "",
        "主体：",
        "- 一位潮流穿搭博主",
        "- 年轻女性，九头身的完美身材比例",
        "- 自然、自信的姿态",
        "- 展现潮流穿搭风格与个人态度",
        "",
        "风格：",
        "- 潮流时尚风格",
        "- 有品味，不随波逐流",
        "- 避免过于正式或商务的氛围",
        "- 避免过于幼稚或甜美的感觉",
        "- 避免居家或运动感过重",
        "",
        "产品展示：",
        f"- 身上佩戴或手持{product_name}",
        f"- {product_desc if product_desc else '潮玩产品作为穿搭的一部分自然呈现'}",
        "- 产品清晰可见，与整体穿搭协调",
        "",
        "画面要求：",
        "- 构图自然，人物比例协调",
        "- 光线柔和自然",
        "- 背景简洁不抢镜",
        f"- 图片比例 {ratio}",
        f"- 图片尺寸必须是 {dimension}",
        "- 高质量视觉效果",
    ]

    return "\n".join(prompt_parts).strip(), random_seed


def generate_image(
    prompt: str,
    api_url: str,
    api_key: str,
    model: str,
    image_files: Optional[List[str]] = None,
    output_path: Optional[str] = None
) -> Optional[str]:
    """调用 API 生成图片"""
    # 确保 API URL 以 /chat/completions 结尾
    if not api_url.endswith("/chat/completions"):
        api_url = api_url.rstrip("/") + "/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # 验证参考图片是否存在
    valid_images = []
    if image_files:
        for image_file in image_files:
            if os.path.exists(image_file):
                valid_images.append(image_file)
            else:
                logger.warning(f"   Warning: Image file not found: {image_file}")

    # 记录模式
    if valid_images:
        logger.info(f"   Mode: Image-to-Image (refs: {', '.join(valid_images)})")
    else:
        logger.info(f"   Mode: Text-to-Image")

    logger.info(f"   Format: OpenAI compatible (base64 encoding)")

    # 构建消息
    content_parts = [{
        "type": "text",
        "text": prompt
    }]

    for image_file in valid_images:
        image_base64 = encode_image_to_base64(image_file)
        content_parts.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_base64}"
            }
        })

    messages = [{"role": "user", "content": content_parts}]
    payload = {"model": model, "messages": messages}

    # 发送请求
    logger.info(f"   Sending request to {api_url}...")
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=180
        )
        logger.info(f"   Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                content = message.get("content", "") if isinstance(message, dict) else str(message)

                if content:
                    image_url = extract_image_url_from_markdown(content)
                    if image_url:
                        logger.info(f"   Generated image URL: {image_url}")
                        if output_path:
                            ensure_output_dir(output_path)
                            download_image_from_url(image_url, output_path)
                            logger.info(f"   Image saved to: {output_path}")
                            return output_path
                        return image_url
                    else:
                        logger.warning(f"   No image URL found in response")
            else:
                logger.error(f"   Unexpected response structure")
        else:
            logger.error(f"   API Error Response Text: {response.text}")
    except Exception as e:
        logger.error(f"   Request failed: {str(e)}")

    return None


def main():
    """主函数"""
    # 解析参数
    parser = argparse.ArgumentParser(
        description=f"潮玩穿搭图生成工具 v{__version__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python toy_outfit_generator.py --product "毛绒挂件" --output outfit.png
  python toy_outfit_generator.py --product "潮玩手办" --ref-image product.jpg --output street.png
  python toy_outfit_generator.py --product "毛绒挂件" --output outfit.png --count 3 --seed 12345

环境变量:
  IMAGE_GEN_API_KEY    API密钥（必需）
  IMAGE_GEN_API_URL    API地址（默认：https://api.1openapi.com/v1）
  IMAGE_GEN_MODEL      模型名称（默认：openai/gpt-image-2）
        """
    )
    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument("--desc", help="产品描述")
    parser.add_argument("--ratio", default=DEFAULT_RATIO, help="图片比例（默认：3:4，支持如 3:4, 1:1, 16:9 等）")
    parser.add_argument("--ref-image", action="append", help="产品参考图路径（图生图模式，可多次使用）")
    parser.add_argument("--ref-url", action="append", help="产品参考图URL（自动下载，可多次使用）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--api-url", help="API地址")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--model", help="模型名称")
    parser.add_argument("--count", type=int, default=1, help="生成图片数量（默认：1）")
    parser.add_argument("--seed", type=int, help="随机种子（用于复现结果）")
    parser.add_argument("-v", "--version", action="version", version=f"toy_outfit_generator.py v{__version__}")

    args = parser.parse_args()

    # 获取配置
    api_key = args.api_key or os.environ.get("IMAGE_GEN_API_KEY")
    api_url = args.api_url or os.environ.get("IMAGE_GEN_API_URL", DEFAULT_API_URL)
    model = args.model or os.environ.get("IMAGE_GEN_MODEL", DEFAULT_MODEL)

    if not api_key:
        logger.error("Error: API key not provided. Use --api-key or set IMAGE_GEN_API_KEY environment variable.")
        sys.exit(1)

    # 打印欢迎信息
    logger.info("=" * 60)
    logger.info(f"潮玩穿搭图生成工具 v{__version__}")
    logger.info("=" * 60)
    logger.info(f"产品: {args.product}")
    if args.desc:
        logger.info(f"描述: {args.desc}")
    logger.info(f"输出: {args.output}")
    logger.info(f"比例: {args.ratio}")
    logger.info(f"数量: {args.count}")
    logger.info(f"API: {api_url}")
    logger.info(f"模型: {model}")
    logger.info("-" * 60)

    # 收集参考图片
    image_files = []
    if args.ref_image:
        image_files.extend(args.ref_image)

    # 下载远程参考图片
    temp_files = []
    if args.ref_url:
        for idx, url in enumerate(args.ref_url):
            temp_file = f"_temp_ref_{idx}.jpg"
            if download_image_from_url(url, temp_file):
                image_files.append(temp_file)
                temp_files.append(temp_file)

    try:
        # 循环生成多张图片
        for i in range(args.count):
            # 每次生成使用不同的 seed（除非用户指定了固定 seed）
            current_seed = args.seed if args.seed else None
            prompt, used_seed = build_prompt(
                args.product, args.desc, current_seed, args.ratio
            )

            # 确定输出文件名
            if args.count > 1:
                base, ext = os.path.splitext(args.output)
                current_output = f"{base}_{i+1}{ext}"
            else:
                current_output = args.output

            # 生成图片
            logger.info(f"\n[{i+1}/{args.count}] 生成图片...")
            logger.info(f"   Prompt:\n{prompt}")

            result = generate_image(
                prompt=prompt,
                api_url=api_url,
                api_key=api_key,
                model=model,
                image_files=image_files,
                output_path=current_output
            )

            if result:
                logger.info(f"   ✓ 成功生成图片")
            else:
                logger.error(f"   ✗ 图片生成失败")
    finally:
        # 清理临时文件
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    logger.info("\n" + "=" * 60)
    logger.info("任务完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
