#!/usr/bin/env python3
"""
更新攻略文件中的卡牌链接，添加中文别名
将 [[CardName]] 改为 [[CardName|中文名]]
"""

import re
from pathlib import Path

# 卡牌中文名映射表
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
    "Backstab": "背刺",
    "Finisher": "终结技",
    "Dash": "冲刺",
    "Deflect": "偏折",
    "Bane": "灾祸",
    "Flying Knee": "飞膝",
    "Quick Slash": "快斩",
    "Cut": "切割",
    "Sudden Strike": "突然一拳",
    "Glass Blade": "玻璃刀刃",
    "Die Die Die": "死吧死吧死吧",
    "Unload": "乾坤一掷",
    "All Out Attack": "全力攻击",
    "Heel Hook": "足跟勾",
    "Choke": "勒脖",
    "Endless Agony": "无尽苦痛",
    "Outmaneuver": "声东击西",
    "Escape Plan": "逃脱计划",
    "Expertise": "独门技术",
    "Leg Sweep": "扫腿",
    "Terror": "恐怖",
    "Crippling Cloud": "致残毒云",
    "Adrenaline": "肾上腺素",
    "Bullet Time": "子弹时间",
    "Burst": "爆发",
    "Malaise": "萎靡",
    "Nightmare": "夜魇",
    "Phantasmal Killer": "幻影杀手",
    "Storm of Steel": "钢铁风暴",
    "Alchemize": "炼制药水",
    "Distraction": "分心",
    "Jack of All Trades": "万事通",
    "Madness": "疯狂",
    "Purity": "纯净",
    "Secret Technique": "秘技",
    "Secret Weapon": "秘密武器",
    "The Bomb": "炸弹",
    "Thinking Ahead": "提前思考",
    "Violence": "暴力",
    "Apparition": "幽灵",
    "Bandage Up": "包扎",
    "Blind": "致盲",
    "Dark Shackles": "黑暗枷锁",
    "Deep Breath": "深呼吸",
    "Discovery": "发现",
    "Dramatic Entrance": "戏剧性登场",
    "Enlightenment": "启蒙",
    "Finesse": "技巧",
    "Flash of Steel": "钢铁闪光",
    "Forethought": "深谋远虑",
    "Good Instincts": "良好直觉",
    "Impatience": "急躁",
    "Jack of All Trades": "万事通",
    "Madness": "疯狂",
    "Mind Blast": "心灵冲击",
    "Panacea": "万能药",
    "Panache": "华丽",
    "Purity": "纯净",
    "Swift Strike": "迅捷打击",
    "Trip": "绊倒",

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
    "Static Discharge": "静电释放",
    "Heatsinks": "散热器",
    "Hello World": "你好世界",
    "Force Field": "力场",
    "Auto Shields": "自动护盾",
    "Boot Sequence": "启动序列",
    "Chaos": "混乱",
    "Charge Battery": "充电电池",
    "Doom and Gloom": "悲观失望",
    "Double Energy": "双倍能量",
    "Dualcast": "双重施放",
    "Fission": "裂变",
    "FTL": "超光速",
    "Go for the Eyes": "直击眼睛",
    "Overclock": "超频",
    "Recycle": "回收",
    "Scrape": "刮削",
    "Sunder": "分裂",
    "Sweeping Beam": "横扫光束",
    "Beam Cell": "光束细胞",
    "Claw": "利爪",
    "Rebound": "反弹",
    "Rip and Tear": "撕裂",
    "Streamline": "流线型",
    "All for One": "孤注一掷",
    "Core Surge": "核心涌流",
    "Hyperbeam": "超光束",
    "Meteor Strike": "流星打击",
    "Thunder Strike": "雷霆打击",
    "Biased Cognition": "偏差认知",
    "Buffer": "缓冲",
    "Creative AI": "创造性AI",
    "Echo Form": "回声形态",
    "Electrodynamics": "电动力学",
    "Machine Learning": "机器学习",

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
    "Falling Star": "陨星",
    "Cloak of Stars": "星辰斗篷",
    "Big Bang": "大爆炸",
    "Star Potion": "星辰药水",

    # 死灵契约师卡牌
    "Scourge": "鞭打",
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
    "Pot of Ghouls": "食尸鬼之锅",
    "Potion of Doom": "厄运药水",
    "Bone Brew": "骨酿",
    "Undeath": "亡灵",
    "Legion of Bone": "骨军团",
}

def update_links_in_file(file_path, card_names):
    """更新文件中的卡牌链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        updated_count = 0

        # 对每个卡牌名进行替换
        for card_name, chinese_name in card_names.items():
            # 匹配 [[CardName]] 但不匹配 [[CardName|中文名]]
            pattern = rf'\[\[{re.escape(card_name)}\]\](?!\|)'
            replacement = f'[[{card_name}|{chinese_name}]]'

            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                updated_count += count

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, updated_count
        else:
            return False, 0

    except Exception as e:
        return False, str(e)

def main():
    guide_dir = Path("/Users/lzw/Documents/LobsterAI/HammerChain/SlayTheSpire2/05-导航")

    guides = [
        "铁甲战士抓牌攻略.md",
        "静默猎手抓牌攻略.md",
        "故障机器人抓牌攻略.md",
        "死灵法师抓牌攻略.md",
        "摄政王抓牌攻略.md",
    ]

    total_updated = 0

    for guide_name in guides:
        guide_path = guide_dir / guide_name
        if guide_path.exists():
            success, count = update_links_in_file(guide_path, CARD_NAMES)
            if success:
                print(f"✓ {guide_name}: 更新了 {count} 处链接")
                total_updated += count
            elif isinstance(count, int) and count == 0:
                print(f"- {guide_name}: 无需更新")
            else:
                print(f"✗ {guide_name}: 错误 - {count}")
        else:
            print(f"✗ {guide_name}: 文件不存在")

    print(f"\n总共更新了 {total_updated} 处链接")

if __name__ == "__main__":
    main()
