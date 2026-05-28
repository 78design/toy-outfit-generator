#!/usr/bin/env python3
"""
潮玩穿搭图生成工具
专为潮玩博主设计的通用穿搭图生成工具
"""

__version__ = "3.1.0"

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

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 先检查 --version 和 -h/--help 选项，避免依赖检查影响这些操作
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
    """
    将图片文件编码为base64字符串

    Args:
        image_path: 图片文件路径

    Returns:
        base64编码的字符串
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def download_image_from_url(url: str, output_path: str) -> bool:
    """
    从URL下载图片到本地

    Args:
        url: 图片URL
        output_path: 输出文件路径

    Returns:
        是否下载成功
    """
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
    """
    从Markdown内容中提取图片URL

    Args:
        content: Markdown文本内容

    Returns:
        提取到的图片URL，未找到则返回None
    """
    pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def ensure_output_dir(output_path: str) -> None:
    """
    确保输出目录存在，不存在则创建

    Args:
        output_path: 输出文件路径
    """
    output_dir = Path(output_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"   Created output directory: {output_dir}")


def build_prompt(product_name: str, product_desc: str = "", random_seed: Optional[int] = None, ratio: str = "3:4") -> Tuple[str, int]:
    """
    构建潮玩穿搭提示词

    Args:
        product_name: 产品名称
        product_desc: 产品描述
        random_seed: 随机种子
        ratio: 图片比例（默认：3:4）

    Returns:
        (提示词文本, 使用的随机种子)
    """
    if random_seed is None:
        random_seed = int(time.time() * 1000000) % 100000000

    forbidden_items = {
        "人物规范": [
            "年龄小于18岁", "未成年感",
            "年龄大于30岁", "成熟感",
            "男性特征",
            "身材臃肿", "比例失调", "平板身材", "无曲线感", "胸部平坦", "五五分身材", "六四分身材", "非九头身",
            "夸张妆容", "不自然表情",
            "僵硬姿势", "呆板站姿", "游客照摆拍", "双手自然下垂", "表情空洞", "眼神呆滞", "身体紧绷"
        ],
        "穿搭规范": [
            "正式服装", "西装", "礼服", "通勤风格", "商务风格", "暴露服装", "复杂图案抢镜", "大面积亮色", "品牌logo明显",
            "工装裤", "短款背心", "crop tops", "基础款白T恤", "牛仔裤", "平庸穿搭", "普通运动服",
            "路人感", "居家感", "甜美少女风", "可爱风"
        ],
        "产品展示": [
            "产品模糊", "产品被遮挡", "毛绒挂件悬浮", "挂件漂浮", "挂件悬空", "挂件未挂在包上", "挂件穿模",
            "挂件位置错乱", "挂件脱离包体", "挂件无挂扣连接", "挂件浮空", "不合理悬挂", "错位", "漂浮物体",
            "悬空物体", "穿帮"
        ],
        "场景规范": [
            "杂乱背景", "其他人物抢镜", "品牌logo明显", "不雅场景"
        ],
        "拍摄规范": [
            "俯拍", "仰拍", "人物太满", "人物太小", "过度后期", "不自然光线", "模糊不清",
            "深景深", "背景过于清晰", f"非{ratio}比例"
        ],
        "商业规范": [
            "价格信息", "促销信息"
        ]
    }

    prompt_parts = [
        f"时尚潮玩穿搭博主风格，产品穿搭展示（随机种子: {random_seed}）：",
        ""
    ]

    for section, items in forbidden_items.items():
        prompt_parts.append(f"{section}（禁止事项）：")
        for item in items:
            prompt_parts.append(f"- 不要{item}")
        prompt_parts.append("")

    prompt_parts.extend([
        "核心要求：",
        f"- 身上佩戴或手持{product_name}",
        f"- {product_desc if product_desc else '潮玩产品'}",
        "- 保持产品与参考图一致",
        "- 人是穿搭的核心！"
    ])

    return "\n".join(prompt_parts).strip(), random_seed


def generate_image(
    prompt: str,
    api_url: str,
    api_key: str,
    model: str,
    image_files: Optional[List[str]] = None,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    调用API生成图片
    
    Args:
        prompt: 提示词
        api_url: API地址
        api_key: API密钥
        model: 模型名称
        image_files: 参考图片文件列表
        output_path: 输出文件路径
    
    Returns:
        保存的文件路径或图片URL，失败返回None
    """
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

    # 优先尝试 multipart/form-data 方式（传递本地文件）
    if valid_images:
        logger.info(f"   Mode: Image-to-Image (refs: {', '.join(valid_images)})")
        try:
            return generate_image_multipart(
                prompt=prompt,
                api_url=api_url,
                api_key=api_key,
                model=model,
                image_files=valid_images,
                output_path=output_path
            )
        except Exception as e:
            logger.warning(f"   Multipart upload failed, trying base64 fallback: {e}")
    
    # 使用 base64 编码方式作为备选（兼容 text-to-image 和 image-to-image）
    if valid_images:
        logger.info(f"   Mode: Image-to-Image (base64 fallback)")
    else:
        logger.info(f"   Mode: Text-to-Image")
    
    return generate_image_base64(
        prompt=prompt,
        api_url=api_url,
        api_key=api_key,
        model=model,
        image_files=valid_images,
        output_path=output_path
    )


def generate_image_multipart(
    prompt: str,
    api_url: str,
    api_key: str,
    model: str,
    image_files: List[str],
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    使用 multipart/form-data 方式上传本地文件调用API（优先使用）
    
    Args:
        prompt: 提示词
        api_url: API地址
        api_key: API密钥
        model: 模型名称
        image_files: 参考图片文件列表
        output_path: 输出文件路径
    
    Returns:
        保存的文件路径或图片URL，失败返回None
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    files = []
    for idx, image_file in enumerate(image_files):
        image_ext = Path(image_file).suffix.lower()
        mime_type = "image/jpeg" if image_ext in [".jpg", ".jpeg"] else "image/png"
        files.append((f"image_{idx}", (os.path.basename(image_file), open(image_file, "rb"), mime_type)))
    
    payload = {
        "model": model,
        "prompt": prompt
    }
    
    logger.info(f"   Model: {model}")
    logger.info(f"   API: {api_url}")
    logger.info(f"   Prompt preview: {prompt[:120]}...")
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            data=payload,
            files=files,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        return handle_image_response(result, output_path)
    finally:
        # 关闭打开的文件
        for _, (_, file_obj, _) in files:
            file_obj.close()


def generate_image_base64(
    prompt: str,
    api_url: str,
    api_key: str,
    model: str,
    image_files: List[str],
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    使用 base64 编码方式调用API（备选方案）
    
    Args:
        prompt: 提示词
        api_url: API地址
        api_key: API密钥
        model: 模型名称
        image_files: 参考图片文件列表
        output_path: 输出文件路径
    
    Returns:
        保存的文件路径或图片URL，失败返回None
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    
    if image_files:
        for image_file in image_files:
            image_base64 = encode_image_to_base64(image_file)
            image_ext = Path(image_file).suffix.lower()
            mime_type = "image/jpeg" if image_ext in [".jpg", ".jpeg"] else "image/png"
            
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            })
    
    logger.info(f"   Model: {model}")
    logger.info(f"   API: {api_url}")
    logger.info(f"   Prompt preview: {prompt[:120]}...")
    
    payload = {
        "model": model,
        "messages": messages
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return handle_image_response(result, output_path)
    except Exception as e:
        logger.error(f"   Failed: API request error - {e}")
        return None


def handle_image_response(result: dict, output_path: Optional[str]) -> Optional[str]:
    """
    处理API响应并保存图片
    
    Args:
        result: API响应结果
        output_path: 输出文件路径
    
    Returns:
        保存的文件路径或图片URL，失败返回None
    """
    if "choices" in result and len(result["choices"]) > 0:
        message = result["choices"][0].get("message", {})
        content = message.get("content", "")
        
        image_url = extract_image_url_from_markdown(str(content))
        if image_url:
            logger.info(f"   Image URL: {image_url}")
            if output_path:
                ensure_output_dir(output_path)
                if download_image_from_url(image_url, output_path):
                    logger.info(f"\n   Saved: {output_path}")
                    return output_path
            return image_url
        
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "image_url":
                    img_url = item.get("image_url", {}).get("url", "")
                    if img_url.startswith("data:image"):
                        base64_data = img_url.split(",")[1]
                        image_data = base64.b64decode(base64_data)
                        if output_path:
                            ensure_output_dir(output_path)
                            with open(output_path, "wb") as f:
                                f.write(image_data)
                            logger.info(f"\n   Saved: {output_path}")
                            return output_path
                    elif img_url.startswith("http"):
                        logger.info(f"   Image URL: {img_url}")
                        if output_path:
                            ensure_output_dir(output_path)
                            if download_image_from_url(img_url, output_path):
                                logger.info(f"\n   Saved: {output_path}")
                                return output_path
                        return img_url
        
        # 尝试直接从 images 字段获取
        if "images" in result and len(result["images"]) > 0:
            img_url = result["images"][0]
            logger.info(f"   Image URL: {img_url}")
            if output_path:
                ensure_output_dir(output_path)
                if download_image_from_url(img_url, output_path):
                    logger.info(f"\n   Saved: {output_path}")
                    return output_path
            return img_url
    
    logger.error(f"\n   Failed: Cannot extract image from response")
    return None


def parse_args() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        解析后的参数对象
    """
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
    parser.add_argument("--ratio", default="3:4", help="图片比例（默认：3:4，支持如 3:4, 1:1, 16:9 等）")
    parser.add_argument("--ref-image", action="append", help="产品参考图路径（图生图模式，可多次使用）")
    parser.add_argument("--ref-url", action="append", help="产品参考图URL（自动下载，可多次使用）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--api-url", help="API地址")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--model", help="模型名称")
    parser.add_argument("--count", type=int, default=1, help="生成图片数量（默认：1）")
    parser.add_argument("--seed", type=int, help="随机种子（用于复现结果）")

    return parser.parse_args()


def cleanup_temp_files(temp_files: List[str]) -> None:
    """
    清理临时文件

    Args:
        temp_files: 临时文件路径列表
    """
    logger.info("\n--- 清理临时文件 ---")
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                logger.info(f"   Cleaned up: {temp_file}")
            except Exception as e:
                logger.warning(f"   Warning: Failed to clean up {temp_file}: {e}")


def main() -> None:
    """主函数"""
    args = parse_args()

    logger.info(f"潮玩穿搭图生成工具 v{__version__}")
    logger.info("=" * 50)

    api_key = args.api_key or os.environ.get("IMAGE_GEN_API_KEY")
    api_url = args.api_url or os.environ.get("IMAGE_GEN_API_URL", "https://api.1openapi.com/v1")
    model = args.model or os.environ.get("IMAGE_GEN_MODEL", "openai/gpt-image-2")

    if not api_key:
        logger.error("Error: API密钥必需")
        logger.error("请通过 --api-key 参数或设置 IMAGE_GEN_API_KEY 环境变量")
        sys.exit(1)

    if args.count < 1:
        logger.error("Error: 生成数量必须大于0")
        sys.exit(1)

    ref_images = []
    temp_files = []

    if args.ref_image:
        ref_images.extend(args.ref_image)

    if args.ref_url:
        for idx, url in enumerate(args.ref_url):
            tmp_path = os.path.join(os.getcwd(), f"ref_{idx}.png")
            try:
                if download_image_from_url(url, tmp_path):
                    ref_images.append(tmp_path)
                    temp_files.append(tmp_path)
            except Exception as e:
                logger.error(f"   Error downloading URL {url}: {e}")

    success_count = 0

    for i in range(args.count):
        logger.info(f"\n--- 生成第 {i+1}/{args.count} 张图 ---")

        current_seed = args.seed
        if current_seed is not None:
            current_seed = current_seed + i

        logger.info("构建穿搭提示词...")
        prompt, used_seed = build_prompt(args.product, args.desc, current_seed, args.ratio)
        logger.info(f"   使用随机种子: {used_seed}")
        logger.info(f"   图片比例: {args.ratio}")

        if args.count == 1:
            output_path = args.output
        else:
            path_obj = Path(args.output)
            output_path = str(path_obj.parent / f"{path_obj.stem}_{i+1}{path_obj.suffix}")

        logger.info("生成图片...")
        result = generate_image(
            prompt=prompt,
            api_url=api_url,
            api_key=api_key,
            model=model,
            image_files=ref_images if ref_images else None,
            output_path=output_path
        )

        if result:
            success_count += 1

    cleanup_temp_files(temp_files)

    logger.info(f"\n--- 完成 ---")
    logger.info(f"成功生成: {success_count}/{args.count} 张图")

    sys.exit(0 if success_count > 0 else 1)


if __name__ == "__main__":
    main()
