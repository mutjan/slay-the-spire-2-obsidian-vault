#!/usr/bin/env python3
"""
修复嵌套的 wiki 链接 - 更强力的版本
"""

import re
from pathlib import Path


def fix_nested_links(text: str) -> str:
    """修复各种嵌套格式"""

    # 修复: [[[[仆从|Minion]] Strike|[[仆从|Minion]] Strikes]] -> [[Minion Strike|Minion Strikes]]
    # 先处理内部链接
    pattern1 = r'\[\[([^\]]*?)\|([^\]]*?)\]\]'

    def simplify_link(match):
        # 获取显示文本部分
        display = match.group(2)
        return display

    # 重复处理直到没有变化
    prev_text = None
    while prev_text != text:
        prev_text = text
        # 处理 [[xxx|yyy]] 中的 yyy 如果包含 [[ ]] 则简化
        text = re.sub(r'\[\[([^\]]+?)\|([^\[\]]*?)\[\[([^\]]+?)\|([^\]]+?)\]\]([^\[\]]*?)\]\]',
                      r'[[\3|\4\5]]', text)

    # 处理 [[[[内容]]|显示文本]] -> [[内容|显示文本]]
    pattern2 = r'\[\[\[\[(.*?)\]\]\|(.*?)\]\]'
    while re.search(pattern2, text):
        text = re.sub(pattern2, r'[[\1|\2]]', text)

    # 处理 [[[[[[内容]]]]|显示文本]] -> [[内容|显示文本]]
    pattern3 = r'\[\[\[\[\[\[(.*?)\]\]\]\]\|(.*?)\]\]'
    while re.search(pattern3, text):
        text = re.sub(pattern3, r'[[\1|\2]]', text)

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
