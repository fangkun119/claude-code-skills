# 系统规则（System Rules）

## 概述

系统规则定义了 Skill 执行过程中不可逾越的边界条件。它们拥有**最高优先级**——任何执行阶段的逻辑都不得覆盖或违反这些约束。

这些约束对主 Agent 和执行期间产生的所有 Sub Agent 均有效。

## 三大核心规则

### 规则 1：源文件只读（source_file_restriction）

**严禁以任何方式修改 `{source_file_path}` 所指的源文件。**

#### 设计动机

源文件是改写的唯一真实来源（single source of truth）：
- 改写过程会产生大量中间状态
- 若源文件被意外修改，将无法回溯原始内容
- 改写的可追溯性和可重复性会被破坏

因此，源文件在整个 Skill 生命周期中必须保持只读。

#### 禁止的操作

包括但不限于：
- 写入、追加、覆盖、删除内容
- 任何形式的修改操作

#### 正确做法

- 所有改写操作都在**改写副本**（`{rewritten_file_path}`）上进行
- 源文件仅作为读取参考

---

### 规则 2：四级标题体系（title_restriction）

改写文件中所有章节标题必须严格遵循以下四级标题体系，不允许超出这四个层级。

#### 标题层级规格

| Level | 名称 | Markdown 前缀 | 编号模式 | 格式 | 示例 |
|-------|------|--------------|----------|------|------|
| 1 | 章 | `##` | 阿拉伯数字递增 | `## {n}. ` | `## 1. ` |
| 2 | 节 | `###` | 父级.子级递增 | `### {n}.{m} ` | `### 1.1 ` |
| 3 | 小节 | `####` | 圆括号阿拉伯数字递增 | `#### ({k}) ` | `#### (1) ` |
| 4 | 段落条目 | `#####` | 带圈数字递增 | `##### {circled_n} ` | `##### ① ` |

#### JSON 规格定义

```json
{
  "levels": [
    {
      "level": 1,
      "name": "章",
      "markdown_prefix": "##",
      "numbering_pattern": "阿拉伯数字递增",
      "format": "## {n}. ",
      "example": "## 1. "
    },
    {
      "level": 2,
      "name": "节",
      "markdown_prefix": "###",
      "numbering_pattern": "父级.子级递增",
      "format": "### {n}.{m} ",
      "example": "### 1.1 "
    },
    {
      "level": 3,
      "name": "小节",
      "markdown_prefix": "####",
      "numbering_pattern": "圆括号阿拉伯数字递增",
      "format": "#### ({k}) ",
      "example": "#### (1) "
    },
    {
      "level": 4,
      "name": "段落条目",
      "markdown_prefix": "#####",
      "numbering_pattern": "带圈数字递增",
      "format": "##### {circled_n} ",
      "example": "##### ① "
    }
  ]
}
```

#### 附加规则

1. **不允许超出以上四个层级**
2. **每个层级的标题编号必须按上述格式编写**
3. 开发者在实现标题编号逻辑时应逐字段对照规格定义

#### 设计动机

统一的标题层级保证改写文档的结构一致性：
- Skill 的改写流程会将文档拆分到多个 Sub Agent 并行处理
- 只有严格的标题规范才能确保各章节独立改写后仍能无缝拼合
- 避免出现层级冲突或编号错乱

---

### 规则 3：工作区目录（workspace_directory_restriction）

Skill 运行期间生成的文件分为两类，各有存放位置约束。

#### 文件分类

1. **输出文件**：存放在源文件同目录下（`{source_file_dir}`）
   - 改写副本：`{rewritten_file_path}`
   - 原始备份：`{backup_file_path}`

2. **中间产物**：必须且只能存放在 `{workspace_directory}` 目录下
   - 如：requirements.md、spec.md、plan.md 等

#### 设计动机

- 改写副本和备份放在源文件同目录下：确保文档中基于相对路径的图片和 Wiki-link 引用不会因目录变更而失效
- 中间产物隔离到独立的工作区目录：避免污染用户文件系统，且清理和归档简单——只需处理一个目录

#### 路径推导规则

所有路径变量由用户输入的 `{source_file_path}` 推导得出：

| 变量 | 推导方式 | 示例 |
|------|---------|------|
| `{source_file_path}` | 用户输入的源文件完整路径 | `./tech_note/codex.md` |
| `{source_file_dir}` | 取 `{source_file_path}` 的父目录 | `./tech_note/` |
| `{source_file_name}` | 取 `{source_file_path}` 的文件名部分（不含扩展名） | `codex` |
| `{workspace_directory}` | `{source_file_dir} + "workspace/" + {source_file_name} + "/"` | `./tech_note/workspace/codex/` |
| `{rewritten_file_path}` | `{source_file_dir} + {source_file_name} + "_rewritten.md"` | `./tech_note/codex_rewritten.md` |
| `{backup_file_path}` | `{source_file_dir} + {source_file_name} + "_backup.md"` | `./tech_note/codex_backup.md` |

#### 路径模板

| 变量 | 路径模板 |
|------|----------|
| `{workspace_directory}` | `{source_file_dir}/workspace/{source_file_name}/` |
| `{rewritten_file_path}` | `{source_file_dir}/{source_file_name}_rewritten.md` |
| `{backup_file_path}` | `{source_file_dir}/{source_file_name}_backup.md` |

#### 推导示例

以 `{source_file_path}` = `"./tech_note/codex.md"` 为例：

- `{source_file_dir}` = `"./tech_note/"`
- `{source_file_name}` = `"codex"`
- `{workspace_directory}` = `"./tech_note/workspace/codex/"`
- `{rewritten_file_path}` = `"./tech_note/codex_rewritten.md"`
- `{backup_file_path}` = `"./tech_note/codex_backup.md"`

## 规则总结

| 规则 | 核心要求 | 违反后果 |
|------|---------|---------|
| 源文件只读 | 不修改 `{source_file_path}` | 破坏可追溯性和可重复性 |
| 四级标题体系 | 严格遵循四级层级和编号格式 | 文档结构混乱，无法正确拼合 |
| 工作区目录隔离 | 中间产物放入 `workspace/` | 污染用户文件系统 |

**记住**：系统规则是整个 Skill 的基石，任何时候都不能违反。
