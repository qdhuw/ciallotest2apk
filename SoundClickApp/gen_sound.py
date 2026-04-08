import struct
import math
import os

def write_wav(filename, sample_rate=44100, duration=0.15, freq=800, decay=8.0):
    """生成一个短促的点击音效 WAV 文件"""
    num_samples = int(sample_rate * duration)
    
    # WAV 文件头
    data_size = num_samples * 2  # 16-bit samples
    
    with open(filename, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))       # chunk size
        f.write(struct.pack('<H', 1))        # PCM format
        f.write(struct.pack('<H', 1))        # mono
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))  # byte rate
        f.write(struct.pack('<H', 2))        # block align
        f.write(struct.pack('<H', 16))       # bits per sample
        
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        
        # 生成混合音效（基频 + 谐波 + 快速衰减）
        for i in range(num_samples):
            t = i / sample_rate
            envelope = math.exp(-decay * t)
            
            # 混合多个谐波，更有金属感
            sample = (
                0.5 * math.sin(2 * math.pi * freq * t) +
                0.3 * math.sin(2 * math.pi * freq * 2 * t) +
                0.15 * math.sin(2 * math.pi * freq * 3 * t) +
                0.05 * math.sin(2 * math.pi * freq * 5 * t)
            )
            
            value = int(sample * envelope * 28000)
            value = max(-32768, min(32767, value))
            f.write(struct.pack('<h', value))

output_path = r'd:\AI\TXAIUSE\SoundClickApp\app\src\main\res\raw\click_sound.wav'
write_wav(output_path)
print(f"WAV 文件生成完成: {output_path}")
print(f"文件大小: {os.path.getsize(output_path)} bytes")
