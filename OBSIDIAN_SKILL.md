---
name: obsidian-vault
description: Create and manage Obsidian knowledge base vaults with markdown files, Dataview queries, wiki links, and structured relationships. Use for building interconnected knowledge systems, personal wikis, entity relationship databases, and comprehensive topic libraries with graph visualization support.
license: Complete terms in LICENSE.txt
---

# Obsidian Vault Creator

Create professional Obsidian knowledge base vaults with structured markdown files, bidirectional wiki links, Dataview queries, and relationship mappings.

## Core Capabilities

### 1. Vault Structure Creation

Create organized vault directory structures:

```
vault-name/
├── Main Category/          # Primary content folders
├── Subcategory/            # Secondary classifications
├── Entities/               # People, places, items, concepts
├── Navigation/             # Index pages and directories
└── .obsidian/              # Obsidian configuration (optional)
    ├── community-plugins.json
    └── plugins/
```

### 2. Markdown Content Generation

Generate rich markdown files with:

**Wiki Links**: `[[Page Name]]` or `[[Target|Display Text]]`
- Creates bidirectional connections between pages
- Supports aliases for different names of the same entity

**Dataview Inline Fields**: `field:: value`
- Enables dynamic queries and relationship mapping
- Supports linking: `author:: [[Person Name]]`

**Frontmatter YAML**:
```yaml
---
title: Page Title
category: Category
tags: [tag1, tag2]
created: 2024-01-01
---
```

### 3. Dataview Query Integration

Add dynamic tables and lists:

```markdown
```dataview
TABLE field1 as "Column 1", field2 as "Column 2"
FROM "Folder"
WHERE condition
SORT field DESC
```
```

### 4. Relationship Mapping

Create entity relationships using Dataview fields:

```markdown
# Character Name

author:: [[Author Name]]
spouse:: [[Spouse Name]]
children:: [[Child 1]], [[Child 2]]
house:: [[House Name]]
allegiance:: [[Faction Name]]
```

## Workflow

### Step 1: Plan Vault Structure

Determine:
- Main categories and subcategories
- Entity types (people, places, items, events, concepts)
- Relationship types between entities
- Navigation/index pages needed

### Step 2: Create Directory Structure

```python
from pathlib import Path

vault_path = Path("/path/to/VaultName")
categories = ["Characters", "Locations", "Items", "Events", "Navigation"]

for cat in categories:
    (vault_path / cat).mkdir(parents=True, exist_ok=True)
```

### Step 3: Generate Content Files

Use Python scripts to batch-generate markdown files:

```python
def create_entity_file(vault_path, entity_name, entity_data, category):
    file_path = vault_path / category / f"{entity_name}.md"

    content = f"""# {entity_name}

> **Type**: {entity_data['type']} | **Category**: [[{entity_data['category']}]]

## Description

{entity_data['description']}

## Relationships

{chr(10).join([f"{k}:: [[{v}]]" for k, v in entity_data['relationships'].items()])}

## Related Pages

{chr(10).join([f"- [[{r}]]" for r in entity_data['related']])}

---

*Back to [[{category} Directory]]*
"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
```

### Step 4: Create Navigation Pages

Generate index pages with Dataview queries:

```markdown
# Directory

## All Pages

```dataview
TABLE type as "Type", category as "Category"
FROM "Category"
SORT file.name ASC
```

## By Relationship

```dataview
TABLE relationships as "Relationships"
FROM "Category"
WHERE relationships
```
```

### Step 5: Configure Obsidian (Optional)

Install plugins via direct download:

```bash
# Dataview plugin
mkdir -p vault/.obsidian/plugins/dataview
curl -L "https://github.com/blacksmithgu/obsidian-dataview/releases/download/0.5.68/dataview-0.5.68.zip" -o /tmp/dataview.zip
unzip /tmp/dataview.zip -d vault/.obsidian/plugins/dataview/

# Graph Link Types plugin
mkdir -p vault/.obsidian/plugins/graph-link-types
curl -L "https://github.com/user/graph-link-types/releases/download/0.3.3/graph-link-types.zip" -o /tmp/graph-link-types.zip
unzip /tmp/graph-link-types.zip -d vault/.obsidian/plugins/graph-link-types/
```

Create `community-plugins.json`:
```json
[
  "dataview",
  "graph-link-types"
]
```

## Design Patterns

### Pattern 1: Entity-Relationship Database

For novels, games, or complex worlds:

```
Entities/
├── Characters/           # People with relationships
├── Locations/            # Places with connections
├── Organizations/        # Groups and factions
├── Events/               # Historical events
└── Concepts/             # Ideas and terminology
```

**Relationship fields**: `father::`, `mother::`, `spouse::`, `house::`, `location::`, `participated::`

### Pattern 2: Hierarchical Knowledge Base

For structured topics like zodiac, taxonomy:

```
Topics/
├── Main Categories/      # 12 zodiac signs
├── Subcategories/        # 144 combinations
├── Attributes/           # Elements, modes
└── Relationships/        # Compatibility analyses
```

**Linking pattern**: `[[Parent.Child]]` for hierarchical relationships

### Pattern 3: Daily Notes with Links

For journaling or project tracking:

```markdown
# 2024-01-01

date:: 2024-01-01
mood:: [[Happy]]
projects:: [[Project A]], [[Project B]]
people:: [[Alice]], [[Bob]]

## Notes

Today I worked on [[Project A]] with [[Alice]].
```

## Best Practices

### Wiki Links
- Use consistent naming conventions
- Create alias links for alternate names: `[[Full Name|Nickname]]`
- Link entities on first mention in each file

### Dataview Fields
- Use lowercase field names with `::` syntax
- Link entity values: `author:: [[Author Name]]` not `author:: Author Name`
- Group related fields: personal info, relationships, metadata

### File Organization
- Keep file paths meaningful: `Category/Subcategory/Name.md`
- Use URL-safe filenames (no special characters)
- Create stub files for all linked entities

### Content Structure
- Start with metadata callout: `> **Field**: value`
- Use headers for major sections
- End with navigation links
- Include Dataview queries for dynamic content

## Example: Complete Vault Generation

See bundled script for full implementation:

```bash
python /Users/lzw/Library/Application\ Support/LobsterAI/SKILLs/obsidian-vault/scripts/generate_zodiac_vault.py
```

This generates a 284-file zodiac knowledge base with:
- 12 main sign pages with planetary influences
- 144 sun-ascendant combinations
- 12 moon sign emotional profiles
- 12 venus sign love styles
- 12 mars sign action patterns
- 78 compatibility analyses
- Element and mode explanations
- Full navigation with Dataview queries

## Common Operations

### Count Files
```bash
find vault-path -name "*.md" | wc -l
```

### Check Vault Size
```bash
du -sh vault-path
```

### Validate Links
Use Obsidian's Graph view or third-party plugins to detect broken links.

## Resources

- [Obsidian Documentation](https://help.obsidian.md/)
- [Dataview Plugin Docs](https://blacksmithgu.github.io/obsidian-dataview/)
- [Markdown Syntax](https://www.markdownguide.org/)
