---
name:: "[[Retain|保留]]"
english_name:: "Retain"
aliases:: ["保留"]
category:: "[[机制]]"
---

> **英文**: Retain | **中文**: 保留

## 描述

回合结束时不会自动丢弃。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
