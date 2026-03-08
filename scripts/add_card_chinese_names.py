#!/usr/bin/env python3
"""
为Slay the Spire 2卡牌添加中文名aliases
"""

import os
import re
from pathlib import Path

# 卡牌中文名映射表（基于官方中文翻译）
CARD_NAMES = {
    # 铁甲战士卡牌
    "Corruption": "腐化",
    "Dark Embrace": "黑暗之拥",
    "Feel No Pain": "无惧疼痛",
    "Burning Pact": "燃烧契约",
    "Fiend Fire": "恶魔之火",
    "Inflame": "燃烧",
    "Demon Form": "恶魔形态",
    "Limit Break": "突破极限",
    "Spot Weakness": "观察弱点",
    "Shrug It Off": "耸肩无视",
    "Ghostly Armor": "幽灵铠甲",
    "Barricade": "壁垒",
    "Entrench": "巩固",
    "Body Slam": "全身撞击",
    "Combust": "自燃",
    "Rupture": "撕裂",
    "Hemokinesis": "御血术",
    "Reaper": "死亡收割",
    "Blood for Blood": "以血还血",
    "Clash": "交锋",
    "Thunderclap": "霹雳",
    "Anger": "愤怒",
    "Bash": "痛击",
    "Strike": "打击",
    "Defend": "防御",
    "True Grit": "坚毅",
    "Battle Trance": "战斗专注",
    "Offering": "祭品",
    "Heavy Blade": "重刃",
    "Sword Boomerang": "飞剑回旋镖",
    "Feed": "狂宴",
    "Brutality": "残暴",
    "Charon's Ashes": "卡戎之灰",

    # 静默猎手卡牌
    "Deadly Poison": "致命毒药",
    "Bouncing Flask": "弹跳药瓶",
    "Noxious Fumes": "毒雾",
    "Envenom": "涂毒",
    "Accelerant": "促进剂",
    "Catalyst": "催化剂",
    "Blade Dance": "刀刃之舞",
    "Infinite Blades": "无限刀刃",
    "Cloak and Dagger": "斗篷与匕首",
    "Storm of Steel": "钢铁风暴",
    "Accuracy": "精准",
    "Fan of Knives": "飞刀",
    "Phantom Blades": "幻影之刃",
    "Eviscerate": "内脏切除",
    "Reflex": "本能反应",
    "Tactician": "战术大师",
    "Sneaky Strike": "隐秘打击",
    "Backflip": "后空翻",
    "Footwork": "灵动步法",
    "After Image": "余像",
    "Blur": "模糊",
    "Dodge and Roll": "闪躲翻滚",
    "Survivor": "生存者",
    "Neutralize": "中和",
    "Grand Finale": "华丽收场",
    "Riddle with Holes": "千穿百刺",
    "Setup": "部署",
    "Prepared": "早有准备",
    "Dagger Throw": "投掷匕首",
    "Dagger Spray": "匕首雨",
    "Calculated Gamble": "计算下注",
    "Predator": "猎杀者",
    "Bane": "灾祸",
    "Flying Knee": "飞膝",
    "Quick Slash": "快斩",
    "Cut": "切割",
    "Sudden Strike": "突然一拳",
    "Sneaky Strike": "隐秘打击",
    "Glass Blade": "玻璃刀刃",
    "Die Die Die": "死吧死吧死吧",
    "Unload": "乾坤一掷",
    "All Out Attack": "全力攻击",
    "Backstab": "背刺",
    "Heel Hook": "足跟勾",
    "Finisher": "终结技",
    "Choke": "勒脖",
    "Dash": "冲刺",
    "Endless Agony": "无尽苦痛",
    "Deflect": "偏折",
    "Strike": "打击",
    "Defend": "防御",

    # 故障机器人卡牌
    "Ball Lightning": "球状闪电",
    "Cold Snap": "寒流",
    "Darkness": "黑暗",
    "Chaos": "混乱",
    "Dualcast": "双重施放",
    "Consume": "吞噬",
    "Capacitor": "电容器",
    "Inserter": "插入器",
    "Biased Cognition": "偏差认知",
    "Defragment": "碎片整理",
    "Core Surge": "核心涌流",
    "Electrostatic Field": "静电场",
    "Thunder Strike": "雷霆打击",
    "Storm": "风暴",
    "Glacier": "冰川",
    "Coolheaded": "冷静头脑",
    "Chill": "寒冷",
    "Loop": "循环",
    "Consuming Shadow": "吞噬暗影",
    "Amplify": "放大",
    "Multi-Cast": "多重施放",
    "Rainbow": "彩虹",
    "Fusion": "聚变",
    "Meteor Strike": "流星打击",
    "Tempest": "暴风雪",
    "Compile Driver": "编译驱动",
    "Skim": "略读",
    "Hyperbeam": "超光束",
    "Sunder": "分裂",
    "Zap": "电击",
    "Strike": "打击",
    "Defend": "防御",
    "Barrage": "弹幕",
    "Static Discharge": "静电释放",
    "Rebound": "反弹",
    "Hologram": "全息图",
    "Recycle": "回收",
    "Redo": "重做",
    "Steam": "蒸汽",
    "TURBO": "涡轮增压",
    "Undo": "撤销",
    "White Noise": "白噪声",
    "Reinforced Body": "强化躯体",
    "Equilibrium": "平衡",
    "Genetic Algorithm": "基因算法",
    "Buffer": "缓冲",
    "Machine Learning": "机器学习",
    "Creative AI": "创造性AI",
    "Echo Form": "回声形态",
    "Self Repair": "自我修复",

    # 储君卡牌
    "Alignment": "对齐",
    "Glow": "辉光",
    "Solar Strike": "太阳打击",
    "Gather Light": "聚光",
    "Genesis": "创世纪",
    "The Sealed Throne": "封印王座",
    "Refine Blade": "精炼之刃",
    "Summon Forth": "召唤",
    "Conqueror": "征服者",
    "Bulwark": "壁垒",
    "Furnace": "熔炉",
    "The Smith": "铁匠",
    "Sovereign Blade": "王权之剑",
    "Seeking Edge": "寻刃",
    "Sword Sage": "剑圣",
    "Parry": "招架",
    "Child of the Stars": "星辰之子",
    "Black Hole": "黑洞",
    "Orbit": "轨道",
    "Astral Pulse": "星脉冲",
    "Meteor Shower": "流星雨",
    "Comet": "彗星",
    "Gamma Blast": "伽马爆裂",
    "Decisions, Decisions": "抉择",
    "Particle Wall": "粒子墙",
    "Pale Blue Dot": "暗淡蓝点",
    "Arsenal": "军械库",
    "Spectrum Shift": "光谱转移",
    "Manifest Authority": "权威显现",
    "Bundle of Joy": "欢乐束",
    "Heirloom Hammer": "传家宝锤",
    "Dying Star": "垂死之星",
    "Crash Landing": "坠毁",
    "Seven Stars": "七星",
    "Crush Under": "碾碎",
    "Resonance": "共鸣",
    "Kingly Kick": "王者踢",
    "Monarch's Gaze": "君主凝视",
    "Void Form": "虚空形态",
    "Royalties": "王权",
    "Venerate": "崇敬",
    "Strike": "打击",
    "Defend": "防御",
    "Falling Star": "陨星",
    "Cloak of Stars": "星辰斗篷",
    "Big Bang": "大爆炸",
    "Star Potion": "星辰药水",

    # 死灵契约师卡牌
    "Scourge": "天灾",
    "Blight Strike": "荒疫打击",
    "Deathbringer": "死亡使者",
    "Countdown": "倒计时",
    "End of Days": "末日",
    "No Escape": "无处可逃",
    "Oblivion": "遗忘",
    "Capture Spirit": "捕获灵魂",
    "Reave": "掠夺",
    "Glimpse Beyond": "窥视彼岸",
    "Grave Warden": "墓地守卫",
    "Devour Life": "吞噬生命",
    "Haunt": "萦绕",
    "Soul Storm": "灵魂风暴",
    "Dirge": "挽歌",
    "Necromastery": "死灵精通",
    "Legion": "军团",
    "Raise Dead": "复活死者",
    "Resurrect": "复活",
    "Bury": "埋葬",
    "Banshee's Cry": "女妖之嚎",
    "Borrowed Time": "借来的时间",
    "Reaper Form": "收割者形态",
    "Death's Door": "死亡之门",
    "Negative Pulse": "负脉冲",
    "Blight": "枯萎",
    "Strike": "打击",
    "Defend": "防御",
    "Pot of Ghouls": "食尸鬼之锅",
    "Potion of Doom": "厄运药水",
    "Bone Brew": "骨酿",
    "Undeath": "亡灵",
    "Legion of Bone": "骨军团",

    # 无色卡牌
    "Dramatic Entrance": "戏剧性登场",
    "Finesse": "技巧",
    "Flash of Steel": "钢铁闪光",
    "Mind Blast": "心灵冲击",
    "Swift Strike": "迅捷打击",
    "Thinking Ahead": "提前思考",
    "Hand of Greed": "贪婪之手",
    "Magnetism": "磁性",
    "Master of Strategy": "战略大师",
    "Panache": "华丽",
    "Purity": "纯净",
    "Secret Technique": "秘技",
    "Secret Weapon": "秘密武器",
    "The Bomb": "炸弹",
    "Vampiric Touch": "吸血鬼之触",
    "Apotheosis": "神化",
    "Chrysalis": "蛹",
    "Discovery": "发现",
    "Enlightenment": "启蒙",
    "Fame and Fortune": "名利",
    "Forethought": "深谋远虑",
    "Madness": "疯狂",
    "Metamorphosis": "变形",
    "Panacea": "万能药",
    "Transmutation": "转化",
    "Violence": "暴力",
    "Apparition": "幽灵",
    "Beta": "测试版",
    "Insight": "洞察",
    "J.A.X.": "J.A.X.",
    "Live Forever": "永生",
    "Miracle": "奇迹",
    "Safety": "安全",
    "Shiv": "匕首",
    "Smile": "微笑",
    "Through Violence": "通过暴力",
}

def add_alias_to_card(card_path, chinese_name):
    """为卡牌文件添加中文alias"""
    try:
        with open(card_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已有aliases
        if 'aliases::' in content:
            return False, "Already has aliases"

        # 在frontmatter中添加aliases
        lines = content.split('\n')
        new_lines = []
        in_frontmatter = False
        frontmatter_end = 0

        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    # Frontmatter结束，插入aliases
                    new_lines.append(f'aliases:: ["{chinese_name}"]')
                    frontmatter_end = i
                    in_frontmatter = False
            new_lines.append(line)

        new_content = '\n'.join(new_lines)

        with open(card_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, "Added alias"
    except Exception as e:
        return False, str(e)

def main():
    base_path = Path("/Users/lzw/Documents/LobsterAI/HammerChain/SlayTheSpire2/02-卡牌")

    success_count = 0
    fail_count = 0
    not_found = []

    for card_name, chinese_name in CARD_NAMES.items():
        # 查找卡牌文件
        card_file = base_path / f"{card_name}.md"

        # 如果直接找不到，尝试递归查找
        if not card_file.exists():
            found = False
            for subdir in base_path.iterdir():
                if subdir.is_dir():
                    potential_file = subdir / f"{card_name}.md"
                    if potential_file.exists():
                        card_file = potential_file
                        found = True
                        break
            if not found:
                not_found.append(card_name)
                continue

        success, msg = add_alias_to_card(card_file, chinese_name)
        if success:
            success_count += 1
            print(f"✓ {card_name} -> {chinese_name}")
        else:
            fail_count += 1
            print(f"✗ {card_name}: {msg}")

    print(f"\n完成: {success_count} 成功, {fail_count} 失败, {len(not_found)} 未找到")
    if not_found:
        print(f"未找到的卡牌: {', '.join(not_found[:10])}{'...' if len(not_found) > 10 else ''}")

if __name__ == "__main__":
    main()
