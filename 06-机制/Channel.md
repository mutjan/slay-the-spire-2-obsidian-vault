---
name:: "[[Channel|充能]]"
english_name:: "Channel"
aliases:: ["充能"]
category:: "[[机制]]"
---

> **英文**: Channel | **中文**: 充能

## 描述

生成一个充能球放入充能球槽。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
