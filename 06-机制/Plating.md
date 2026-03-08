---
name:: "[[Plating|护甲]]"
english_name:: "Plating"
aliases:: ["护甲"]
category:: "[[机制]]"
---

> **英文**: Plating | **中文**: 护甲

## 描述

类似格挡，但不会随回合消失。受到伤害时优先消耗。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
