#!/bin/bash
set -e

TOOL_NAME="toy-outfit-generator"
INSTALL_DIR="$HOME/.local/bin/$TOOL_NAME"

echo "🚀 正在安装 $TOOL_NAME ..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到pip3，请先安装pip3"
    exit 1
fi

echo "✅ 系统环境检查通过"
echo ""

# 清理旧版本
if [ -d "$INSTALL_DIR" ]; then
    echo "🧹 清理旧版本..."
    rm -rf "$INSTALL_DIR"
fi

# 创建安装目录
echo "📁 创建安装目录..."
mkdir -p "$INSTALL_DIR"

# 复制文件
echo "📦 复制文件..."

# 确定源文件位置
if [ -f "toy_outfit_generator.py" ]; then
    # 如果在源目录
    cp -r . "$INSTALL_DIR/"
elif [ -f "src/toy_outfit_generator.py" ]; then
    # 如果在标准结构中
    cp -r . "$INSTALL_DIR/"
    # 如果没有requirements.txt，尝试从其他位置复制
    if [ ! -f "$INSTALL_DIR/requirements.txt" ] && [ -f "requirements.txt" ]; then
        cp requirements.txt "$INSTALL_DIR/"
    fi
    if [ ! -f "$INSTALL_DIR/.env.example" ] && [ -f ".env.example" ]; then
        cp .env.example "$INSTALL_DIR/"
    fi
else
    echo "❌ 错误: 未找到源文件，请确保在正确的目录中运行"
    exit 1
fi

# 添加执行权限
chmod +x "$INSTALL_DIR/src/toy_outfit_generator.py" 2>/dev/null || true
chmod +x "$INSTALL_DIR/toy_outfit_generator.py" 2>/dev/null || true

# 创建符号链接
echo "🔗 创建命令链接..."
mkdir -p "$HOME/.local/bin"

# 确定主程序位置
if [ -f "$INSTALL_DIR/src/toy_outfit_generator.py" ]; then
    MAIN_SCRIPT="$INSTALL_DIR/src/toy_outfit_generator.py"
else
    MAIN_SCRIPT="$INSTALL_DIR/toy_outfit_generator.py"
fi

ln -sf "$MAIN_SCRIPT" "$HOME/.local/bin/toy"
ln -sf "$MAIN_SCRIPT" "$HOME/.local/bin/toy-outfit"
ln -sf "$MAIN_SCRIPT" "$HOME/.local/bin/toy-outfit-generator"

# 复制环境变量示例
if [ ! -f "$INSTALL_DIR/.env" ] && [ -f "$INSTALL_DIR/.env.example" ]; then
    cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"
    echo ""
    echo "⚠️  请编辑 $INSTALL_DIR/.env 配置文件设置API密钥"
elif [ ! -f "$INSTALL_DIR/.env" ] && [ -f ".env.example" ]; then
    cp ".env.example" "$INSTALL_DIR/.env"
    echo ""
    echo "⚠️  请编辑 $INSTALL_DIR/.env 配置文件设置API密钥"
fi

# 安装Python依赖
echo ""
echo "📚 安装Python依赖..."
cd "$INSTALL_DIR"
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    pip3 install requests>=2.31.0
fi

echo ""
echo "✅ 安装成功！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 使用方式："
echo ""
echo "  # 方式一：命令快捷方式"
echo "  toy-outfit --product \"毛绒挂件\" --output outfit.png"
echo ""
echo "  # 方式二：直接运行"
echo "  python3 $MAIN_SCRIPT --product \"毛绒挂件\" --output outfit.png"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 配置文件：$INSTALL_DIR/.env"
echo "📂 安装目录：$INSTALL_DIR"
echo ""
echo "💡 提示："
echo "   如果命令无法使用，请将 ~/.local/bin 添加到PATH"
echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""
echo "📖 完整文档："
echo "   安装目录下的 README.md 和 SKILL.md"
echo ""
