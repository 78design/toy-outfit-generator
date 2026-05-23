---
name: toy-outfit-generator
description: 潮玩穿搭图生成工具 - 专为潮玩博主设计的通用穿搭图生成工具
version: 1.0.0
---

# 潮玩穿搭图生成工具

专为潮玩博主设计的通用穿搭图生成工具，支持文生图和图生图模式，集成严格的时尚穿搭摄影规范。

## 技能特点

- **通用设计**：适用于各类潮玩产品（毛绒挂件、手办、盲盒等）
- **灵活输入**：支持本地图片和远程URL两种参考图模式
- **严格规范控制**：年龄、性别、身材、妆容等多维度约束
- **丰富变化**：自动避免重复的颜色组合和穿搭风格

## 安装

### 前置要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

### 环境变量配置

```bash
export IMAGE_GEN_API_KEY="your-api-key"
export IMAGE_GEN_API_URL="https://api.1openapi.com/v1"
export IMAGE_GEN_MODEL="openai/gpt-image-2"
```

### 配置说明

| 环境变量 | 说明 | 必填 | 默认值 |
|---------|------|------|--------|
| `IMAGE_GEN_API_KEY` | API密钥 | ✅ | - |
| `IMAGE_GEN_API_URL` | API地址 | ❌ | `https://api.1openapi.com/v1` |
| `IMAGE_GEN_MODEL` | 模型名称 | ❌ | `openai/gpt-image-2` |

## 使用方法

### 文生图模式

```bash
python toy_outfit_generator.py --product "毛绒挂件" --output outfit.png
```

### 图生图模式（本地图片）

```bash
python toy_outfit_generator.py --product "潮玩手办" \
  --ref-image product.jpg --style streetwear --color black \
  --output street.png
```

### 图生图模式（远程URL）

```bash
python toy_outfit_generator.py --product "盲盒公仔" \
  --ref-url "https://example.com/product.jpg" --style urban \
  --output product.png
```

## 命令参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--product` | ✅ | 产品名称 |
| `--desc` | ❌ | 产品描述 |
| `--ref-image` | ❌ | 产品参考图路径（可多次使用） |
| `--ref-url` | ❌ | 产品参考图URL（自动下载，可多次使用） |
| `--output` | ✅ | 输出文件路径 |
| `--style` | ❌ | 穿搭风格 |
| `--color` | ❌ | 主色调 |
| `--scene` | ❌ | 场景类型 |
| `--api-url` | ❌ | API地址（覆盖环境变量） |
| `--api-key` | ❌ | API密钥（覆盖环境变量） |
| `--model` | ❌ | 模型名称（覆盖环境变量） |

## 穿搭风格

| 风格 | 描述 |
|------|------|
| streetwear | 街头潮流风格，oversize版型，个性配饰 |
| techwear | 机能风，科技面料，多口袋设计 |
| urban | 都市休闲风格，简约时尚，质感面料 |
| avant-garde | 先锋前卫风格，独特剪裁，艺术感设计 |
| casual | 休闲时尚风格，舒适自在，日常穿搭 |
| vintage | 复古风格，经典元素，怀旧氛围 |

## 颜色选项

| 颜色 | 描述 |
|------|------|
| black | 纯黑色调，神秘酷感 |
| white | 纯白色调，干净简约 |
| gray | 灰色系，高级感 |
| navy | 深蓝色，沉稳大气 |
| olive | 橄榄绿，复古质感 |
| cream | 奶油色，温柔优雅 |
| beige | 米色，自然舒适 |
| burgundy | 酒红色，复古优雅 |
| forest | 森林绿，自然清新 |
| charcoal | 炭灰色，沉稳内敛 |

## 场景类型

| 场景 | 描述 |
|------|------|
| urban_street | 城市街头，现代建筑背景 |
| cafe | 潮流咖啡馆，工业风装修 |
| rooftop | 城市天台，日落时分 |
| studio | 简约摄影棚，干净背景 |
| gallery | 艺术画廊，现代展览空间 |
| street_art | 街头艺术墙，涂鸦背景 |

## 摄影规范

### 人物规范
- 年龄：18-30岁女性
- 身材：匀称有曲线感，比例协调
- 妆容：自然不夸张
- 姿态：自然放松，避免僵硬摆拍

### 穿搭规范
- 风格：时尚酷感、街头潮流、个性设计感
- 禁忌：正式服装、暴露服装、品牌logo明显、基础款白T牛仔裤

### 拍摄规范
- 角度：平拍（eye-level）
- 景别：中远景，人物占画面约1/2高度
- 景深：浅景深，背景虚化
- 比例：3:4

## 示例

```bash
# 生成街头风格穿搭
python toy_outfit_generator.py --product "毛绒挂件" \
  --style streetwear --color black \
  --ref-image product.jpg --output street_style.png

# 生成城市天台场景
python toy_outfit_generator.py --product "潮玩手办" \
  --desc "精致的动漫手办，色彩丰富" \
  --style techwear --color gray --scene rooftop \
  --output rooftop_outfit.png

# 使用远程URL作为参考图
python toy_outfit_generator.py --product "盲盒公仔" \
  --ref-url "https://example.com/product.jpg" \
  --style urban --color beige --output urban_style.png
```

## 安全说明

⚠️ **重要提示**：
- 请妥善保管您的API密钥，不要上传到代码仓库
- 建议使用环境变量或.env文件管理密钥
- 本项目的`.gitignore`已配置为忽略敏感文件和生成的图片

## 项目结构

```
.
├── SKILL.md               # 技能说明文档
├── README.md              # 项目说明文档
├── toy_outfit_generator.py  # 主程序文件
├── requirements.txt       # Python依赖
└── .gitignore            # Git忽略配置
```

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue。
