# -*- coding: utf-8 -*-
# gen_mindmap.pyw 0.05: ASCII→PNG自動変換
from PIL import Image, ImageDraw, ImageFont
import datetime

# 入力・出力
src_path = "ascii_mindmap_flow_layer.txt"
dst_path = "ascii_mindmap_flow_layer.png"

# テキスト読み込み
with open(src_path, encoding="utf-8") as f:
    lines = f.read().splitlines()

# 設定
font = ImageFont.load_default()
line_h = 16
padding = 20
width = max(len(line) for line in lines) * 8 + padding * 2
height = len(lines) * line_h + padding * 2 + 30

# 画像生成
img = Image.new("RGB", (width, height), (20, 20, 20))
draw = ImageDraw.Draw(img)
y = padding

for line in lines:
    draw.text((padding, y), line, font=font, fill=(240, 240, 240))
    y += line_h

# タイムスタンプ
ts = datetime.datetime.now().strftime("Generated: %Y-%m-%d %H:%M:%S")
draw.text((padding, height - 25), ts, font=font, fill=(150, 150, 150))

img.save(dst_path)
print(f"✅ PNG saved: {dst_path}")
