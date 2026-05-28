---
name: toy-outfit-generator
description: 潮玩穿搭图生成工具 - 专为潮玩博主设计的通用穿搭图生成工具
version: 3.1.0
author: 78design
license: MIT
---

# 潮玩穿搭图生成工具

专为潮玩博主设计的通用穿搭图生成工具，支持文生图和图生图模式，采用反向规范控制（只说明禁止事项，不指定明确风格）。

## 📋 技能信息

| 属性 | 值 |
|------|-----|
| **名称** | toy-outfit-generator |
| **版本** | 3.1.0 |
| **作者** | 78design |
| **许可证** | MIT |
| **语言** | Python |
| **类型** | CLI工具 |

## ✨ 核心功能

- **文生图模式**：根据产品描述生成穿搭图
- **图生图模式**：支持本地图片和远程URL参考
- **反向规范控制**：只说明禁止事项，不限制具体风格
- **自定义比例**：支持3:4、1:1、16:9等常用比例
- **批量生成**：支持一次生成多张图
- **随机种子**：支持指定随机种子复现结果

## 📦 安装方式

### 方式一：标准技能安装（最推荐）

```bash
npx skills add 78design/toy-outfit-generator
```

或使用完整URL：
```bash
npx skills add https://github.com/78design/toy-outfit-generator
```

### 方式二：在线一键安装

使用 curl：
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/78design/toy-outfit-generator/main/install-online.sh)"
```

使用 wget：
```bash
bash -c "$(wget -O- https://raw.githubusercontent.com/78design/toy-outfit-generator/main/install-online.sh)"
```

### 方式三：本地安装

1. 下载压缩包：[toy-outfit-generator-3.1.0.zip](https://github.com/78design/toy-outfit-generator/releases)
2. 解压后运行安装脚本：
```bash
chmod +x install.sh
./install.sh
```

### 方式四：从源码安装

```bash
git clone https://github.com/78design/toy-outfit-generator.git
cd toy-outfit-generator
pip install -e .
```

## ⚙️ 配置

### 环境变量

| 变量名 | 说明 | 必填 | 默认值 |
|---------|------|------|--------|
| `IMAGE_GEN_API_KEY` | API密钥 | ✅ | - |
| `IMAGE_GEN_API_URL` | API地址 | ❌ | `https://api.1openapi.com/v1` |
| `IMAGE_GEN_MODEL` | 模型名称 | ❌ | `openai/gpt-image-2` |

### 配置文件

项目提供 `.env.example` 作为参考配置文件，复制为 `.env` 后填入实际值即可：

```bash
cp .env.example .env
# 编辑 .env 配置文件
```

## 🚀 使用方法

### 基础命令

查看帮助：
```bash
toy-outfit --help
# 或
python -m toy_outfit_generator --help
```

查看版本：
```bash
toy-outfit --version
```

### 文生图

```bash
toy-outfit --product "毛绒挂件" --output outfit.png
```

### 图生图（本地图片）

```bash
toy-outfit --product "潮玩手办" --ref-image product.jpg --output street.png
```

### 图生图（远程URL）

```bash
toy-outfit --product "盲盒公仔" --ref-url "https://example.com/product.jpg" --output product.png
```

### 自定义比例

```bash
# 1:1 正方形
toy-outfit --product "毛绒挂件" --ratio "1:1" --output square.png

# 16:9 横版
toy-outfit --product "潮玩手办" --ratio "16:9" --output wide.png
```

### 批量生成

```bash
toy-outfit --product "毛绒挂件" --count 5 --output outfit.png
```

### 复现结果（随机种子）

```bash
toy-outfit --product "毛绒挂件" --seed 12345 --output outfit.png
```

## 📖 完整命令参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--product` | str | ✅ | - | 产品名称 |
| `--desc` | str | ❌ | - | 产品描述 |
| `--ratio` | str | ❌ | 3:4 | 图片比例（3:4、1:1、16:9等） |
| `--ref-image` | list | ❌ | - | 产品参考图路径（可多次使用） |
| `--ref-url` | list | ❌ | - | 产品参考图URL（可多次使用） |
| `--output` | str | ✅ | - | 输出文件路径 |
| `--api-url` | str | ❌ | 环境变量 | API地址（覆盖环境变量） |
| `--api-key` | str | ❌ | 环境变量 | API密钥（覆盖环境变量） |
| `--model` | str | ❌ | 环境变量 | 模型名称（覆盖环境变量） |
| `--count` | int | ❌ | 1 | 生成图片数量 |
| `--seed` | int | ❌ | - | 随机种子（用于复现结果） |
| `-h, --help` | - | ❌ | - | 显示帮助信息 |
| `-v, --version` | - | ❌ | - | 显示版本信息 |

## 📁 项目结构

```
toy-outfit-generator/
├── SKILL.md                # 技能说明（本文件）
├── README.md              # 项目说明
├── INSTALL.md             # 安装说明
├── pyproject.toml         # Python项目配置
├── requirements.txt       # 依赖列表
├── install.sh            # 本地安装脚本
├── install-online.sh      # 在线安装脚本
├── .env.example          # 环境变量配置示例
├── .gitignore            # Git忽略配置
├── src/                  # 源代码目录
│   ├── __init__.py
│   └── toy_outfit_generator.py  # 主程序
├── docs/                 # 文档目录
├── examples/             # 示例目录
└── .github/              # GitHub相关配置
    └── workflows/
        └── release.yml    # 自动化发布工作流
```

## 📚 文档

- [README.md](README.md) - 项目使用指南
- [INSTALL.md](INSTALL.md) - 详细安装说明
- [examples/](examples/) - 使用示例

## 🔄 更新日志

### v3.1.0 (2026-05-28)
- **新增**：`--ratio` 参数支持自定义图片比例
- **优化**：重构图生图模块，优先使用multipart/form-data上传
- **优化**：完善项目结构，符合标准技能规范
- **新增**：自动化GitHub Actions发布工作流
- **优化**：提供多种安装方式（压缩包、在线、技能安装）

### v3.0.0 (2026-05-27)
- **重大优化**：代码全面重构，提升可维护性和规范性
- **新增**：完整的类型提示（Type Hints）
- **新增**：标准化的Google风格文档字符串
- **新增**：专业的日志系统
- **新增**：自动创建输出目录功能
- **优化**：消除重复代码，提取公共函数
- **优化**：异常处理更完善

### 更早版本
- 详见 [README.md](README.md#版本更新)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
