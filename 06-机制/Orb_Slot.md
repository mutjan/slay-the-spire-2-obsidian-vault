---
name:: "[[Orb_Slot|充能球槽]]"
english_name:: "Orb_Slot"
aliases:: ["充能球槽"]
category:: "[[机制]]"
---

> **英文**: Orb_Slot | **中文**: 充能球槽

## 描述

容纳充能球的槽位。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
