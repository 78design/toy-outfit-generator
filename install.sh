#!/bin/bash

# 潮玩穿搭图生成工具 - 安装脚本

echo "开始安装..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 安装依赖
echo "正在安装Python依赖..."
pip3 install -r requirements.txt

# 赋予执行权限
chmod +x toy_outfit_generator.py

echo ""
echo "安装完成！"
echo ""
echo "配置说明："
echo "1. 复制 .env.example 为 .env"
echo "2. 编辑 .env 填入您的API密钥"
echo "3. 使用 python toy_outfit_generator.py --help 查看使用方法"
