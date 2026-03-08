---
name:: "[[Exhaust|消耗]]"
english_name:: "Exhaust"
aliases:: ["消耗"]
category:: "[[机制]]"
---

> **英文**: Exhaust | **中文**: 消耗

## 描述

打出后从本场战斗中移除，进入消耗牌堆。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
