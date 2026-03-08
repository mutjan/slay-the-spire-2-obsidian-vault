---
name:: "[[Wound|伤口]]"
english_name:: "Wound"
aliases:: ["伤口"]
category:: "[[机制]]"
---

> **英文**: Wound | **中文**: 伤口

## 描述

状态牌，无法打出。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
