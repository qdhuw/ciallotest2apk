"""将 SoundClickApp 项目打包成 zip"""
import zipfile
import os

project_dir = r'd:\AI\TXAIUSE\SoundClickApp'
output_zip = r'd:\AI\TXAIUSE\SoundClickApp.zip'

skip_dirs = {'build', '.gradle', '.idea', '__pycache__'}

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(project_dir):
        # 跳过不需要的目录
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, os.path.dirname(project_dir))
            zf.write(file_path, arcname)
            print(f"  + {arcname}")

print(f"\n打包完成: {output_zip}")
print(f"文件大小: {os.path.getsize(output_zip) / 1024:.1f} KB")
