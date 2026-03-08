---
name:: "[[Sweeping_Gaze|扫视]]"
english_name:: "Sweeping_Gaze"
aliases:: ["扫视"]
category:: "[[机制]]"
---

> **英文**: Sweeping_Gaze | **中文**: 扫视

## 描述

储君的衍生牌。

## 相关卡牌

```dataview
TABLE type as "类型", character as "角色", rarity as "稀有度"
FROM "02-卡牌"
WHERE contains(file.outlinks, this.file.link) OR contains(file.inlinks, this.file.link)
SORT type, character
```

---

*返回 [[机制目录]]*
