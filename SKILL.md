---
name: toy-outfit-generator
description: 潮玩穿搭图生成工具 - 专为潮玩博主设计的通用穿搭图生成工具
version: 2.2.0
---

# 潮玩穿搭图生成工具

专为潮玩博主设计的通用穿搭图生成工具，支持文生图和图生图模式，采用反向规范控制（只说明禁止事项，不指定明确风格）。

## 🚀 安装方式

### 方式一：标准技能安装命令（最推荐！）

```bash
npx skills add 78design/toy-outfit-generator
```

或者使用完整 GitHub URL：

```bash
npx skills add https://github.com/78design/toy-outfit-generator
```

### 方式二：在线一键安装

使用 curl 一键安装：

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/78design/toy-outfit-generator/main/install-online.sh)"
```

或者使用 wget：

```bash
bash -c "$(wget -O- https://raw.githubusercontent.com/78design/toy-outfit-generator/main/install-online.sh)"
```

---

## 技能特点

- **通用设计**：适用于各类潮玩产品（毛绒挂件、手办、盲盒、零钱包等）
- **灵活输入**：支持本地图片和远程URL两种参考图模式
- **反向规范控制**：只说明禁止事项，不限制具体风格、色彩，让AI有更大发挥空间
- **产品一致性**：支持参考图模式，保持产品特征一致

## 安装

### 前置要求

- Python 3.8+
- pip

### 安装依赖（如果不使用一键安装）

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
  --ref-image product.jpg --output street.png
```

### 图生图模式（远程URL）

```bash
python toy_outfit_generator.py --product "盲盒公仔" \
  --ref-url "https://example.com/product.jpg" --output product.png
```

## 命令参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--product` | ✅ | 产品名称 |
| `--desc` | ❌ | 产品描述 |
| `--ref-image` | ❌ | 产品参考图路径（可多次使用） |
| `--ref-url` | ❌ | 产品参考图URL（可多次使用） |
| `--output` | ✅ | 输出文件路径 |
| `--api-url` | ❌ | API地址（覆盖环境变量） |
| `--api-key` | ❌ | API密钥（覆盖环境变量） |
| `--model` | ❌ | 模型名称（覆盖环境变量） |

## 摄影规范（禁止事项）

### 人物规范（禁止事项）
- ❌ 不要出现未成年感，年龄<18岁
- ❌ 不要出现成熟感，年龄>30岁
- ❌ 不要出现男性特征
- ❌ 不要身材臃肿，比例失调
- ❌ 不要平板身材，无曲线感
- ❌ 不要胸部平坦，无挺拔感
- ❌ 不要非九头身比例
- ❌ 不要夸张妆容
- ❌ 不要不自然表情
- ❌ 不要僵硬、呆板的站姿
- ❌ 不要游客照式的摆拍动作
- ❌ 不要双手自然下垂的僵硬姿势
- ❌ 不要表情空洞，眼神呆滞
- ❌ 不要身体紧绷，不自然

### 穿搭规范（禁止事项）
- ❌ 不要出现过于正式的服装（西装、礼服等）
- ❌ 不要出现暴露服装
- ❌ 不要出现复杂图案抢镜
- ❌ 不要出现大面积亮色
- ❌ 不要出现品牌logo明显
- ❌ 不要出现工装裤
- ❌ 不要出现短款背心、crop tops
- ❌ 不要出现基础款白T恤+牛仔裤的平庸穿搭
- ❌ 不要出现平庸穿搭
- ❌ 不要出现路人感、居家感
- ❌ 不要出现甜美少女风、可爱风

### 产品展示（禁止事项）
- ❌ 不要让产品过于隐蔽看不清
- ❌ 不要让其他元素抢产品的风头
- ❌ 不要改变产品颜色、款式、材质
- ❌ 不要产品模糊
- ❌ 不要产品被遮挡
- ❌ 不要毛绒挂件悬浮
- ❌ 不要挂件漂浮
- ❌ 不要挂件悬空
- ❌ 不要挂件未挂在包上
- ❌ 不要挂件穿模
- ❌ 不要挂件位置错乱
- ❌ 不要挂件脱离包体
- ❌ 不要挂件无挂扣连接
- ❌ 不要挂件浮空
- ❌ 不要不合理悬挂
- ❌ 不要错位
- ❌ 不要漂浮物体
- ❌ 不要悬空物体
- ❌ 不要穿帮

### 场景规范（禁止事项）
- ❌ 不要出现过于杂乱的背景
- ❌ 不要出现其他人物抢镜
- ❌ 不要出现品牌logo明显
- ❌ 不要出现不雅场景

### 拍摄规范（禁止事项）
- ❌ 不要俯拍或仰拍，只允许平拍
- ❌ 不要人物太满（脑袋和脚顶到画面边缘）
- ❌ 不要人物太小看不清穿搭
- ❌ 不要出现过度后期效果
- ❌ 不要出现不自然光线
- ❌ 不要出现模糊不清
- ❌ 不要出现全景清晰（深景深）
- ❌ 不要出现背景过于清晰抢镜
- ❌ 不要出现非3:4比例
- ❌ 不要让人物太满，脑袋和脚顶到画面边缘

### 商业规范（禁止事项）
- ❌ 不要出现价格信息
- ❌ 不要出现促销信息

### 核心要求
- 产品挂在包包上、拿在手里、放在口袋旁都可以
- 产品要清晰可见
- 人是穿搭的核心！

## 示例

```bash
# 生成穿搭图（文生图）
python toy_outfit_generator.py --product "毛绒挂件" --output outfit.png

# 生成穿搭图（图生图）
python toy_outfit_generator.py --product "潮玩手办" \
  --ref-image product.jpg --output street_style.png

# 使用远程URL作为参考图
python toy_outfit_generator.py --product "盲盒公仔" \
  --ref-url "https://example.com/product.jpg" --output product.png

# 带产品描述
python toy_outfit_generator.py --product "疯兔怪" \
  --desc "萌牙怪兽毛绒挂件" \
  --ref-image product.jpg --output fashion_疯兔怪_001.png
```

## 安全说明

⚠️ **重要提示**：
- 请妥善保管您的API密钥，不要上传到代码仓库
- 建议使用环境变量或.env文件管理密钥
- 本项目的.gitignore已配置为忽略敏感文件和生成的图片

## 项目结构

```
.
├── SKILL.md                # 技能说明文档
├── README.md              # 项目说明文档
├── INSTALL.md              # 专门安装说明文档
├── toy_outfit_generator.py # 主程序文件
├── install.sh            # 本地安装脚本
├── install-online.sh      # 在线安装脚本
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量配置示例
└── .gitignore            # Git忽略配置
```

## 版本更新

### v2.2.0 (2026-05-24)
- **新增**：在代码中添加 `__version__` 常量
- **新增**：`--version` 和 `-v` 选项查看版本
- **优化**：运行时显示版本号

### v2.1.0 (2026-05-24)
- **优化**：修复临时文件清理问题
- **优化**：移除未使用的 import
- **新增**：`npx skills add` 标准技能安装命令

### v2.0.3 (2026-05-23)
- **格式标准化**：按照标准技能格式整理项目结构
- 新增 `install.sh` 本地安装脚本
- 新增 `.env.example` 配置文件示例
- 新增 `INSTALL.md` 专门的安装说明文档
- 更新在线安装脚本配合标准格式

### v2.0.0 (2026-05-22)
- **重大更新**：规范系统重构为反向规范模式
- 只说明禁止事项，不限制具体风格、色彩
- 移除了style/color/scene参数
- 新增更详细的产品展示禁止规范
- 保持核心功能不变

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue。
