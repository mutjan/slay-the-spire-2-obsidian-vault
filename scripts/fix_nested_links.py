#!/usr/bin/env python3
"""
修复嵌套的 wiki 链接
"""

import re
from pathlib import Path


def fix_nested_links(text: str) -> str:
    """修复嵌套的 [[[[xxx]]|yyy]] 格式为 [[xxx|yyy]]"""

    # 匹配模式: [[[[内容]]|显示文本]] -> [[内容|显示文本]]
    # 处理多层嵌套
    pattern = r'\[\[\[\[(.*?)\]\]\|(.*?)\]\]'

    while re.search(pattern, text):
        text = re.sub(pattern, r'[[\1|\2]]', text)

    # 处理更深层嵌套: [[[[[[内容]]]]|显示文本]]
    pattern2 = r'\[\[\[\[\[\[(.*?)\]\]\]\]\|(.*?)\]\]'
    while re.search(pattern2, text):
        text = re.sub(pattern2, r'[[\1|\2]]', text)

    return text


def process_file(file_path: Path) -> bool:
    """处理单个文件"""

    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # 修复嵌套链接
        content = fix_nested_links(content)

        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """主函数"""
    vault_path = Path('/Users/lzw/Documents/LobsterAI/HammerChain/SlayTheSpire2')
    cards_path = vault_path / '02-卡牌'

    modified = 0

    # 遍历所有卡牌文件
    for card_file in cards_path.rglob('*.md'):
        if process_file(card_file):
            modified += 1
            print(f"Fixed: {card_file.relative_to(vault_path)}")

    print(f"\n总计: 修复 {modified} 个文件")


if __name__ == '__main__':
    main()
