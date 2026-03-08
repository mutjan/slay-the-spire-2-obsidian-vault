---
name:: "[[Block|格挡]]"
english_name:: "Block"
aliases:: ["格挡"]
category:: "[[机制]]"
---

> **英文**: Block | **中文**: 格挡

## 描述

阻挡即将到来的伤害。在下一回合开始时会消失。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
