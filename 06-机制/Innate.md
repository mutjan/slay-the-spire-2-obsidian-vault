---
name:: "[[Innate|固有]]"
english_name:: "Innate"
aliases:: ["固有"]
category:: "[[机制]]"
---

> **英文**: Innate | **中文**: 固有

## 描述

战斗开始时就放入手牌。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
