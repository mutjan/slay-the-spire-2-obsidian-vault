---
name:: "[[Dexterity|敏捷]]"
english_name:: "Dexterity"
aliases:: ["敏捷"]
category:: "[[机制]]"
---

> **英文**: Dexterity | **中文**: 敏捷

## 描述

增加从卡牌获得的格挡值。每点敏捷增加1点格挡。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
