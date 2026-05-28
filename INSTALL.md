# 安装说明

本文档提供详细的安装指南，包括多种安装方式。

## 📋 前置要求

在安装前，请确保您的系统满足以下要求：

| 要求 | 说明 |
|------|------|
| **操作系统** | Linux、macOS、Windows（WSL2） |
| **Python版本** | 3.8 或更高 |
| **包管理器** | pip3 |
| **Git** | （可选，用于源码安装） |

验证Python环境：
```bash
python3 --version
pip3 --version
```

## 🚀 安装方式

### 方式一：标准技能安装（最推荐）

通过 `npx skills add` 命令安装，这是最简单的方式：

```bash
npx skills add 78design/toy-outfit-generator
```

或使用完整GitHub URL：
```bash
npx skills add https://github.com/78design/toy-outfit-generator
```

安装完成后，直接使用 `toy-outfit` 命令即可。

---

### 方式二：在线一键安装

使用 curl：
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/78design/toy-outfit-generator/main/install-online.sh)"
```

使用 wget：
```bash
bash -c "$(wget -O- https://raw.githubusercontent.com/78design/toy-outfit-generator/main/install-online.sh)"
```

此脚本会：
1. 检查并安装Python依赖
2. 创建配置文件
3. 创建命令快捷方式
4. 提供配置指引

---

### 方式三：下载压缩包安装

1. 访问 [Releases](https://github.com/78design/toy-outfit-generator/releases) 页面
2. 下载最新的压缩包（推荐 zip 格式）
3. 解压并进入目录
4. 运行安装脚本

```bash
# 下载（示例为v3.1.0）
wget https://github.com/78design/toy-outfit-generator/releases/download/v3.1.0/toy-outfit-generator-3.1.0.zip

# 解压
unzip toy-outfit-generator-3.1.0.zip
cd toy-outfit-generator-3.1.0

# 安装
chmod +x install.sh
./install.sh
```

---

### 方式四：从源码安装

克隆仓库并安装：

```bash
# 克隆仓库
git clone https://github.com/78design/toy-outfit-generator.git
cd toy-outfit-generator

# 方式A：使用pip安装（推荐）
pip install -e .

# 方式B：使用提供的安装脚本
chmod +x install.sh
./install.sh

# 方式C：手动安装依赖
pip install -r requirements.txt
```

---

### 方式五：Docker安装（可选）

如果您使用Docker，可以创建Dockerfile：

```dockerfile
# 待添加
# Docker支持将在后续版本中提供
```

---

## ⚙️ 配置

安装完成后，需要配置API密钥。

### 方法1：环境变量（推荐）

临时配置（当前终端有效）：
```bash
export IMAGE_GEN_API_KEY="your-api-key"
```

永久配置（添加到 shell 配置文件）：
```bash
# 对于bash
echo 'export IMAGE_GEN_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc

# 对于zsh
echo 'export IMAGE_GEN_API_KEY="your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

### 方法2：.env文件

项目提供了配置示例文件：

```bash
cd <安装目录>
cp .env.example .env
# 编辑 .env 文件
```

配置文件内容示例：
```bash
# API配置
IMAGE_GEN_API_KEY=your-api-key-here
IMAGE_GEN_API_URL=https://api.1openapi.com/v1
IMAGE_GEN_MODEL=openai/gpt-image-2
```

---

## 🧪 验证安装

安装完成后，验证是否成功：

```bash
# 查看版本
toy-outfit --version

# 查看帮助
toy-outfit --help

# 测试运行（需要配置API密钥）
toy-outfit --product "测试产品" --output test.png
```

---

## 📁 安装位置

根据不同的安装方式，文件会安装在以下位置：

| 安装方式 | 安装位置 |
|----------|---------|
| 技能安装 | `~/.skills/toy-outfit-generator/` |
| 脚本安装 | `~/.local/bin/toy-outfit-generator/` |
| pip安装 | Python包目录 |
| 源码安装 | 当前目录 |

---

## 🔄 更新

### 更新到最新版本

使用技能安装的用户：
```bash
npx skills update 78design/toy-outfit-generator
```

或重新运行安装脚本：
```bash
# 如果保留了源码
cd toy-outfit-generator
git pull
./install.sh
```

---

## ❌ 卸载

### 使用技能卸载
```bash
npx skills remove 78design/toy-outfit-generator
```

### 手动卸载
```bash
# 删除安装目录
rm -rf ~/.local/bin/toy-outfit-generator

# 删除命令链接
rm -f ~/.local/bin/toy
rm -f ~/.local/bin/toy-outfit
```

---

## 🚩 常见问题

### Q: 提示找不到命令？
A: 确保 `~/.local/bin` 在您的PATH中：
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Q: Python版本太旧？
A: 请升级Python到3.8或更高版本。

### Q: 权限被拒绝？
A: 使用sudo或确保目标目录有写入权限。

### Q: 依赖安装失败？
A: 尝试使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 💡 下一步

安装完成后，请查看：
- [README.md](README.md) - 使用指南
- [SKILL.md](SKILL.md) - 技能完整文档
- [examples/](examples/) - 更多示例

---

如有问题，请提交 [Issue](https://github.com/78design/toy-outfit-generator/issues)。
