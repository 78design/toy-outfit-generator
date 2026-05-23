#!/bin/bash
# toy-outfit-generator 在线安装脚本
# 一键安装潮玩穿搭图生成工具

VERSION="2.0.2"
REPO_URL="https://github.com/78design/toy-outfit-generator.git"
DIR_NAME="toy-outfit-generator"

echo "=============================================="
echo "   潮玩穿搭图生成工具 v${VERSION} 在线安装"
echo "=============================================="
echo ""

# 检查 git 是否安装
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 请先安装 git"
    exit 1
fi

# 检查 python3 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 请先安装 Python 3"
    exit 1
fi

# 检查 pip 是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 请先安装 pip"
    exit 1
fi

echo "✅ 系统环境检查通过"
echo ""

# 克隆仓库
echo "📥 正在从 GitHub 克隆仓库..."
if [ -d "$DIR_NAME" ]; then
    echo "⚠️ 检测到已存在 $DIR_NAME 目录"
    read -p "是否需要更新？[Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$DIR_NAME" && git pull
    fi
else
    git clone "$REPO_URL" "$DIR_NAME"
fi

if [ $? -ne 0 ]; then
    echo "❌ 克隆仓库失败"
    exit 1
fi

cd "$DIR_NAME"

echo "✅ 仓库获取成功"
echo ""

# 安装依赖
echo "📦 正在安装 Python 依赖..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装成功"
echo ""

# 创建示例配置文件
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ 已创建 .env 配置文件"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "=============================================="
echo "使用方法："
echo ""
echo "1. 先配置 API 密钥："
echo "   编辑 .env 文件，填入你的 API 密钥"
echo ""
echo "2. 文生图模式："
echo "   python toy_outfit_generator.py --product \"产品名称\" --output test.png"
echo ""
echo "3. 图生图模式（推荐）："
echo "   python toy_outfit_generator.py --product \"产品名称\" --ref-url \"产品图片链接\" --output test.png"
echo ""
echo "4. 查看帮助："
echo "   python toy_outfit_generator.py --help"
echo "=============================================="
echo ""
echo "🚀 开始使用吧！"
