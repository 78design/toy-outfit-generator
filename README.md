# 潮玩穿搭图生成工具

专为潮玩博主设计的通用穿搭图生成工具，支持文生图和图生图模式，采用反向规范控制（只说明禁止事项，不指定明确风格）。

![Version](https://img.shields.io/badge/version-3.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow)

## ✨ 核心功能

- **文生图模式**：根据产品描述生成穿搭图
- **图生图模式**：支持本地图片和远程URL参考
- **反向规范控制**：只说明禁止事项，不限制具体风格
- **自定义比例**：支持3:4、1:1、16:9等常用比例
- **批量生成**：支持一次生成多张图
- **随机种子**：支持指定随机种子复现结果

## 🚀 快速开始

### 前置要求

- Python 3.8+
- pip

### 安装

查看详细安装说明：[INSTALL.md](INSTALL.md)

最简单的方式：
```bash
npx skills add 78design/toy-outfit-generator
```

### 配置

设置API密钥：
```bash
export IMAGE_GEN_API_KEY="your-api-key"
```

或使用配置文件：
```bash
cp .env.example .env
# 编辑 .env 文件
```

### 运行

```bash
# 文生图
toy-outfit --product "毛绒挂件" --output outfit.png

# 图生图
toy-outfit --product "潮玩手办" --ref-image product.jpg --output street.png

# 自定义比例
toy-outfit --product "毛绒挂件" --ratio "1:1" --output square.png
```

## 📖 完整文档

- [SKILL.md](SKILL.md) - 技能完整说明
- [INSTALL.md](INSTALL.md) - 详细安装说明
- [examples/](examples/) - 使用示例

## 📝 命令参数

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

## 🔄 版本更新

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

### v2.3.0 (2026-05-26)
- **重要优化**：解决了生成多张图返回相同图片的问题
- **新增**：`--count` 参数支持一次生成多张图
- **新增**：`--seed` 参数支持指定随机种子复现结果

完整更新日志：详见 [CHANGELOG.md](CHANGELOG.md)（或SKILL.md）

## 📁 项目结构

```
toy-outfit-generator/
├── SKILL.md                # 技能说明
├── README.md              # 项目说明（本文件）
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

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
