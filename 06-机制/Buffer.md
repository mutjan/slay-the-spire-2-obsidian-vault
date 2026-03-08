---
name:: "[[Buffer|缓冲]]"
english_name:: "Buffer"
aliases:: ["缓冲"]
category:: "[[机制]]"
---

> **英文**: Buffer | **中文**: 缓冲

## 描述

免疫下一次受到的生命值损失。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
