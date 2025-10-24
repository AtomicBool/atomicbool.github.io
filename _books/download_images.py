import os
import re
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# 直接引用豆瓣链接会出问题故写了这个脚本

def process_md_file(md_file):
    """处理单个Markdown文件-下载封面并更新链接"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取封面URL
    cover_match = re.search(r'cover:\s*(https?://[^\s]+)', content)
    if not cover_match:
        print(f"⚠️ 未找到封面URL: {md_file}")
        return
    
    cover_url = cover_match.group(1)
    base_name = Path(md_file).stem
    
    try:
        # 下载图片
        response = requests.get(cover_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        # 转换为JPG格式
        img = Image.open(BytesIO(response.content))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 保存为JPG（直接保存在当前目录）
        output_path = f"{base_name}.jpg"
        img.save(output_path, "JPEG", quality=90)
        
        # 更新Markdown内容中的链接路径
        new_cover = f"cover: /assets/img/book_covers/{base_name}.jpg"
        new_content = re.sub(r'cover:\s*https?://[^\s]+', new_cover, content)
        
        # 写回文件
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 处理成功: {md_file}")
        print(f"   下载: {cover_url} -> {output_path}")
        print(f"   更新: {new_cover}")
        
    except Exception as e:
        print(f"❌ 处理失败: {md_file} | 错误: {str(e)}")

def main():
    # 获取当前目录所有Markdown文件
    md_files = [f for f in os.listdir() if f.endswith('.md')]
    
    if not md_files:
        print("未找到Markdown文件")
        return
    
    print(f"找到 {len(md_files)} 个Markdown文件")
    for md_file in md_files:
        print(f"\n处理: {md_file}")
        process_md_file(md_file)

if __name__ == "__main__":
    main()