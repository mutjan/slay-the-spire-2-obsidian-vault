#!/usr/bin/env python3
"""
移除卡牌文件中的一级标题（# Title），因为文件名已经包含该信息
使 YAML frontmatter 成为文件的第一部分
"""

import re
from pathlib import Path


def process_card_file(file_path: Path) -> bool:
    """处理单个卡牌文件，移除一级标题"""

    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # 移除文件开头的一级标题（# Title）
        # 匹配模式: 文件开头或换行后的 # 标题行
        content = re.sub(r'^(# .+\n)\n*', '', content)

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

    processed = 0
    modified = 0

    # 遍历所有卡牌文件
    for card_file in cards_path.rglob('*.md'):
        processed += 1
        if process_card_file(card_file):
            modified += 1
            print(f"Modified: {card_file.relative_to(vault_path)}")

    print(f"\n总计: 处理 {processed} 个文件, 修改 {modified} 个文件")


if __name__ == '__main__':
    main()
