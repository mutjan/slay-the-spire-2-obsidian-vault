#!/usr/bin/env python3
"""
为卡牌效果描述中的机制关键词添加双向链接
"""

import re
from pathlib import Path

# 定义替换规则列表，按优先级排序
# 格式: (匹配模式, 替换文本, 是否保留原始形式)
REPLACEMENT_RULES = [
    # 1. 组合词（优先匹配）
    (r'\bOrb Slot\b', '[[充能球槽|Orb Slot]]', False),
    (r'\bMinion Strikes\b', '[[Minion Strike|Minion Strikes]]', False),
    (r'\bMinion Strike\b', '[[Minion Strike]]', False),
    (r'\bMinion Sacrifice\b', '[[Minion Sacrifice]]', False),
    (r'\bSovereign Blade\b', '[[Sovereign Blade]]', False),
    (r'\bSweeping Gaze\b', '[[Sweeping Gaze]]', False),
    (r'\bGiant Rock\b', '[[Giant Rock]]', False),

    # 2. 衍生牌
    (r'\bShivs\b', '[[Shiv|Shivs]]', False),
    (r'\bShiv\b', '[[Shiv]]', False),
    (r'\bSouls\b', '[[Soul|Souls]]', False),
    (r'\bSoul\b', '[[Soul]]', False),
    (r'\bSword\b', '[[Sword]]', False),
    (r'\bBurn\b', '[[Burn]]', False),
    (r'\bDazed\b', '[[Dazed]]', False),
    (r'\bWound\b', '[[Wound]]', False),
    (r'\bSlimed\b', '[[Slimed]]', False),
    (r'\bVoid\b', '[[Void]]', False),

    # 3. 充能球相关
    (r'\bLightning\b', '[[闪电球|Lightning]]', False),
    (r'\bFrost\b', '[[冰霜球|Frost]]', False),
    (r'\bDark\b', '[[黑暗球|Dark]]', False),
    (r'\bPlasma\b', '[[等离子球|Plasma]]', False),
    (r'\bGlass\b', '[[玻璃球|Glass]]', False),
    (r'\bChannel\b', '[[充能|Channel]]', False),
    (r'\bEvoke\b', '[[激发|Evoke]]', False),
    (r'\bFocus\b', '[[集中|Focus]]', False),
    (r'\bOrb\b', '[[充能球|Orb]]', False),

    # 4. 基础状态
    (r'\bBlock\b', '[[格挡|Block]]', False),
    (r'\bStrength\b', '[[力量|Strength]]', False),
    (r'\bDexterity\b', '[[敏捷|Dexterity]]', False),
    (r'\bVulnerable\b', '[[易伤|Vulnerable]]', False),
    (r'\bWeak\b', '[[虚弱|Weak]]', False),
    (r'\bFrail\b', '[[脆弱|Frail]]', False),
    (r'\bPoison\b', '[[毒素|Poison]]', False),

    # 5. STS2 新机制
    (r'\bDoom\b', '[[厄运|Doom]]', False),
    (r'\bSummon\b', '[[召唤|Summon]]', False),
    (r'\bForge\b', '[[锻造|Forge]]', False),

    # 6. 卡牌特性
    (r'\bExhaust\b', '[[消耗|Exhaust]]', False),
    (r'\bEthereal\b', '[[虚无|Ethereal]]', False),
    (r'\bRetain\b', '[[保留|Retain]]', False),
    (r'\bSly\b', '[[狡猾|Sly]]', False),
    (r'\bUnplayable\b', '[[不可打出|Unplayable]]', False),
    (r'\bInnate\b', '[[固有|Innate]]', False),

    # 7. 其他机制
    (r'\bPlating\b', '[[护甲|Plating]]', False),
    (r'\bIntangible\b', '[[无形|Intangible]]', False),
    (r'\bThorns\b', '[[荆棘|Thorns]]', False),
    (r'\bVigor\b', '[[活力|Vigor]]', False),
    (r'\bArtifact\b', '[[神器|Artifact]]', False),
    (r'\bBuffer\b', '[[缓冲|Buffer]]', False),
    (r'\bTransform\b', '[[转化|Transform]]', False),
    (r'\bUpgrade\b', '[[升级|Upgrade]]', False),
    (r'\bMinion\b', '[[仆从|Minion]]', False),
    (r'\bOsty\b', '[[奥斯蒂|Osty]]', False),
]


def add_links_to_effect(text: str) -> str:
    """为效果描述文本添加机制链接"""

    # 保存已有的 wiki 链接
    preserved_links = []
    def save_link(match):
        preserved_links.append(match.group(0))
        return f"\x00LINK{len(preserved_links)-1}\x00"

    # 保护已有的 wiki 链接
    text = re.sub(r'\[\[.*?\]\]', save_link, text)

    # 按顺序应用替换规则
    for pattern, replacement, _ in REPLACEMENT_RULES:
        text = re.sub(pattern, replacement, text)

    # 恢复被保护的链接
    def restore_link(match):
        idx = int(match.group(1))
        return preserved_links[idx] if idx < len(preserved_links) else match.group(0)

    text = re.sub(r'\x00LINK(\d+)\x00', restore_link, text)

    return text


def process_card_file(file_path: Path) -> bool:
    """处理单个卡牌文件"""

    try:
        content = file_path.read_text(encoding='utf-8')

        # 找到效果描述部分
        effect_pattern = r'(## 效果描述\n\n)(.*?)(\n\n##)'
        match = re.search(effect_pattern, content, re.DOTALL)

        if match:
            effect_section = match.group(2)
            new_effect = add_links_to_effect(effect_section)

            if new_effect != effect_section:
                # 替换效果描述
                content = content[:match.start(2)] + new_effect + content[match.end(2):]

                # 写回文件
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
