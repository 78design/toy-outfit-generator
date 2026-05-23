#!/usr/bin/env python3
"""
潮玩穿搭图生成工具
专为潮玩博主设计的通用穿搭图生成工具
"""

import argparse
import base64
import os
import re
import sys
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not installed.")
    print("Run: pip install requests")
    sys.exit(1)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def download_image_from_url(url, output_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"   Downloaded reference image: {url}")
        return True
    except Exception as e:
        print(f"   Failed to download image: {e}")
        return False

def extract_image_url_from_markdown(content):
    pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None

# 保持兼容性别名
download_image = download_image_from_url

def build_prompt(product_name, product_desc="", style=None, color=None, scene=None):
    
    negative_prompts = [
        "年龄小于18岁", "未成年感",
        "年龄大于30岁", "成熟感",
        "男性特征",
        "身材臃肿", "比例失调", "平板身材", "无曲线感", "胸部平坦", "五五分身材", "六四分身材", "非九头身",
        "夸张妆容", "不自然表情",
        "僵硬姿势", "呆板站姿", "游客照摆拍", "双手自然下垂", "表情空洞", "眼神呆滞", "身体紧绷",
        "正式服装", "西装", "礼服", "通勤风格", "商务风格", "暴露服装", "复杂图案抢镜", "大面积亮色", "品牌logo明显",
        "工装裤", "短款背心", "crop tops", "基础款白T恤", "牛仔裤", "平庸穿搭", "普通运动服",
        "路人感", "居家感", "甜美少女风", "可爱风",
        "杂乱背景", "其他人物抢镜", "品牌logo明显", "不雅场景",
        "俯拍", "仰拍", "人物太满", "人物太小", "过度后期", "不自然光线", "模糊不清",
        "深景深", "背景过于清晰", "非3:4比例",
        "价格信息", "促销信息",
        "产品模糊", "产品被遮挡", "毛绒挂件悬浮", "挂件漂浮", "挂件悬空", "挂件未挂在包上", "挂件穿模", "挂件位置错乱", "挂件脱离包体", "挂件无挂扣连接", "挂件浮空", "不合理悬挂", "错位", "漂浮物体", "悬空物体", "穿帮",
    ]
    
    prompt = f"""
    时尚潮玩穿搭博主风格，产品穿搭展示：
    
    人物规范（禁止事项）：
    - 不要出现未成年感，年龄<18岁
    - 不要出现成熟感，年龄>30岁
    - 不要出现男性特征
    - 不要身材臃肿，比例失调
    - 不要平板身材，无曲线感
    - 不要胸部平坦，无挺拔感
    - 不要非九头身比例
    - 不要夸张妆容
    - 不要不自然表情
    - 不要僵硬、呆板的站姿
    - 不要游客照式的摆拍动作
    - 不要双手自然下垂的僵硬姿势
    - 不要表情空洞，眼神呆滞
    - 不要身体紧绷，不自然
    
    穿搭规范（禁止事项）：
    - 不要出现过于正式的服装（西装、礼服等）
    - 不要出现暴露服装
    - 不要出现复杂图案抢镜
    - 不要出现大面积亮色
    - 不要出现品牌logo明显
    - 不要出现工装裤
    - 不要出现短款背心、crop tops
    - 不要出现基础款白T恤+牛仔裤的平庸穿搭
    - 不要出现平庸穿搭
    - 不要出现路人感、居家感
    - 不要出现甜美少女风、可爱风
    
    产品展示（禁止事项）：
    - 不要让产品过于隐蔽看不清
    - 不要让其他元素抢产品的风头
    - 不要改变产品颜色、款式、材质
    - 不要产品模糊
    - 不要产品被遮挡
    - 不要毛绒挂件悬浮
    - 不要挂件漂浮
    - 不要挂件悬空
    - 不要挂件未挂在包上
    - 不要挂件穿模
    - 不要挂件位置错乱
    - 不要挂件脱离包体
    - 不要挂件无挂扣连接
    - 不要挂件浮空
    - 不要不合理悬挂
    - 不要错位
    - 不要漂浮物体
    - 不要悬空物体
    - 不要穿帮
    
    场景规范（禁止事项）：
    - 不要出现过于杂乱的背景
    - 不要出现其他人物抢镜
    - 不要出现品牌logo明显
    - 不要出现不雅场景
    
    拍摄规范（禁止事项）：
    - 不要俯拍或仰拍，只允许平拍
    - 不要人物太满（脑袋和脚顶到画面边缘）
    - 不要人物太小看不清穿搭
    - 不要出现过度后期效果
    - 不要出现不自然光线
    - 不要出现模糊不清
    - 不要出现全景清晰（深景深）
    - 不要出现背景过于清晰抢镜
    - 不要出现非3:4比例
    - 不要让人物太满，脑袋和脚顶到画面边缘
    
    商业规范（禁止事项）：
    - 不要出现价格信息
    - 不要出现促销信息
    
    核心要求：
    - 身上佩戴或手持{product_name}
    - {product_desc if product_desc else '潮玩产品'}
    - 保持产品与参考图一致
    - 人是穿搭的核心！
    """
    
    return prompt.strip()

def generate_image(prompt, api_url, api_key, model, image_files=None, output_path=None):
    if not api_url.endswith("/chat/completions"):
        if api_url.endswith("/"):
            api_url = api_url + "chat/completions"
        else:
            api_url = api_url + "/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "user", "content": []}]

    messages[0]["content"].append({
        "type": "text",
        "text": prompt
    })

    if image_files and len(image_files) > 0:
        valid_images = []
        for image_file in image_files:
            if os.path.exists(image_file):
                valid_images.append(image_file)
            else:
                print(f"   Warning: Image file not found: {image_file}")
        
        if valid_images:
            print(f"   Mode: Image-to-Image (refs: {', '.join(valid_images)})")
            for image_file in valid_images:
                image_base64 = encode_image_to_base64(image_file)
                image_ext = Path(image_file).suffix.lower()
                mime_type = "image/jpeg" if image_ext in [".jpg", ".jpeg"] else "image/png"

                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}"
                    }
                })
        else:
            print("   Warning: No valid reference images found")
            print("   Falling back to text-to-image mode.")
    else:
        print("   Mode: Text-to-Image")

    print(f"   Model: {model}")
    print(f"   API: {api_url}")
    print(f"   Prompt preview: {prompt[:120]}...")

    payload = {
        "model": model,
        "messages": messages
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {})
            content = message.get("content", "")

            image_url = extract_image_url_from_markdown(str(content))
            if image_url:
                print(f"   Image URL: {image_url}")
                if output_path:
                    if download_image_from_url(image_url, output_path):
                        print(f"\n   Saved: {output_path}")
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
                                with open(output_path, "wb") as f:
                                    f.write(image_data)
                                print(f"\n   Saved: {output_path}")
                                return output_path

        print(f"\n   Failed: Cannot extract image from response")
        return None

    except requests.exceptions.Timeout:
        print("\n   Failed: API request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\n   Failed: API request error - {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="潮玩穿搭图生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python toy_outfit_generator.py --product "毛绒挂件" --output outfit.png
  python toy_outfit_generator.py --product "潮玩手办" --ref-image product.jpg --output street.png

环境变量:
  IMAGE_GEN_API_KEY    API密钥（必需）
  IMAGE_GEN_API_URL    API地址（默认：https://api.1openapi.com/v1）
  IMAGE_GEN_MODEL      模型名称（默认：openai/gpt-image-2）
        """
    )

    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument("--desc", help="产品描述")
    parser.add_argument("--ref-image", action="append", help="产品参考图路径（图生图模式，可多次使用）")
    parser.add_argument("--ref-url", action="append", help="产品参考图URL（自动下载，可多次使用）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--api-url", help="API地址")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--model", help="模型名称")

    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("IMAGE_GEN_API_KEY")
    api_url = args.api_url or os.environ.get("IMAGE_GEN_API_URL", "https://api.1openapi.com/v1")
    model = args.model or os.environ.get("IMAGE_GEN_MODEL", "openai/gpt-image-2")

    if not api_key:
        print("Error: API密钥必需")
        print("请通过 --api-key 参数或设置 IMAGE_GEN_API_KEY 环境变量")
        sys.exit(1)

    ref_images = []
    
    if args.ref_image:
        ref_images.extend(args.ref_image)
    
    if args.ref_url:
        with tempfile.TemporaryDirectory() as tmpdir:
            for idx, url in enumerate(args.ref_url):
                tmp_path = os.path.join(tmpdir, f"ref_{idx}.png")
                if download_image_from_url(url, tmp_path):
                    ref_images.append(tmp_path)
    
    print("构建穿搭提示词...")
    prompt = build_prompt(args.product, args.desc, args.style, args.color, args.scene)
    
    print("生成图片...")
    result = generate_image(
        prompt=prompt,
        api_url=api_url,
        api_key=api_key,
        model=model,
        image_files=ref_images if ref_images else None,
        output_path=args.output
    )

    if result:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
