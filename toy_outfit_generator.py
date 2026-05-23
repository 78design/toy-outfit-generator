#!/usr/bin/env python3
"""
潮玩穿搭图生成工具
专为潮玩博主设计的通用穿搭图生成工具
"""

import argparse
import base64
import os
import random
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

STYLES = {
    "streetwear": "街头潮流风格，oversize版型，个性配饰",
    "techwear": "机能风，科技面料，多口袋设计",
    "urban": "都市休闲风格，简约时尚，质感面料",
    "avant-garde": "先锋前卫风格，独特剪裁，艺术感设计",
    "casual": "休闲时尚风格，舒适自在，日常穿搭",
    "vintage": "复古风格，经典元素，怀旧氛围",
}

COLORS = {
    "black": "纯黑色调，神秘酷感",
    "white": "纯白色调，干净简约",
    "gray": "灰色系，高级感",
    "navy": "深蓝色，沉稳大气",
    "olive": "橄榄绿，复古质感",
    "cream": "奶油色，温柔优雅",
    "beige": "米色，自然舒适",
    "burgundy": "酒红色，复古优雅",
    "forest": "森林绿，自然清新",
    "charcoal": "炭灰色，沉稳内敛",
}

SCENES = {
    "urban_street": "城市街头，现代建筑背景",
    "cafe": "潮流咖啡馆，工业风装修",
    "rooftop": "城市天台，日落时分",
    "studio": "简约摄影棚，干净背景",
    "gallery": "艺术画廊，现代展览空间",
    "street_art": "街头艺术墙，涂鸦背景",
}

POSES = [
    "自然站立，身体微微侧转，一只手插在口袋",
    "倚靠在墙边，姿态放松自然",
    "行走中抓拍，动态感十足",
    "坐在台阶上，腿部自然交叉",
    "随意靠在栏杆上，眼神看向镜头",
    "微微侧身，一只手轻轻撩动头发",
    "双手交叉抱胸，自信姿态",
    "手持咖啡杯，悠闲自在",
]

EXPRESSIONS = [
    "自然微笑，眼神自信",
    "中性表情，酷感十足",
    "略带微笑，亲和力强",
    "专注表情，眼神坚定",
    "慵懒表情，随性自然",
]

ACCESSORIES = [
    "银色项链",
    "黑色棒球帽",
    "金属手链",
    "皮质斜挎包",
    "复古墨镜",
    "针织帽",
    "银色耳环",
    "帆布托特包",
    "细带手表",
    "珍珠项链",
]

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
    style_desc = STYLES.get(style, STYLES["streetwear"]) if style else random.choice(list(STYLES.values()))
    if color:
        color_desc = COLORS.get(color, COLORS["black"])
    else:
        random_color_key = random.choice(list(COLORS.keys()))
        color_desc = COLORS[random_color_key]
    scene_desc = SCENES.get(scene, SCENES["urban_street"]) if scene else random.choice(list(SCENES.values()))
    
    pose = random.choice(POSES)
    expression = random.choice(EXPRESSIONS)
    accessory = random.choice(ACCESSORIES)
    
    negative_prompts = [
        "未成年感", "年龄小于18岁", "年龄大于30岁",
        "男性特征",
        "身材臃肿", "比例失调", "平板身材", "无曲线感", "胸部平坦", "五五分身材", "六四分身材",
        "夸张妆容", "不自然表情",
        "僵硬姿势", "呆板站姿", "游客照摆拍", "双手自然下垂", "表情空洞", "眼神呆滞", "身体紧绷",
        "正式服装", "西装", "礼服", "暴露服装", "复杂图案抢镜", "大面积亮色", "品牌logo明显",
        "工装裤", "短款背心", "crop tops", "基础款白T恤", "牛仔裤", "平庸穿搭", "运动服",
        "路人感", "居家感", "甜美少女风", "可爱风",
        "杂乱背景", "其他人物抢镜", "不雅场景",
        "俯拍", "仰拍", "人物太满", "人物太小", "过度后期", "不自然光线", "模糊不清",
        "深景深", "背景过于清晰", "非3:4比例", "价格信息",
    ]
    
    prompt = f"""
    时尚潮玩穿搭博主风格，产品穿搭展示：
    
    主体描述：
    - 一位20-28岁的年轻女性，身材匀称有曲线感，比例协调，胸部挺拔
    - {pose}，{expression}
    - 自然妆容，不夸张
    
    穿搭风格：
    - {style_desc}
    - {color_desc}主色调
    - 佩戴{accessory}
    - 不要出现西装、礼服、暴露服装、工装裤、短款背心、白T恤配牛仔裤
    
    产品展示：
    - 身上佩戴或手持{product_name}
    - {product_desc if product_desc else '时尚潮玩产品'}
    - 产品作为主要展示对象，不要被其他元素抢风头
    
    场景环境：
    - {scene_desc}
    - 背景简洁不杂乱
    
    拍摄要求：
    - 平拍视角（eye-level）
    - 中远景（medium-wide shot），人物占画面约1/2高度
    - 浅景深，背景虚化
    - 3:4比例
    - 人物主体占画面约1/2到3/4，头部上方和脚下留有余量
    - 自然光线，清晰画质
    
    负面提示：
    - {', '.join(negative_prompts)}
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
  python toy_outfit_generator.py --product "潮玩手办" --ref-image product.jpg --style streetwear --color black --output street.png

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
    parser.add_argument("--style", choices=STYLES.keys(), help="穿搭风格")
    parser.add_argument("--color", choices=COLORS.keys(), help="主色调")
    parser.add_argument("--scene", choices=SCENES.keys(), help="场景类型")
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
