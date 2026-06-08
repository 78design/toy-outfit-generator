# 使用指南

本目录包含详细的使用文档。

## 目录

- [快速开始](#快速开始)
- [高级用法](#高级用法)
- [参数详解](#参数详解)
- [常见问题](#常见问题)

---

## 快速开始

### 最简单的用法

```bash
# 文生图
toy-outfit --product "毛绒挂件" --output outfit.png
```

### 带描述的文生图

```bash
toy-outfit --product "疯兔怪" \
    --desc "萌牙怪兽毛绒挂件，粉色系" \
    --output outfit_cute.png
```

### 图生图

```bash
# 使用本地图片作为参考
toy-outfit --product "潮玩手办" \
    --ref-image product.jpg \
    --output street_style.png
```

---

## 高级用法

### 批量生成多张图

```bash
# 一次生成5张不同的图
toy-outfit --product "毛绒挂件" \
    --count 5 \
    --output outfit.png
```

输出文件会自动命名为：
- outfit_1.png
- outfit_2.png
- outfit_3.png
- outfit_4.png
- outfit_5.png

### 复现结果（固定随机种子）

```bash
# 指定随机种子，可复现相同结果
toy-outfit --product "毛绒挂件" \
    --seed 12345 \
    --output outfit.png
```

### 自定义图片比例

```bash
# 1:1 正方形
toy-outfit --product "毛绒挂件" \
    --ratio "1:1" \
    --output square.png

# 16:9 横版
toy-outfit --product "潮玩手办" \
    --ratio "16:9" \
    --output wide.png
```

---

## 参数详解

### --product (必填)

产品名称，用于提示AI生成对应的穿搭。

```bash
toy-outfit --product "产品名称" --output out.png
```

### --desc (可选)

产品详细描述，帮助AI更好地理解产品特征。

```bash
toy-outfit --product "产品名" \
    --desc "详细描述，比如颜色、风格、材质等" \
    --output out.png
```

### --ratio (可选，默认3:4)

输出图片比例。

```bash
toy-outfit --product "产品名" \
    --ratio "3:4" \
    --output out.png
```

常用比例：
- `3:4` - 竖版（默认，适合社交媒体）
- `1:1` - 正方形（适合头像）
- `16:9` - 横版（适合视频封面）
- `9:16` - 竖版长图

### --ref-image (可选)

本地参考图片路径，可以多次使用。

```bash
toy-outfit --product "产品名" \
    --ref-image product1.jpg \
    --ref-image product2.jpg \
    --output out.png
```

### --ref-url (可选)

远程参考图片URL，可以多次使用。

```bash
toy-outfit --product "产品名" \
    --ref-url "https://example.com/image1.jpg" \
    --output out.png
```

### --output (必填)

输出文件路径。

```bash
toy-outfit --product "产品名" \
    --output ./outputs/result.png
```

### --api-url / --api-key / --model (可选)

覆盖环境变量配置，临时使用不同的API设置。

```bash
toy-outfit --product "产品名" \
    --api-url "https://custom-api.com/v1" \
    --api-key "custom-key" \
    --model "custom-model" \
    --output out.png
```

---

## 常见问题

### Q: 如何配置API？

A: 可以通过环境变量或.env文件配置：

```bash
# 方式1：环境变量
export IMAGE_GEN_API_KEY=your-key
export IMAGE_GEN_API_URL=https://api.1openapi.com/v1
export IMAGE_GEN_MODEL=openai/gpt-image-2

# 方式2：.env文件
cp .env.example .env
# 编辑.env填入信息
```

### Q: 提示图生图失败？

A: 如果multipart上传失败，系统会自动降级到base64方式。

### Q: 如何处理多个参考图？

A: 可以通过多次使用 --ref-image 或 --ref-url 参数添加多个参考图。

### Q: 生成的图片不理想？

A: 可以尝试：
- 添加更详细的 --desc 描述
- 尝试不同的随机种子
- 使用不同的比例
- 提供更清晰的参考图
