---
name:: "[[Unplayable|不可打出]]"
english_name:: "Unplayable"
aliases:: ["不可打出"]
category:: "[[机制]]"
---

> **英文**: Unplayable | **中文**: 不可打出

## 描述

无法从手牌中打出。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
