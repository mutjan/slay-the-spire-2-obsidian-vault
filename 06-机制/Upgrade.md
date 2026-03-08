---
name:: "[[Upgrade|升级]]"
english_name:: "Upgrade"
aliases:: ["升级"]
category:: "[[机制]]"
---

> **英文**: Upgrade | **中文**: 升级

## 描述

强化卡牌的效果。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
