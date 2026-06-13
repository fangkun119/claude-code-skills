# Phase 2: Requirement Clarification（需求澄清）

## 概述

此 Phase 在**独立上下文的 Sub Agent** 中执行，目标是通过需求澄清并将结果持久化到 `{workspace_directory}/requirements.md`。

**Phase 2 通过 6 轮交互澄清需求**：

## 前置检查

在执行 6 轮澄清之前，先检查是否提供了 `{requirements_file_path}` 参数：

- **若已提供**：直接将该文件复制到 `{workspace_directory}/requirements.md`，跳过本流程，Phase 2 完成
- **若未提供**：继续执行以下 6 轮澄清流程

**设计动机**：支持用户复用已有的需求规格文件，避免重复澄清相同的需求维度，提升改写效率。用户可能在之前的改写中已经明确了需求，或者有预定义的需求模板，直接复用可节省时间。

---

## 执行流程

```mermaid
flowchart LR
    R1["第 1 轮：document_purposes"] --> R2["第 2 轮：audience_and_needs"]
    R2 --> R3["第 3 轮：rewriter_personas"]
    R3 --> R4["第 4 轮：writing_style"]
    R4 --> R5["第 5 轮：hard_constraints"]
    R5 --> R6["第 6 轮：additional_clarifications"]
    R6 --> SAVE["整理 JSON → requirements.md"]
    SAVE --> DONE["Phase 2 完成"]
```

## 6 轮需求澄清流程

### ① 需求维度澄清详情

Sub Agent 分析 `{initial_requirements}` 和 `{source_file_path}` 的文件内容后，通过 6 轮 `AskUserQuestion` 逐一澄清以下需求维度：

#### 轮次 1：document_purposes（文档用途）

**问题**：改写后的文档将用于哪些场景？

**是否多选**：容许多选
**是否必填**：容许为空
**对应变量**：`document_purposes`

**示例答案**：
```json
["技术培训", "向技术经理介绍该技术"]
```

**澄清意图**：
- 了解文档的使用场景有助于确定改写的重点方向
- 不同场景对内容的深度、广度、表达方式有不同要求

---

#### 轮次 2：audience_and_needs（读者与需求）

**问题**：改写后的文档面向哪些读者？他们各自的核心诉求是什么？

**是否多选**：容许多选
**是否必填**：容许为空
**对应变量**：`audience_and_needs`

**示例答案**：
```json
[
  "程序员，学习文档中的技术",
  "技术经理，了解技术价值、应用场景、选型和架构"
]
```

**澄清意图**：
- 明确目标读者有助于选择合适的表达方式和内容深度
- 了解读者诉求能帮助突出关键信息

---

#### 轮次 3：rewriter_personas（改写角色）

**问题**：改写时应扮演什么角色身份？该角色擅长什么？

**是否多选**：容许多选
**是否必填**：容许为空
**对应变量**：`rewriter_personas`

**示例答案**：
```json
[
  "资深架构师、逻辑清晰、擅长技术可视化、深入浅出",
  "Java 分布式技术栈培训师、精通中间件、重视实操"
]
```

**澄清意图**：
- 明确改写者的角色身份有助于确定行文风格和视角
- 角色的专业背景会影响技术表述的准确性和深度

---

#### 轮次 4：writing_style（写作风格）

**问题**：改写后的文档应采用怎样的表达风格（行文风格、内容深度、表达调性等）？

**是否多选**：容许多选
**是否必填**：容许为空
**对应变量**：`writing_style`

**示例答案**：
```json
[
  "用词精炼但内容充实",
  "适合图表的部分用 mermaid 或 ASCII chart 表示"
]
```

**澄清意图**：
- 写作风格直接影响读者的阅读体验
- 不同的内容类型适合不同的表达方式

---

#### 轮次 5：hard_constraints（硬性约束）

**问题**：改写过程中有哪些不可违反的硬性规则？

**是否多选**：容许多选
**是否必填**：容许为空
**对应变量**：`hard_constraints`

**示例答案**：
```json
[
  "代码必须格式化放在 code block 中、完整保留",
  "行文风格参考 @./tech_doc/sector_sample.md"
]
```

**澄清意图**：
- 硬性约束是改写过程中必须遵守的规则
- 这些规则通常来自文档格式要求或内容完整性要求

---

#### 轮次 6：additional_clarifications（补充澄清）

**问题**：还有其他需要澄清的问题吗？

**是否多选**：容许多选
**是否必填**：容许为空
**对应变量**：`additional_clarifications`

**示例答案**：
```json
[
  "提问：操作时的命令和终端输出是否保留？<br>用户回答：是的保留，放在 text 类型的 code block 中、格式化后完整保留"
]
```

**澄清意图**：
- 捕捉前 5 轮未涵盖的特殊需求
- 提供开放的澄清空间

---

### ② 备选答案生成策略

每一轮提问时，Sub Agent 应基于以下信息生成备选答案：

1. **`{initial_requirements}`**：用户的初始需求
2. **源文件内容**：原文档的主题、结构、内容特征
3. **前几轮用户的回答**：已澄清的需求维度

#### 生成原则

- 备选答案应按**可能性从高到低排列**
- 提供 3-5 个备选答案
- 备选答案应**具体、可操作**
- 用户可**多选**备选答案，也可**打字补充**

#### 示例：生成第 1 轮备选答案

假设源文件是关于 "Kubernetes 集群部署" 的技术文档，`initial_requirements` 为 "简化内容，适合初学者"：

**可能生成的备选答案**：
1. "新人培训材料，帮助团队成员快速上手 Kubernetes"
2. "向非技术管理层介绍 Kubernetes 的价值和基本概念"
3. "作为客户部署手册，提供清晰的步骤说明"
4. "技术博客文章，分享 Kubernetes 最佳实践"

### ③ 结果持久化

所有轮次完成后，将各轮的问题和用户回答整理为 JSON，保存至：
`{workspace_directory}/requirements.md`

### JSON 格式

```json
{
  "document_purposes": {
    "clarification_question": "改写后的文档将用于哪些场景？",
    "answers": ["程序员技术培训", "向技术经理介绍该技术"]
  },
  "audience_and_needs": {
    "clarification_question": "改写后的文档面向哪些读者？他们各自的核心诉求是什么？",
    "answers": ["程序员，学习文档中的技术", "技术经理，了解技术价值、应用场景、选型和架构"]
  },
  "rewriter_personas": {
    "clarification_question": "改写时应扮演什么角色身份？该角色擅长什么？",
    "answers": ["资深架构师、逻辑清晰、擅长技术可视化、深入浅出、发现技术价值", "Java分布式技术栈培训师、精通中间件技术、重视实操、擅长编写教学文稿"]
  },
  "writing_style": {
    "clarification_question": "改写后的文档应采用怎样的表达风格（行文风格、内容深度、表达调性等）？",
    "answers": ["用词精炼但内容充实", "适合使用图表展示的部分、用mermaid或ascii chart来表示"]
  },
  "hard_constraints": {
    "clarification_question": "改写过程中有哪些不可违反的硬性规则？",
    "answers": ["代码必须格式化放在code block中、然后完整保留", "操作步骤要介绍清楚、不能省略或简单概括"]
  },
  "additional_clarifications": {
    "clarification_question": "还有其他需要澄清的问题吗？",
    "answers": ["提问：操作时的命令和终端输出是否保留？ 用户回答：是的保留，放在text类型的code block中、格式化后完整保留"]
  }
}
```

## Sub Agent 执行注意事项

1. **独立上下文**：此 Phase 在独立的 Sub Agent 中执行，拥有独立的上下文窗口
2. **串行执行**：6 轮提问严格按照顺序执行，不可并行或跳过
3. **灵活处理**：若用户在某轮表示"没有特殊要求"，可继续下一轮
4. **记录完整**：确保所有问题和用户回答都被正确记录到 `requirements.md`

## 进入 Phase 3 的条件

当以下条件满足时，Phase 2 完成，可进入 Phase 3：

1. 6 轮提问全部完成
2. `requirements.md` 文件已成功保存到 `{workspace_directory}/`
3. 主 Agent 确认可以继续
