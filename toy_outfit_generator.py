#!/usr/bin/env python3
"""
潮玩穿搭图生成工具
专为潮玩博主设计的通用穿搭图生成工具
"""

__version__ = "3.2.0"

import argparse
import base64
import logging
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

if "--version" in sys.argv or "-v" in sys.argv:
    print(f"toy_outfit_generator.py v{__version__}")
    sys.exit(0)

if "-h" in sys.argv or "--help" in sys.argv:
    from argparse import RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(
        description=f"潮玩穿搭图生成工具 v{__version__}",
        formatter_class=RawDescriptionHelpFormatter,
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
    parser.add_argument("--ratio", default="3:4", help="图片比例（默认：3:4，支持如 3:4, 1:1, 16:9 等）")
    parser.add_argument("--ref-image", action="append", help="产品参考图路径（图生图模式，可多次使用）")
    parser.add_argument("--ref-url", action="append", help="产品参考图URL（自动下载，可多次使用）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--api-url", help="API地址")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--model", help="模型名称")
    parser.add_argument("--count", type=int, default=1, help="生成图片数量（默认：1）")
    parser.add_argument("--seed", type=int, help="随机种子（用于复现结果）")
    parser.print_help()
    sys.exit(0)

try:
    import requests
except ImportError:
    logger.error("Error: requests library not installed.")
    logger.error("Run: pip install requests")
    sys.exit(1)


def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def download_image_from_url(url: str, output_path: str) -> bool:
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
    pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def ensure_output_dir(output_path: str) -> None:
    output_dir = Path(output_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"   Created output directory: {output_dir}")


# 当 --count > 1 时，从元素池随机组合场景描述，确保每张图不同
_SCENE_LOCATIONS = [
    "都市街角", "咖啡店", "画廊展厅", "城市天台", "创意工作室",
    "街边长椅", "地铁站台", "海边码头", "户外公园", "独立书店",
    "花店门口", "唱片店内", "复古市集", "天桥过道", "露台花园",
]
_SCENE_LIGHTING = [
    "自然光", "暖色灯光", "柔和侧光", "落日余晖", "清晨阳光",
    "霓虹灯光", "散射柔光", "窗边逆光",
]
_SCENE_ATMOSPHERE = [
    "慵懒氛围", "活力氛围", "沉静氛围", "随性氛围", "酷感氛围",
    "温暖氛围", "清新氛围", "文艺氛围",
]


def _random_scene() -> str:
    loc = random.choice(_SCENE_LOCATIONS)
    light = random.choice(_SCENE_LIGHTING)
    atm = random.choice(_SCENE_ATMOSPHERE)
    return f"{loc}，{light}，{atm}"


def build_prompt(
    product_name: str,
    product_desc: str = "",
    random_seed: Optional[int] = None,
    ratio: str = "3:4",
    scene_variation: Optional[str] = None
) -> Tuple[str, int]:
    if random_seed is None:
        random_seed = int(time.time() * 1000000) % 100000000

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
        "- 高质量视觉效果",
        "",
        "场景/背景：",
        f"- {scene_variation}" if scene_variation else "",
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
    if not api_url.endswith("/chat/completions"):
        api_url = api_url.rstrip("/") + "/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    valid_images = []
    if image_files:
        for image_file in image_files:
            if os.path.exists(image_file):
                valid_images.append(image_file)
            else:
                logger.warning(f"   Warning: Image file not found: {image_file}")

    if valid_images:
        logger.info(f"   Mode: Image-to-Image (refs: {', '.join(valid_images)})")
    else:
        logger.info(f"   Mode: Text-to-Image")

    logger.info(f"   Format: OpenAI compatible (base64 encoding)")

    messages = []
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

    messages.append({
        "role": "user",
        "content": content_parts
    })

    payload = {
        "model": model,
        "messages": messages
    }

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
                if isinstance(message, dict):
                    content = message.get("content", "")
                else:
                    content = str(message)
                
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
    parser = argparse.ArgumentParser(description="潮玩穿搭图生成工具")
    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument("--desc", help="产品描述")
    parser.add_argument("--ratio", default="3:4", help="图片比例")
    parser.add_argument("--ref-image", action="append", help="产品参考图路径")
    parser.add_argument("--ref-url", action="append", help="产品参考图URL")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--api-url", help="API地址")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--model", help="模型名称")
    parser.add_argument("--count", type=int, default=1, help="生成图片数量")
    parser.add_argument("--seed", type=int, help="随机种子")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("IMAGE_GEN_API_KEY")
    api_url = args.api_url or os.environ.get("IMAGE_GEN_API_URL", "https://api.1openapi.com/v1")
    model = args.model or os.environ.get("IMAGE_GEN_MODEL", "openai/gpt-image-2")

    if not api_key:
        logger.error("Error: API key not provided. Use --api-key or set IMAGE_GEN_API_KEY environment variable.")
        sys.exit(1)

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

    image_files = []
    if args.ref_image:
        image_files.extend(args.ref_image)

    if args.ref_url:
        for idx, url in enumerate(args.ref_url):
            temp_file = f"_temp_ref_{idx}.jpg"
            if download_image_from_url(url, temp_file):
                image_files.append(temp_file)

    for i in range(args.count):
        current_seed = args.seed if args.seed else None
        scene = None
        if args.count > 1:
            scene = _random_scene()
        prompt, used_seed = build_prompt(
            args.product, args.desc, current_seed, args.ratio, scene
        )
        
        if args.count > 1:
            base, ext = os.path.splitext(args.output)
            current_output = f"{base}_{i+1}{ext}"
        else:
            current_output = args.output

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

    if args.ref_url:
        for idx in range(len(args.ref_url)):
            temp_file = f"_temp_ref_{idx}.jpg"
            if os.path.exists(temp_file):
                os.remove(temp_file)

    logger.info("\n" + "=" * 60)
    logger.info("任务完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
