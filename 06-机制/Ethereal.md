---
name:: "[[Ethereal|虚无]]"
english_name:: "Ethereal"
aliases:: ["虚无"]
category:: "[[机制]]"
---

> **英文**: Ethereal | **中文**: 虚无

## 描述

如果在手牌中未被打出，在回合结束时被消耗。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
