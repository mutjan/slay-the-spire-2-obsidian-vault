#!/usr/bin/env python3
"""
Slay The Spire 2 机制关键词费用模型分析
扩展分析：Strength, Dexterity, Exhaust, Ethereal, Retain, Innate, Channel, Evoke, Orb等
"""

import json
import re
import statistics
from collections import defaultdict

def load_cards(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_energy(energy_str):
    if energy_str in ['X', '']:
        return None
    try:
        return int(energy_str)
    except:
        return None

def extract_number(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def extract_damage(description):
    return extract_number(description, [r'Deal (\d+) damage'])

def extract_block(description):
    return extract_number(description, [r'Gain (\d+) Block'])

def extract_draw(description):
    return extract_number(description, [r'Draw (\d+) cards?'])

def analyze_mechanics(cards):
    """分析各种机制关键词的费用模型"""

    # 基础模型（已知的）
    DAMAGE_PER_ENERGY = 7.0
    BLOCK_PER_ENERGY = 6.0

    # 机制分类存储
    mechanics = {
        # 属性增益
        'strength': [],      # 力量
        'dexterity': [],     # 敏捷
        'focus': [],         # 集中

        # 负面状态施加
        'vulnerable': [],    # 易伤
        'weak': [],          # 虚弱
        'poison': [],        # 中毒
        'frail': [],         # 脆弱

        # 特殊机制
        'exhaust': {'with_damage': [], 'with_block': [], 'only': [], 'draw': []},
        'ethereal': [],
        'retain': [],
        'innate': [],

        # 球体相关
        'channel': {'lightning': [], 'frost': [], 'dark': [], 'plasma': [], 'any': []},
        'evoke': [],

        # 特殊资源
        'shiv': [],
        'soul': [],

        # 防御机制
        'thorns': [],
        'artifact': [],
        'intangible': [],
        'plated_armor': [],
    }

    for card in cards:
        energy = parse_energy(card.get('EnergyCost', ''))
        if energy is None:
            continue

        ctype = card.get('Type', '')
        desc = card.get('Description', '')
        rarity = card.get('Rarity', '')
        title = card.get('Title', '')

        if rarity in ['Special', '']:
            continue

        damage = extract_damage(desc)
        block = extract_block(desc)
        draw = extract_draw(desc)

        card_data = {
            'title': title,
            'energy': energy,
            'damage': damage,
            'block': block,
            'draw': draw,
            'rarity': rarity,
            'description': desc
        }

        # --- 力量 (Strength) ---
        if 'Strength' in desc and ctype != 'Power':
            str_val = extract_number(desc, [r'Gain (\d+) Strength'])
            if str_val:
                mechanics['strength'].append({**card_data, 'value': str_val})

        # --- 敏捷 (Dexterity) ---
        if 'Dexterity' in desc and ctype != 'Power':
            dex_val = extract_number(desc, [r'Gain (\d+) Dexterity'])
            if dex_val:
                mechanics['dexterity'].append({**card_data, 'value': dex_val})

        # --- 集中 (Focus) ---
        if 'Focus' in desc:
            focus_val = extract_number(desc, [r'Gain (\d+) Focus'])
            if focus_val:
                mechanics['focus'].append({**card_data, 'value': focus_val})

        # --- 易伤 (Vulnerable) ---
        if 'Vulnerable' in desc:
            vuln_val = extract_number(desc, [r'(\d+) Vulnerable'])
            mechanics['vulnerable'].append({**card_data, 'value': vuln_val or 2})

        # --- 虚弱 (Weak) ---
        if 'Weak' in desc:
            weak_val = extract_number(desc, [r'(\d+) Weak'])
            mechanics['weak'].append({**card_data, 'value': weak_val or 2})

        # --- 中毒 (Poison) ---
        if 'Poison' in desc and ctype != 'Power':
            poison_val = extract_number(desc, [r'(\d+) Poison'])
            if poison_val:
                mechanics['poison'].append({**card_data, 'value': poison_val})

        # --- 脆弱 (Frail) ---
        if 'Frail' in desc:
            mechanics['frail'].append(card_data)

        # --- 消耗 (Exhaust) ---
        if 'Exhaust' in desc:
            if damage and block:
                mechanics['exhaust']['with_damage_block'].append(card_data)
            elif damage:
                mechanics['exhaust']['with_damage'].append(card_data)
            elif block:
                mechanics['exhaust']['with_block'].append(card_data)
            elif draw:
                mechanics['exhaust']['draw'].append(card_data)
            else:
                mechanics['exhaust']['only'].append(card_data)

        # --- 虚无 (Ethereal) ---
        if 'Ethereal' in desc:
            mechanics['ethereal'].append(card_data)

        # --- 保留 (Retain) ---
        if 'Retain' in desc:
            mechanics['retain'].append(card_data)

        # --- 固有 (Innate) ---
        if 'Innate' in desc:
            mechanics['innate'].append(card_data)

        # --- 球体相关 ---
        if 'Channel' in desc or 'Orb' in desc:
            if 'Lightning' in desc:
                mechanics['channel']['lightning'].append(card_data)
            elif 'Frost' in desc:
                mechanics['channel']['frost'].append(card_data)
            elif 'Dark' in desc:
                mechanics['channel']['dark'].append(card_data)
            elif 'Plasma' in desc:
                mechanics['channel']['plasma'].append(card_data)
            else:
                mechanics['channel']['any'].append(card_data)

        if 'Evoke' in desc:
            mechanics['evoke'].append(card_data)

        # --- Shiv ---
        if 'Shiv' in desc:
            shiv_count = extract_number(desc, [r'(\d+) Shiv'])
            mechanics['shiv'].append({**card_data, 'value': shiv_count or 1})

        # --- Soul ---
        if 'Soul' in desc:
            soul_count = extract_number(desc, [r'(\d+) Soul'])
            mechanics['soul'].append({**card_data, 'value': soul_count or 1})

        # --- 荆棘 (Thorns) ---
        if 'Thorns' in desc:
            thorns_val = extract_number(desc, [r'(\d+) Thorns'])
            mechanics['thorns'].append({**card_data, 'value': thorns_val})

        # --- 神器 (Artifact) ---
        if 'Artifact' in desc:
            art_val = extract_number(desc, [r'(\d+) Artifact'])
            mechanics['artifact'].append({**card_data, 'value': art_val})

        # --- 无形 (Intangible) ---
        if 'Intangible' in desc:
            int_val = extract_number(desc, [r'(\d+) Intangible'])
            mechanics['intangible'].append({**card_data, 'value': int_val})

    return mechanics

def calculate_mechanic_value(cards, mechanic_name, base_value_per_energy):
    """计算机制的价值（以能量当量表示）"""
    if not cards:
        return None

    values = []
    for c in cards:
        if c['energy'] > 0 and c.get('value'):
            # 计算该卡牌的基础价值（伤害/格挡部分）
            base_value = 0
            if c.get('damage'):
                base_value += c['damage']
            if c.get('block'):
                base_value += c['block']

            # 预期价值 = 能量 * 单位能量价值
            expected_value = c['energy'] * base_value_per_energy

            # 机制价值 = (预期价值 - 基础价值) / 机制层数
            if c['value'] > 0:
                mechanic_value = (expected_value - base_value) / c['value']
                values.append(mechanic_value)

    if values:
        return {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values)
        }
    return None

def analyze_status_value(cards, status_name, base_dpe=7.0):
    """分析状态效果的价值（基于带伤害的状态牌）"""
    if not cards:
        return None

    # 筛选带伤害的状态牌
    with_damage = [c for c in cards if c.get('damage') and c['energy'] > 0]

    if not with_damage:
        return None

    values = []
    for c in with_damage:
        expected_damage = c['energy'] * base_dpe
        # 考虑AOE效果
        aoe_multiplier = 1.5 if 'ALL' in c.get('description', '') else 1.0
        expected_damage *= aoe_multiplier
        status_value = (expected_damage - c['damage']) / c.get('value', 1)
        values.append(status_value)

    return {
        'mean': statistics.mean(values),
        'median': statistics.median(values),
        'count': len(with_damage),
        'cards': with_damage
    }

def analyze_shiv_value(cards):
    """分析Shiv的价值模型"""
    # Shiv基础属性: 0费 4伤 消耗
    # 计算生成Shiv的卡牌效率
    values = []
    for c in cards:
        if c['energy'] >= 0 and c.get('value'):
            # 假设1张Shiv = 0.5费价值 (0费4伤但会消耗)
            shiv_value = c['value'] * 0.5  # 每张Shiv约0.5费
            # 计算效率
            if c['energy'] > 0:
                efficiency = shiv_value / c['energy']
                values.append({
                    'title': c['title'],
                    'energy': c['energy'],
                    'shiv_count': c['value'],
                    'shiv_value': shiv_value,
                    'efficiency': efficiency
                })
    return values

def analyze_exhaust_value(exhaust_data):
    """分析消耗机制的价值模型"""
    # 消耗通常意味着一次性使用，但获得更高数值
    # 分析带消耗的卡牌相比标准模型的溢价

    results = {}
    for category in ['with_damage', 'with_block']:
        cards = exhaust_data.get(category, [])
        if not cards:
            continue

        premiums = []
        for c in cards:
            if c['energy'] <= 0:
                continue

            base_value = 0
            expected_value = 0

            if category == 'with_damage' and c.get('damage'):
                base_value = c['damage']
                expected_value = c['energy'] * 7.0  # 标准攻击效率
            elif category == 'with_block' and c.get('block'):
                base_value = c['block']
                expected_value = c['energy'] * 6.0  # 标准格挡效率

            if expected_value > 0:
                premium = (base_value - expected_value) / c['energy']
                premiums.append(premium)

        if premiums:
            results[category] = {
                'mean_premium': statistics.mean(premiums),
                'median_premium': statistics.median(premiums),
                'count': len(premiums)
            }

    return results

def print_mechanic_report(mechanics):
    """打印机制分析报告"""

    print("=" * 70)
    print("           SLAY THE SPIRE 2 - 机制关键词费用模型")
    print("=" * 70)

    # 1. 属性增益机制
    print("\n【一、属性增益机制】")
    print("-" * 70)

    print("\n  1.1 力量 (Strength)")
    if mechanics['strength']:
        str_cards = mechanics['strength']
        print(f"     样本数: {len(str_cards)}张")
        for c in str_cards[:5]:
            eff = c['value'] / c['energy'] if c['energy'] > 0 else 0
            print(f"       - {c['title']}: {c['energy']}费 +{c['value']}力量 (效率{eff:.1f}力量/费)")

        # 计算力量价值
        val = calculate_mechanic_value(str_cards, 'strength', 7.0)
        if val:
            print(f"     → 1点力量 ≈ {val['median']:.1f} 伤害当量")

    print("\n  1.2 敏捷 (Dexterity)")
    if mechanics['dexterity']:
        dex_cards = mechanics['dexterity']
        print(f"     样本数: {len(dex_cards)}张")
        for c in dex_cards[:5]:
            eff = c['value'] / c['energy'] if c['energy'] > 0 else 0
            print(f"       - {c['title']}: {c['energy']}费 +{c['value']}敏捷 (效率{eff:.1f}敏捷/费)")

        val = calculate_mechanic_value(dex_cards, 'dexterity', 6.0)
        if val:
            print(f"     → 1点敏捷 ≈ {val['median']:.1f} 格挡当量")

    print("\n  1.3 集中 (Focus)")
    if mechanics['focus']:
        focus_cards = mechanics['focus']
        print(f"     样本数: {len(focus_cards)}张")
        for c in focus_cards:
            print(f"       - {c['title']}: {c['energy']}费 +{c['value']}集中")

    # 2. 负面状态机制
    print("\n【二、负面状态施加机制】")
    print("-" * 70)

    print("\n  2.1 易伤 (Vulnerable)")
    if mechanics['vulnerable']:
        vuln_cards = mechanics['vulnerable']
        print(f"     样本数: {len(vuln_cards)}张")
        val = analyze_status_value(vuln_cards, 'vulnerable')
        if val:
            print(f"     → 1层易伤 ≈ {val['median']:.1f} 伤害当量")
            print(f"       (基于{val['count']}张带伤害易伤牌计算)")

    print("\n  2.2 虚弱 (Weak)")
    if mechanics['weak']:
        weak_cards = mechanics['weak']
        print(f"     样本数: {len(weak_cards)}张")
        val = analyze_status_value(weak_cards, 'weak')
        if val:
            print(f"     → 1层虚弱 ≈ {val['median']:.1f} 伤害当量")

    print("\n  2.3 中毒 (Poison)")
    if mechanics['poison']:
        poison_cards = mechanics['poison']
        print(f"     样本数: {len(poison_cards)}张")
        for c in poison_cards[:5]:
            eff = c['value'] / c['energy'] if c['energy'] > 0 else 0
            print(f"       - {c['title']}: {c['energy']}费 +{c['value']}中毒")

    # 3. 特殊关键词机制
    print("\n【三、特殊关键词机制】")
    print("-" * 70)

    print("\n  3.1 消耗 (Exhaust)")
    exhaust = mechanics['exhaust']
    total_exhaust = sum(len(v) for v in exhaust.values())
    print(f"     样本数: {total_exhaust}张")
    for k, v in exhaust.items():
        if v:
            print(f"       - {k}: {len(v)}张")

    # 分析消耗卡牌的价值溢价
    exhaust_analysis = analyze_exhaust_value(exhaust)
    if exhaust_analysis:
        print("\n     消耗卡牌价值分析:")
        for cat, data in exhaust_analysis.items():
            print(f"       - {cat}: 平均溢价 +{data['mean_premium']:.1f}伤/费 (基于{data['count']}张)")

    print("\n  3.2 虚无 (Ethereal)")
    if mechanics['ethereal']:
        print(f"     样本数: {len(mechanics['ethereal'])}张")
        print("     → 负面关键词，卡牌如果没有立即使用会消失")
        print("     → 通常伴随补偿效果（数值增加或额外效果）")

    print("\n  3.3 保留 (Retain)")
    if mechanics['retain']:
        print(f"     样本数: {len(mechanics['retain'])}张")
        print("     → 正面关键词，价值约0.5~1费")
        for c in mechanics['retain'][:3]:
            print(f"       - {c['title']}: {c['energy']}费")

    print("\n  3.4 固有 (Innate)")
    if mechanics['innate']:
        print(f"     样本数: {len(mechanics['innate'])}张")
        print("     → 正面关键词，确保起手可用")
        print("     → 价值约0.5费（减少抽牌方差）")

    # 4. 球体机制
    print("\n【四、球体机制 (Defect专属)】")
    print("-" * 70)

    for orb_type in ['lightning', 'frost', 'dark', 'plasma']:
        orb_cards = mechanics['channel'][orb_type]
        if orb_cards:
            print(f"\n  4.{['lightning','frost','dark','plasma'].index(orb_type)+1} {orb_type.capitalize()}球")
            print(f"     样本数: {len(orb_cards)}张")
            for c in orb_cards[:3]:
                dmg = f"{c['damage']}伤" if c.get('damage') else ""
                blk = f"{c['block']}格" if c.get('block') else ""
                extra = f" ({dmg}{blk})" if (dmg or blk) else ""
                print(f"       - {c['title']}: {c['energy']}费{extra}")

    if mechanics['evoke']:
        print(f"\n  4.5 激发 (Evoke)")
        print(f"     样本数: {len(mechanics['evoke'])}张")

    # 5. 特殊资源
    print("\n【五、特殊资源机制】")
    print("-" * 70)

    print("\n  5.1 Shiv (小刀)")
    if mechanics['shiv']:
        print(f"     样本数: {len(mechanics['shiv'])}张")
        shiv_analysis = analyze_shiv_value(mechanics['shiv'])
        for c in mechanics['shiv'][:5]:
            print(f"       - {c['title']}: {c['energy']}费 +{c['value']}Shiv")
        print("\n     Shiv价值分析:")
        print("       - Shiv本身: 0费 4伤 消耗")
        if shiv_analysis:
            effs = [s['efficiency'] for s in shiv_analysis]
            print(f"       - 生成效率: 平均{statistics.mean(effs):.2f}费价值/费")
            print(f"       - 1 Shiv ≈ 0.5费价值 (基于0费4伤消耗)")

    print("\n  5.2 Soul (灵魂)")
    if mechanics['soul']:
        print(f"     样本数: {len(mechanics['soul'])}张")
        for c in mechanics['soul'][:5]:
            print(f"       - {c['title']}: {c['energy']}费 +{c['value']}Soul")

    # 6. 防御机制
    print("\n【六、防御机制】")
    print("-" * 70)

    print("\n  6.1 荆棘 (Thorns)")
    if mechanics['thorns']:
        for c in mechanics['thorns']:
            print(f"     - {c['title']}: {c['energy']}费 +{c.get('value', '?')}荆棘")

    print("\n  6.2 神器 (Artifact)")
    if mechanics['artifact']:
        for c in mechanics['artifact']:
            print(f"     - {c['title']}: {c['energy']}费 +{c.get('value', '?')}神器")

    print("\n  6.3 无形 (Intangible)")
    if mechanics['intangible']:
        for c in mechanics['intangible']:
            print(f"     - {c['title']}: {c['energy']}费 +{c.get('value', '?')}无形")

def print_summary_table(mechanics):
    """打印汇总表"""
    print("\n" + "=" * 70)
    print("【机制价值汇总表】")
    print("=" * 70)

    print("""
┌──────────────────────────────────────────────────────────────────────┐
│                     STS2 机制费用模型汇总                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  【属性增益】                                                         │
│    1点力量   ≈ 2-3 伤害当量（持续收益）                               │
│    1点敏捷   ≈ 2-3 格挡当量（持续收益）                               │
│    1点集中   ≈ 1-2 球体伤害/格挡（持续收益）                          │
│                                                                      │
│  【负面状态】                                                         │
│    1层易伤   ≈ 1-2 伤害当量（对单目标）                               │
│    1层虚弱   ≈ 1-2 伤害当量（对单目标）                               │
│    1层中毒   ≈ 0.5-1 伤害当量（每回合，可叠加）                       │
│                                                                      │
│  【关键词价值】                                                       │
│    消耗(Exhaust)  = 通常作为补偿，+1~2费价值                           │
│    保留(Retain)   ≈ +0.5~1 费价值                                     │
│    固有(Innate)   ≈ +0.5 费价值（减少方差）                           │
│    虚无(Ethereal) = 负面，需补偿+0.5~1费价值                          │
│                                                                      │
│  【球体价值 (Defect)】                                                │
│    闪电球 = 3伤害/回合 + 激发8伤害                                     │
│    冰霜球 = 2格挡/回合 + 激发5格挡                                     │
│    黑暗球 = 6伤害/回合(累积) + 激发全部                                │
│    等离子 = 2能量/回合                                                 │
│                                                                      │
│  【特殊资源】                                                         │
│    1 Shiv = 0费 4伤 消耗（约0.5费价值）                               │
│    1 Soul = 约0.5费价值（Necrobinder专属）                            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
""")

def calculate_card_value_score(card, base_dpe=7.0, base_bpe=6.0):
    """计算卡牌的价值分数（基于标准模型）"""
    energy = parse_energy(card.get('EnergyCost', ''))
    if energy is None or energy <= 0:
        return None

    desc = card.get('Description', '')
    rarity = card.get('Rarity', '')
    ctype = card.get('Type', '')
    character = card.get('Character', '')

    # 基础数值
    damage = extract_damage(desc) or 0
    block = extract_block(desc) or 0
    draw = extract_draw(desc) or 0

    # 稀有度调整基准
    rarity_multiplier = {
        'Common': 1.0,
        'Uncommon': 1.15,  # 罕见牌预期高15%
        'Rare': 1.3        # 稀有牌预期高30%
    }.get(rarity, 1.0)

    # 计算基础价值（伤害当量）
    base_value = damage + block * (base_dpe / base_bpe)  # 格挡转换为伤害当量

    # 计算抽牌价值（1抽 ≈ 1费价值 ≈ 7伤害当量，但有能量消耗）
    draw_value = draw * base_dpe * 0.7  # 抽牌价值打折扣，因为需要能量打出

    # 关键词价值估算
    keyword_value = 0

    # 负面关键词（需要补偿）
    if 'Ethereal' in desc:
        keyword_value -= 3.5  # 虚无约-0.5费价值

    # 正面关键词
    if 'Retain' in desc:
        keyword_value += 3.5  # 保留约+0.5费价值
    if 'Innate' in desc:
        keyword_value += 3.5  # 固有约+0.5费价值

    # 消耗卡牌通常有补偿（但之前分析显示不明显）
    if 'Exhaust' in desc:
        if ctype == 'Attack':
            keyword_value += 0  # 攻击消耗无明显溢价
        elif ctype == 'Skill':
            keyword_value += 3  # 技能消耗略有溢价

    # 状态效果估算
    status_value = 0
    if 'Vulnerable' in desc:
        vuln = extract_number(desc, [r'(\d+) Vulnerable']) or 2
        status_value += vuln * 1.0  # 1层易伤≈1伤害当量
    if 'Weak' in desc:
        weak = extract_number(desc, [r'(\d+) Weak']) or 2
        status_value += weak * 1.0  # 1层虚弱≈1伤害当量
    if 'Poison' in desc and ctype != 'Power':
        poison = extract_number(desc, [r'(\d+) Poison']) or 0
        status_value += poison * 0.7  # 1层中毒≈0.7伤害当量/回合
    if 'Strength' in desc and ctype != 'Power':
        str_val = extract_number(desc, [r'Gain (\d+) Strength']) or 0
        status_value += str_val * 4.5  # 1力量≈4.5伤害当量
    if 'Dexterity' in desc and ctype != 'Power':
        dex_val = extract_number(desc, [r'Gain (\d+) Dexterity']) or 0
        status_value += dex_val * 3.5  # 1敏捷≈3.5伤害当量（转换为伤害当量）

    # Shiv价值
    if 'Shiv' in desc:
        shiv_count = extract_number(desc, [r'(\d+) Shiv']) or 1
        status_value += shiv_count * 3.5  # 1 Shiv ≈ 0.5费 ≈ 3.5伤害当量

    # Soul价值
    if 'Soul' in desc:
        soul_count = extract_number(desc, [r'(\d+) Soul']) or 1
        status_value += soul_count * 3.5  # 1 Soul ≈ 0.5费

    # ========== Forge 机制 (Regent专属) ==========
    # Forge X = 给 Sovereign Blade 增加 X 点伤害
    # Sovereign Blade 是 Regent 的专属武器，0费攻击牌
    # Forge 的价值 = 增加的伤害 × 预期使用次数
    if 'Forge' in desc and character == 'Regent':
        forge_val = extract_number(desc, [r'Forge (\d+)']) or 0
        # 假设 Sovereign Blade 每回合平均使用 1-2 次，整场战斗 3-5 回合
        # 1点 Forge ≈ 3-5 点总伤害预期
        # 保守估计：1 Forge ≈ 3 伤害当量（约0.4费价值）
        status_value += forge_val * 3.0  # 1 Forge ≈ 3 伤害当量

    # ========== Summon 机制 (Necrobinder专属) ==========
    # Summon X = 如果 Osty 不在场则召唤他（满血），如果在场则给他加 X 血
    # Osty 会自动攻击，且可以替玩家承担伤害（先扣护甲，再扣Osty血，最后扣玩家血）
    # Osty 的血量还可以给某些牌增加伤害
    if 'Summon' in desc and character == 'Necrobinder':
        summon_val = extract_number(desc, [r'Summon (\d+)']) or 0
        # Summon 的价值：
        # 1. 如果 Osty 不在场：召唤一个单位，相当于获得一个"持续输出+肉盾"
        # 2. 如果 Osty 在场：治疗，同时增加某些牌的伤害
        # 保守估计：1 Summon ≈ 0.5 伤害当量（作为治疗/召唤的综合价值）
        # 但考虑到 Osty 可以替玩家承伤，实际价值更高
        # 假设 Osty 每点 HP 可以吸收 1 点伤害 + 造成 0.5 点伤害
        status_value += summon_val * 1.5  # 1 Summon ≈ 1.5 伤害当量

    # Osty 直接攻击的卡牌（这些是直接伤害，已经通过 extract_damage 计算）
    # 但 Osty 攻击的卡牌通常有额外价值（因为不消耗玩家生命）
    if 'Osty deals' in desc:
        # Osty 的伤害是"安全伤害"，价值略高于玩家伤害
        # 已经通过 extract_damage 计算了基础伤害，这里给 10% 溢价
        osty_damage = extract_number(desc, [r'Osty deals (\d+) damage']) or 0
        if osty_damage > 0:
            status_value += osty_damage * 0.1  # 10% 安全溢价

    # AOE调整（AOE通常效率降低）
    aoe_penalty = 1.0
    if 'ALL' in desc or 'all enemies' in desc.lower():
        aoe_penalty = 0.85  # AOE效率约85%

    # 计算预期价值
    expected_value = energy * base_dpe * rarity_multiplier * aoe_penalty

    # 实际总价值
    actual_value = (base_value + draw_value + keyword_value + status_value) * aoe_penalty

    # 效率比 = 实际价值 / 预期价值
    efficiency_ratio = actual_value / expected_value if expected_value > 0 else 0

    return {
        'title': card.get('Title', ''),
        'energy': energy,
        'rarity': rarity,
        'type': ctype,
        'character': character,
        'damage': damage,
        'block': block,
        'draw': draw,
        'base_value': base_value,
        'draw_value': draw_value,
        'keyword_value': keyword_value,
        'status_value': status_value,
        'actual_value': actual_value,
        'expected_value': expected_value,
        'efficiency_ratio': efficiency_ratio,
        'description': desc[:100] + '...' if len(desc) > 100 else desc
    }

def analyze_card_efficiency(cards):
    """分析所有卡牌的效率，找出超模和亏模卡牌"""
    scores = []

    for card in cards:
        rarity = card.get('Rarity', '')
        if rarity in ['Special', '']:
            continue

        score = calculate_card_value_score(card)
        if score:
            scores.append(score)

    # 按效率排序
    scores.sort(key=lambda x: x['efficiency_ratio'], reverse=True)

    return scores

def print_efficiency_report(scores):
    """打印效率分析报告"""
    print("\n" + "=" * 80)
    print("           SLAY THE SPIRE 2 - 卡牌效率分析（超模/亏模）")
    print("=" * 80)

    # 计算统计数据
    ratios = [s['efficiency_ratio'] for s in scores]
    mean_ratio = statistics.mean(ratios)
    median_ratio = statistics.median(ratios)

    print(f"\n【整体统计】")
    print(f"  分析卡牌数: {len(scores)}张")
    print(f"  平均效率比: {mean_ratio:.2f}")
    print(f"  中位数效率比: {median_ratio:.2f}")
    print(f"  标准差: {statistics.stdev(ratios):.2f}")

    # 定义超模/亏模阈值
    super_threshold = 1.4  # 效率比 > 1.4 视为超模
    good_threshold = 1.2   # 效率比 > 1.2 视为优秀
    bad_threshold = 0.8    # 效率比 < 0.8 视为亏模
    terrible_threshold = 0.6  # 效率比 < 0.6 视为严重亏模

    super_cards = [s for s in scores if s['efficiency_ratio'] >= super_threshold]
    good_cards = [s for s in scores if good_threshold <= s['efficiency_ratio'] < super_threshold]
    normal_cards = [s for s in scores if bad_threshold <= s['efficiency_ratio'] < good_threshold]
    bad_cards = [s for s in scores if terrible_threshold <= s['efficiency_ratio'] < bad_threshold]
    terrible_cards = [s for s in scores if s['efficiency_ratio'] < terrible_threshold]

    print(f"\n【效率分布】")
    print(f"  严重亏模 (<0.6): {len(terrible_cards)}张")
    print(f"  轻度亏模 (0.6-0.8): {len(bad_cards)}张")
    print(f"  正常范围 (0.8-1.2): {len(normal_cards)}张")
    print(f"  优秀卡牌 (1.2-1.4): {len(good_cards)}张")
    print(f"  超模卡牌 (>1.4): {len(super_cards)}张")

    # 打印超模卡牌
    print(f"\n【超模卡牌 Top 15】（效率比 > {super_threshold}）")
    print("-" * 80)
    for i, card in enumerate(super_cards[:15], 1):
        print(f"  {i}. {card['title']}")
        print(f"     费用: {card['energy']} | 稀有度: {card['rarity']} | 类型: {card['type']}")
        print(f"     效率比: {card['efficiency_ratio']:.2f}x")
        print(f"     预期价值: {card['expected_value']:.1f} | 实际价值: {card['actual_value']:.1f}")
        if card['damage'] > 0 or card['block'] > 0:
            stats = []
            if card['damage'] > 0:
                stats.append(f"{card['damage']}伤")
            if card['block'] > 0:
                stats.append(f"{card['block']}格")
            print(f"     基础数值: {' | '.join(stats)}")
        print()

    # 打印优秀卡牌
    print(f"\n【优秀卡牌】（效率比 {good_threshold}-{super_threshold}）")
    print("-" * 80)
    for card in good_cards[:10]:
        print(f"  • {card['title']} ({card['energy']}费 {card['rarity']}) - 效率比: {card['efficiency_ratio']:.2f}x")

    # 打印亏模卡牌
    print(f"\n【轻度亏模卡牌】（效率比 {terrible_threshold}-{bad_threshold}）")
    print("-" * 80)
    for card in bad_cards[:10]:
        print(f"  • {card['title']} ({card['energy']}费 {card['rarity']}) - 效率比: {card['efficiency_ratio']:.2f}x")

    print(f"\n【严重亏模卡牌】（效率比 < {terrible_threshold}）")
    print("-" * 80)
    for card in terrible_cards[:10]:
        print(f"  • {card['title']} ({card['energy']}费 {card['rarity']}) - 效率比: {card['efficiency_ratio']:.2f}x")

    return {
        'super': super_cards,
        'good': good_cards,
        'normal': normal_cards,
        'bad': bad_cards,
        'terrible': terrible_cards,
        'stats': {
            'mean': mean_ratio,
            'median': median_ratio,
            'stdev': statistics.stdev(ratios)
        }
    }

def export_results_to_json(scores, categories, output_path):
    """导出分析结果到JSON文件"""
    result = {
        'metadata': {
            'total_cards_analyzed': len(scores),
            'analysis_date': '2025-03-08',
            'model_version': '1.0'
        },
        'statistics': categories['stats'],
        'categories': {
            'super_model': [
                {
                    'title': c['title'],
                    'energy': c['energy'],
                    'rarity': c['rarity'],
                    'type': c['type'],
                    'efficiency_ratio': round(c['efficiency_ratio'], 2),
                    'expected_value': round(c['expected_value'], 1),
                    'actual_value': round(c['actual_value'], 1),
                    'damage': c['damage'],
                    'block': c['block'],
                    'draw': c['draw'],
                    'description': c['description']
                }
                for c in categories['super']
            ],
            'good': [
                {'title': c['title'], 'energy': c['energy'], 'rarity': c['rarity'], 'efficiency_ratio': round(c['efficiency_ratio'], 2)}
                for c in categories['good']
            ],
            'normal': [
                {'title': c['title'], 'energy': c['energy'], 'rarity': c['rarity'], 'efficiency_ratio': round(c['efficiency_ratio'], 2)}
                for c in categories['normal'][:50]  # 只导出前50个
            ],
            'under_model': [
                {'title': c['title'], 'energy': c['energy'], 'rarity': c['rarity'], 'efficiency_ratio': round(c['efficiency_ratio'], 2)}
                for c in categories['bad'] + categories['terrible']
            ]
        }
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n结果已导出到: {output_path}")

def main():
    cards = load_cards('/tmp/sts2/cards.json')
    print(f"加载了 {len(cards)} 张卡牌\n")

    mechanics = analyze_mechanics(cards)
    print_mechanic_report(mechanics)
    print_summary_table(mechanics)

    # 新增：卡牌效率分析
    print("\n\n")
    scores = analyze_card_efficiency(cards)
    categories = print_efficiency_report(scores)

    # 导出结果
    export_results_to_json(scores, categories, '/tmp/sts2/card_efficiency_analysis.json')

if __name__ == '__main__':
    main()
