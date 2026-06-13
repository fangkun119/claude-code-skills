---
name: md-rewrite
description: |
  三阶段 Markdown 文档改写 Skill：Phase 1 准备工作环境 → Phase 2 通过 6 轮交互澄清改写需求 → Phase 3 按需改写文档内容。
  当用户提到"改写文档"、"优化文档"、"重写 Markdown"、"文档重组"、"改善文档结构"、"调整写作风格"、"适配目标读者"时触发。
  支持：调整写作风格、重组章节结构、优化内容表达、适配目标读者、文档格式规范化。
  输入：源 Markdown 文件路径（必选）+ 初始改写需求（可选）。
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Write
  - Edit
---

# Markdown 文档改写 Skill

## 概述

本 Skill 通过三阶段流程将用户提供的 Markdown 文档改写为高质量版本：

1. **Phase 1 - Preparation**: 创建工作目录并初始化改写文件
2. **Phase 2 - Requirement Clarification**: 通过 6 轮交互澄清改写需求
3. **Phase 3 - Document Rewrite**: 执行文档改写（包括图片预处理和内容重写）

### 设计动机

将改写拆分为"准备 → 澄清 → 执行"三个独立阶段，使每个阶段的职责边界清晰：
- Phase 2 专注理解用户意图
- Phase 3 专注执行改写
- 各阶段在独立上下文的 Sub Agent 中运行，避免单次改写的上下文窗口耗尽问题

## 输入参数

Skill 接收三个输入参数：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `source_file_path` | string | ✅ | 源 Markdown 文件的绝对或相对路径，是改写内容的唯一来源 |
| `initial_requirements` | string | ❌ | 用户对改写结果的初始需求（自然语言描述），默认为空字符串 |
| `requirements_file_path` | string | ❌ | 用户提供的现有需求文件路径（可选），若提供则跳过 Phase 2 的 6 轮澄清 |

**使用方式**：用户在触发 Skill 时提供这些参数，或由 Skill 在执行过程中询问。

## 系统规则（System Rules）

系统规则拥有最高优先级，约束整个 Skill 生命周期中的所有操作。**必须严格遵守**，不得违反。

### 核心规则概览

1. **源文件只读（source_file_restriction）**：严禁以任何方式修改源文件
2. **四级标题体系（title_restriction）**：改写文档必须遵循严格的四级标题层级
3. **工作区目录隔离（workspace_directory_restriction）**：中间产物必须存放在 workspace/ 目录

**详细规则说明请参考**：`references/system-rules.md`

## 执行流程

### Phase 1: Preparation（准备工作）

创建工作目录并初始化改写文件：

1. 创建工作区目录：`{source_file_dir}/workspace/{source_file_name}/`
2. 拷贝源文件 → `{source_file_dir}/{source_file_name}_rewritten.md`（改写副本）
3. 拷贝源文件 → `{source_file_dir}/{source_file_name}_backup.md`（原始备份）

**路径推导规则**：所有路径由 `source_file_path` 自动推导得出。

```
source_file_path = "./tech_note/codex.md"
↓
source_file_dir  = "./tech_note/"
source_file_name = "codex"
workspace_directory = "./tech_note/workspace/codex/"
rewritten_file_path = "./tech_note/codex_rewritten.md"
backup_file_path = "./tech_note/codex_backup.md"
```

### Phase 2: Requirement Clarification（需求澄清）

**此 Phase 在独立上下文的 Sub Agent 中执行**。

#### (1) 前置检查

执行前先检查是否提供了 `requirements_file_path` 参数：

- **若已提供**：直接将该文件复制到 `{workspace_directory}/requirements.md`，跳过 6 轮澄清，Phase 2 完成
- **若未提供**：执行 6 轮需求澄清流程（以下步骤 ②-④）

#### (2) 6 轮需求澄清流程

##### ① 需求维度澄清

通过 6 轮交互澄清改写需求：

| 轮次 | 澄清问题 | 对应变量 |
|------|---------|---------|
| 1 | 改写后的文档将用于哪些场景？ | `document_purposes` |
| 2 | 改写后的文档面向哪些读者？他们各自的核心诉求是什么？ | `audience_and_needs` |
| 3 | 改写时应扮演什么角色身份？该角色擅长什么？ | `rewriter_personas` |
| 4 | 改写后的文档应采用怎样的表达风格？ | `writing_style` |
| 5 | 改写过程中有哪些不可违反的硬性规则？ | `hard_constraints` |
| 6 | 还有其他需要澄清的问题吗？ | `additional_clarifications` |

##### ② 备选答案生成策略

每轮提问时，Sub Agent 基于对 `initial_requirements` 和源文件内容的理解，生成可能性最高的若干备选答案，按可能性从高到低排列，供用户多选或补充。

##### ③ 结果持久化

**完成后**，将所有问题和用户回答整理为 JSON，保存至：
`{workspace_directory}/requirements.md`

**详细指导请参考**：`references/phase-2-clarification.md`

### Phase 3: Document Rewrite（文档改写）

**此 Phase 在独立上下文的 Sub Agent 中执行**，包含三个子步骤：

#### (1) 确定执行方式

通过 `AskUserQuestion` 询问用户"是否保持原文的章节顺序"，备选答案为"是"和"否"：
- **是** → 进入 **Option A：保持原文章节顺序**
- **否** → 进入 **Option B：重排章节顺序**

#### (2) 文档图片预处理

为每张图片下方添加 Markdown 注释，记录图片路径、用途和内容描述，为后续改写提供辅助信息。

执行方式：启动独立 Sub Agent 负责，按**从下到上逆序**为每张图片添加注释。

注释格式：
```markdown
<!--
图片内容说明
路径：{图片文件路径}
用途：{推测出来的图片用途}
内容：{提炼出的图片内容说明}
-->
```

#### (3) 文档重写

根据用户选择进入不同分支：

**Option A：保持原文章节顺序**
- Operation 1：章拆分（由独立 Sub Agent 完成）
- Operation 2：逆序逐一改写（调度 Sub Agent 管理，按从下到上逆序为每章创建独立 Sub Agent）

**Option B：重排章节顺序**
- Operation 1：改写结果规格分析（启动独立 Sub Agent，产出 `spec.md`）
- Operation 2：任务拆分与计划制定（启动独立 Sub Agent，产出 `plan.md`）
- Operation 3：计划执行（启动独立 Sub Agent，逐一执行 plan.md 中的步骤）

**详细指导请参考**：`references/phase-3-rewrite.md`

## 四级标题体系

改写文档中所有章节标题必须严格遵循以下四级标题体系：

| Level | 名称 | Markdown 前缀 | 编号模式 | 格式示例 |
|-------|------|--------------|----------|----------|
| 1 | 章 | `##` | 阿拉伯数字递增 | `## 1. ` |
| 2 | 节 | `###` | 父级.子级递增 | `### 1.1 ` |
| 3 | 小节 | `####` | 圆括号阿拉伯数字递增 | `#### (1) ` |
| 4 | 段落条目 | `#####` | 带圈数字递增 | `##### ① ` |

**附加规则**：
- 不允许超出以上四个层级
- 每个层级的标题编号必须严格按上述格式编写

**详细参考**：`references/title-system.md`

## Sub Agent 执行策略

### 设计动机

Phase 2 和 Phase 3 均在独立上下文的 Sub Agent 中执行：
- 每个阶段都需要读取完整源文件并与用户多轮交互或执行大量改写操作
- 若全部在主 Agent 中运行，上下文窗口会迅速耗尽
- 拆分为独立 Sub Agent 后，每个 Agent 只需关注当前阶段的任务，上下文利用率最优

### 并发控制

Phase 3 中可能同时拆分出多个 Sub Agent。为避免触发大模型 API 并发度限制：
- **多个 Sub Agent 必须 2 个 2 个地分配运行**
- 即同时最多 2 个 Sub Agent 在执行
- 待其中一组完成后再启动下一组

## 开始使用

当你准备好源文件路径和可选的初始需求后，本 Skill 将自动执行三阶段流程：

1. **自动完成**：Phase 1 准备工作
2. **交互澄清**：Phase 2 通过 6 轮提问理解你的改写需求
3. **执行改写**：Phase 3 根据你的选择完成文档改写

输出文件：`{source_file_dir}/{source_file_name}_rewritten.md`
