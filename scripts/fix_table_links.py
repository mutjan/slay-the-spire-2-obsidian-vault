#!/usr/bin/env python3
"""
修复 Markdown 表格中的 Obsidian 链接语法
将 [[CardName|中文名]] 改为 [[CardName]]，依赖 aliases 自动解析
"""

import re
from pathlib import Path

def fix_table_links_in_file(file_path):
    """修复文件中的表格链接"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content

    # 匹配表格行中的 [[原名|别名]] 链接
    # 表格行以 | 开头
    def fix_table_line(match):
        line = match.group(0)
        # 替换所有 [[原名|别名]] 为 [[原名]]
        fixed_line = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'[[\1]]', line)
        return fixed_line

    # 匹配表格行（以 | 开头的行）
    content = re.sub(r'^\|.*$', fix_table_line, content, flags=re.MULTILINE)

    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        # 计算修改数量
        original_links = len(re.findall(r'\[\[[^\]|]+\|[^\]]+\]\]', original_content))
        return original_links
    return 0

def main():
    base_path = Path('/Users/lzw/Documents/LobsterAI/HammerChain/SlayTheSpire2')

    # 处理所有抓牌攻略文件
    guide_files = [
        base_path / '05-导航' / '铁甲战士抓牌攻略.md',
        base_path / '05-导航' / '静默猎手抓牌攻略.md',
        base_path / '05-导航' / '故障机器人抓牌攻略.md',
        base_path / '05-导航' / '死灵法师抓牌攻略.md',
        base_path / '05-导航' / '摄政王抓牌攻略.md',
    ]

    total_fixed = 0
    for file_path in guide_files:
        if file_path.exists():
            fixed = fix_table_links_in_file(file_path)
            print(f"✓ {file_path.name}: 修复了 {fixed} 处表格链接")
            total_fixed += fixed
        else:
            print(f"✗ 文件不存在: {file_path}")

    print(f"\n总共修复了 {total_fixed} 处表格链接")

if __name__ == '__main__':
    main()
