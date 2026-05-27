#!/bin/bash
set -e

TOOL_NAME="toy-outfit-generator"
INSTALL_DIR="${HOME}/.local/bin/${TOOL_NAME}"

echo "🚀 正在安装 ${TOOL_NAME}..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 清理旧版本
if [ -d "${INSTALL_DIR}" ]; then
    echo "🧹 清理旧版本..."
    rm -rf "${INSTALL_DIR}"
fi

# 创建安装目录
echo "📁 创建安装目录..."
mkdir -p "${INSTALL_DIR}"

# 复制文件
echo "📦 复制文件..."
cp -r . "${INSTALL_DIR}/"

# 添加执行权限
chmod +x "${INSTALL_DIR}/toy_outfit_generator.py"

# 创建符号链接
echo "🔗 创建命令链接..."
mkdir -p "${HOME}/.local/bin"
ln -sf "${INSTALL_DIR}/toy_outfit_generator.py" "${HOME}/.local/bin/toy"
ln -sf "${INSTALL_DIR}/toy_outfit_generator.py" "${HOME}/.local/bin/toy-outfit"

# 配置环境变量
if [ ! -f "${INSTALL_DIR}/.env" ]; then
    if [ -f "${INSTALL_DIR}/.env.example" ]; then
        cp "${INSTALL_DIR}/.env.example" "${INSTALL_DIR}/.env"
    fi
    echo ""
    echo "⚠️  请编辑 ${INSTALL_DIR}/.env 配置文件设置 API 密钥"
fi

# 安装Python依赖
echo ""
echo "📚 安装Python依赖..."
cd "${INSTALL_DIR}"
pip3 install -r requirements.txt > /dev/null 2>&1

echo ""
echo "✅ 安装成功！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 使用方式："
echo ""
echo "  方式一（命令方式）："
echo "    toy-outfit --product '毛绒挂件' --output outfit.png"
echo ""
echo "  方式二（Python直接运行）："
echo "    python3 ${INSTALL_DIR}/toy_outfit_generator.py \\"
echo "      --product '毛绒挂件' \\"
echo "      --output outfit.png"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 配置文件：${INSTALL_DIR}/.env"
echo "📂 安装目录：${INSTALL_DIR}"
echo ""
echo "💡 提示："
echo "   如果命令 'toy-outfit' 无法使用，请将 ~/.local/bin 添加到 PATH："
echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""
