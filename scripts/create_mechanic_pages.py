#!/usr/bin/env python3
"""
为效果描述中的机制关键词和衍生牌创建文件
文件名使用英文，YAML别名使用中文
"""

from pathlib import Path

# 机制关键词映射: 英文文件名 -> (中文别名, 描述)
MECHANIC_PAGES = {
    # 基础状态
    "Block": ("格挡", "阻挡即将到来的伤害。在下一回合开始时会消失。"),
    "Strength": ("力量", "增加攻击造成的伤害。每点力量增加1点伤害。"),
    "Dexterity": ("敏捷", "增加从卡牌获得的格挡值。每点敏捷增加1点格挡。"),
    "Vulnerable": ("易伤", "受到的攻击伤害增加50%。持续一定回合。"),
    "Weak": ("虚弱", "造成的攻击伤害减少25%。持续一定回合。"),
    "Frail": ("脆弱", "从卡牌获得的格挡减少25%。持续一定回合。"),
    "Poison": ("毒素", "在回合开始时造成伤害，然后减少1点。无视格挡。"),

    # STS2 新机制
    "Doom": ("厄运", "累积型持续伤害，达到阈值触发即死效果。"),
    "Soul": ("灵魂", "死灵契约师的特殊0费消耗牌。"),
    "Summon": ("召唤", "召唤仆从协助战斗。"),
    "Forge": ("锻造", "储君的特殊机制，永久强化王权之剑的伤害。"),
    "Star": ("聚焦", "储君的特殊资源，用于触发各种效果。"),

    # 卡牌特性
    "Exhaust": ("消耗", "打出后从本场战斗中移除，进入消耗牌堆。"),
    "Ethereal": ("虚无", "如果在手牌中未被打出，在回合结束时被消耗。"),
    "Retain": ("保留", "回合结束时不会自动丢弃。"),
    "Sly": ("狡猾", "静默猎手专属特性，某些效果与此相关。"),
    "Unplayable": ("不可打出", "无法从手牌中打出。"),
    "Innate": ("固有", "战斗开始时就放入手牌。"),

    # 充能球
    "Orb": ("充能球", "故障机器人的核心机制，提供各种持续效果。"),
    "Lightning": ("闪电球", "充能球类型，被动：回合结束时对随机敌人造成伤害。激发：对所有敌人造成伤害。"),
    "Frost": ("冰霜球", "充能球类型，被动：回合结束时获得格挡。激发：获得大量格挡。"),
    "Dark": ("黑暗球", "充能球类型，被动：回合结束时伤害增加。激发：对生命值最低的敌人造成伤害。"),
    "Plasma": ("等离子球", "充能球类型，被动：回合开始时获得能量。激发：获得能量。"),
    "Glass": ("玻璃球", "充能球类型，被动：回合结束时获得临时力量。激发：获得临时力量。"),
    "Channel": ("充能", "生成一个充能球放入充能球槽。"),
    "Evoke": ("激发", "触发充能球的激发效果并移除该球。"),
    "Focus": ("集中", "增加充能球的被动和激发效果强度。"),
    "Orb_Slot": ("充能球槽", "容纳充能球的槽位。"),

    # 其他机制
    "Plating": ("护甲", "类似格挡，但不会随回合消失。受到伤害时优先消耗。"),
    "Intangible": ("无形", "受到的所有伤害变为1点。"),
    "Thorns": ("荆棘", "受到攻击时，对攻击者造成固定伤害。"),
    "Vigor": ("活力", "下一次攻击造成额外伤害。"),
    "Artifact": ("神器", "免疫下一次受到的负面效果。"),
    "Buffer": ("缓冲", "免疫下一次受到的生命值损失。"),
    "Transform": ("转化", "将卡牌变为随机其他卡牌。"),
    "Upgrade": ("升级", "强化卡牌的效果。"),
    "Minion": ("仆从", "死灵契约师召唤的生物，可以协助战斗。"),
    "Osty": ("奥斯蒂", "死灵契约师的专属仆从。"),

    # 衍生牌
    "Shiv": ("匕首", "静默猎手的0费攻击牌，造成伤害。"),
    "Sword": ("剑", "储君的衍生牌。"),
    "Minion_Strike": ("仆从打击", "死灵契约师仆从的攻击牌。"),
    "Minion_Sacrifice": ("仆从牺牲", "牺牲仆从产生效果的牌。"),
    "Giant_Rock": ("巨石", "铁甲战士的衍生牌，造成大量伤害。"),
    "Burn": ("灼伤", "状态牌，回合开始时造成伤害。"),
    "Dazed": ("眩晕", "状态牌，无法打出，回合结束时自动丢弃。"),
    "Wound": ("伤口", "状态牌，无法打出。"),
    "Slimed": ("黏液", "状态牌，1费消耗。"),
    "Void": ("虚空", "状态牌，无法打出，抽到时会消耗能量。"),
    "Sovereign_Blade": ("王权之剑", "储君的核心武器牌，可通过锻造升级。"),
    "Sweeping_Gaze": ("扫视", "储君的衍生牌。"),
}


def create_mechanic_page(vault_path: Path, english_name: str, chinese_name: str, description: str):
    """创建机制关键词页面"""

    # 使用英文文件名，空格替换为下划线
    file_name = english_name.replace(" ", "_") + ".md"
    file_path = vault_path / "06-机制" / file_name

    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""---
name:: "[[{english_name}|{chinese_name}]]"
english_name:: "{english_name}"
aliases:: ["{chinese_name}"]
category:: "[[机制]]"
---

> **英文**: {english_name} | **中文**: {chinese_name}

## 描述

{description}

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
"""

    file_path.write_text(content, encoding='utf-8')
    return file_path


def main():
    """主函数"""
    vault_path = Path('/Users/lzw/Documents/LobsterAI/HammerChain/SlayTheSpire2')
    mechanics_path = vault_path / "06-机制"

    # 创建机制目录
    mechanics_path.mkdir(parents=True, exist_ok=True)

    created = 0
    for english_name, (chinese_name, description) in MECHANIC_PAGES.items():
        file_path = create_mechanic_page(vault_path, english_name, chinese_name, description)
        print(f"Created: {file_path.relative_to(vault_path)}")
        created += 1

    # 创建机制目录索引页
    index_path = mechanics_path / "机制目录.md"
    index_content = """---
name:: "[[机制目录]]"
category:: "[[导航]]"
---

# 游戏机制目录

## 基础状态

```dataview
TABLE english_name as "英文", name as "中文", description as "描述"
FROM "06-机制"
WHERE category = "[[机制]]"
SORT file.name
```

---

*返回 [[主页]]*
"""
    index_path.write_text(index_content, encoding='utf-8')
    print(f"Created: {index_path.relative_to(vault_path)}")

    print(f"\n总计: 创建 {created} 个机制页面")


if __name__ == '__main__':
    main()
