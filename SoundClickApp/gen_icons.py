"""生成应用图标 PNG（多尺寸）"""
import struct
import zlib
import os
import math

def create_png(width, height, pixels):
    """最小化 PNG 生成器（不依赖 Pillow）"""
    def pack_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    # 构建原始像素数据（RGBA）
    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter type: None
        for x in range(width):
            raw += bytes(pixels[y][x])
    
    compressed = zlib.compress(raw, 9)
    
    png = b'\x89PNG\r\n\x1a\n'
    png += pack_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png += pack_chunk(b'IDAT', compressed)
    png += pack_chunk(b'IEND', b'')
    return png

def generate_icon(size):
    pixels = [[[0, 0, 0, 0] for _ in range(size)] for _ in range(size)]
    cx, cy = size / 2, size / 2
    r = size / 2
    
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist <= r:
                # 渐变背景：深紫到亮紫
                t = dist / r
                bg_r = int(13 + (123 - 13) * (1 - t))
                bg_g = int(13 + (104 - 13) * (1 - t))
                bg_b = int(26 + (238 - 26) * (1 - t))
                
                # 边框高光
                if dist > r * 0.88:
                    border_t = (dist - r * 0.88) / (r * 0.12)
                    bg_r = int(bg_r * (1 - border_t) + 155 * border_t)
                    bg_g = int(bg_g * (1 - border_t) + 139 * border_t)
                    bg_b = int(bg_b * (1 - border_t) + 255 * border_t)
                    alpha = int(255 * (1 - border_t * 0.3))
                else:
                    alpha = 255
                
                # 声波图案（三个弧形）
                angle = math.atan2(dy, dx)
                for wave_r in [r*0.25, r*0.42, r*0.58]:
                    wave_width = r * 0.05
                    if abs(dist - wave_r) < wave_width and -math.pi/3 < angle < math.pi/3:
                        blend = 1 - abs(dist - wave_r) / wave_width
                        bg_r = int(bg_r * (1 - blend * 0.8) + 255 * blend * 0.8)
                        bg_g = int(bg_g * (1 - blend * 0.8) + 255 * blend * 0.8)
                        bg_b = int(bg_b * (1 - blend * 0.8) + 255 * blend * 0.8)
                
                pixels[y][x] = [
                    max(0, min(255, bg_r)),
                    max(0, min(255, bg_g)),
                    max(0, min(255, bg_b)),
                    alpha
                ]
    
    return pixels

sizes = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192,
}

base = r'd:\AI\TXAIUSE\SoundClickApp\app\src\main\res'

for folder, size in sizes.items():
    pixels = generate_icon(size)
    png_data = create_png(size, size, pixels)
    
    for name in ['ic_launcher.png', 'ic_launcher_round.png']:
        path = os.path.join(base, folder, name)
        with open(path, 'wb') as f:
            f.write(png_data)
    
    print(f"生成 {folder}/{size}x{size} 图标完成")

print("所有图标生成完成！")
