---
name:: "[[Transform|转化]]"
english_name:: "Transform"
aliases:: ["转化"]
category:: "[[机制]]"
---

> **英文**: Transform | **中文**: 转化

## 描述

将卡牌变为随机其他卡牌。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
