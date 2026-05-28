#!/bin/bash
# 快速开始示例
# 运行前请确保已配置 IMAGE_GEN_API_KEY

echo "🧪 潮玩穿搭图生成工具 - 示例脚本"
echo ""

# 检查API密钥是否配置
if [ -z "$IMAGE_GEN_API_KEY" ]; then
    echo "❌ 错误: 请先设置 IMAGE_GEN_API_KEY 环境变量"
    echo "  export IMAGE_GEN_API_KEY=your-api-key"
    exit 1
fi

echo "✅ API密钥已配置"
echo ""

# 示例1: 基础文生图
echo "📝 示例1: 基础文生图"
toy-outfit --product "毛绒挂件" --output outfit_1.png
echo ""

# 示例2: 使用参考图
if [ -f "product.jpg" ]; then
    echo "🖼️  示例2: 使用参考图"
    toy-outfit --product "潮玩手办" --ref-image product.jpg --output street_1.png
else
    echo "ℹ️  提示: 如果有产品图片，可以使用 --ref-image 参数"
fi
echo ""

# 示例3: 自定义比例
echo "📐 示例3: 自定义比例（1:1正方形）"
toy-outfit --product "毛绒挂件" --ratio "1:1" --output square_1.png
echo ""

echo "✅ 示例完成！生成的图片在当前目录中。"
