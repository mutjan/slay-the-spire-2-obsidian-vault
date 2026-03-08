#!/usr/bin/env python3
"""
为 YAML frontmatter 中的双向链接添加引号
type:: [[技能牌]] -> type:: "[[技能牌]]"
"""

import re
from pathlib import Path


def process_card_file(file_path: Path) -> bool:
    """处理单个卡牌文件，为 YAML 中的链接添加引号"""

    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # 匹配 YAML frontmatter 中的双向链接字段
        # 匹配 pattern: field:: [[链接]] 或 field:: [[链接|显示文本]]
        def add_quotes(match):
            field = match.group(1)
            value = match.group(2)
            # 如果已经有引号，跳过
            if value.strip().startswith('"') or value.strip().startswith("'"):
                return match.group(0)
            return f'{field}:: "{value.strip()}"'

        # 只处理 YAML frontmatter 部分（--- 之间的内容）
        yaml_pattern = r'^(---\n)(.*?)(\n---)'

        def fix_yaml_quotes(match):
            yaml_start = match.group(1)
            yaml_content = match.group(2)
            yaml_end = match.group(3)

            # 为 YAML 中的链接值添加引号
            # 匹配 field:: [[...]] 或 field:: value
            fixed_content = re.sub(
                r'^(\w+)::\s*(\[\[.*?\]\].*)$',
                r'\1:: "\2"',
                yaml_content,
                flags=re.MULTILINE
            )

            return yaml_start + fixed_content + yaml_end

        content = re.sub(yaml_pattern, fix_yaml_quotes, content, flags=re.DOTALL)

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
