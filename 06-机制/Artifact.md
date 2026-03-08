---
name:: "[[Artifact|神器]]"
english_name:: "Artifact"
aliases:: ["神器"]
category:: "[[机制]]"
---

> **英文**: Artifact | **中文**: 神器

## 描述

免疫下一次受到的负面效果。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
