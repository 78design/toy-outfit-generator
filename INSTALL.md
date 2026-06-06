# 安装说明

## 快速安装

### 方式一：标准技能安装命令（最推荐！）

```bash
npx skills add 78design/toy-outfit-generator
```

或者使用完整 GitHub URL：

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

### 方式三：使用本地安装脚本

```bash
chmod +x install.sh
./install.sh
```

### 方式四：手动安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量（可选）：
```bash
cp .env.example .env
# 编辑 .env 文件，填入您的API密钥
```

## 快速开始

### 1. 配置API密钥

```bash
# 临时配置（当前终端有效）
export IMAGE_GEN_API_KEY="your-api-key"

# 永久配置（修改 .env 文件）
cp .env.example .env
# 编辑 .env 填入API密钥
```

### 2. 运行

```bash
# 查看帮助
python toy_outfit_generator.py --help

# 生成穿搭图
python toy_outfit_generator.py --product "毛绒挂件" --output outfit.png
```

## 更多详细使用方法请参考 README.md 或 SKILL.md
