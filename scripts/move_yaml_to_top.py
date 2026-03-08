#!/usr/bin/env python3
"""
将卡牌文件中的 YAML 数据字段移到文件顶部作为 frontmatter
"""

import re
from pathlib import Path


def process_card_file(file_path: Path) -> bool:
    """处理单个卡牌文件，将 YAML 移到顶部"""

    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # 提取 YAML 块
        yaml_pattern = r'## 数据字段\n\n```yaml\n(.*?)```'
        yaml_match = re.search(yaml_pattern, content, re.DOTALL)

        if not yaml_match:
            return False

        yaml_content = yaml_match.group(1).strip()

        # 移除旧的 YAML 部分
        content = re.sub(r'\n\n## 数据字段\n\n```yaml\n.*?```', '', content, flags=re.DOTALL)

        # 构建新的 frontmatter
        frontmatter = f"---\n{yaml_content}\n---\n\n"

        # 在标题后插入 frontmatter
        # 找到第一个 # 标题
        title_match = re.match(r'(# .*\n)', content)
        if title_match:
            title_end = title_match.end()
            content = content[:title_end] + "\n" + frontmatter + content[title_end:]
        else:
            # 如果没有标题，在开头添加
            content = frontmatter + content

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
