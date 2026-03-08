---
name:: "[[Poison|毒素]]"
english_name:: "Poison"
aliases:: ["毒素"]
category:: "[[机制]]"
---

> **英文**: Poison | **中文**: 毒素

## 描述

在回合开始时造成伤害，然后减少1点。无视格挡。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
