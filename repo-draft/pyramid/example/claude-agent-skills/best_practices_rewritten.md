# Claude Skill 创作完全指南：从设计原则到高级实现的最佳实践

> 学习如何编写有效的 Skill，使 Claude 能够发现和成功使用。

**本指南的核心价值在于**，帮助您编写 Claude 能够有效发现和使用的 Skill，通过实用的创作决策确保 Skill 的简洁性、结构良好性和真实可用性。

有关 Skill 工作原理的概念背景，请参阅[Skill 概述](/zh-CN/docs/agents-and-tools/agent-skills/overview)。

## 1. 核心设计原则

### 1.1 简洁性优先：令牌优化策略

#### 1.1.1 上下文窗口资源管理

**核心认知**：上下文窗口是有限的公共资源，需要高效利用。

* **资源竞争现实**：您的 Skill 与系统提示、对话历史、其他 Skill 元数据和实际请求共享上下文窗口
* **成本控制机制**：Skill 令牌无直接成本，但加载后会与对话历史和其他上下文竞争
* **按需加载优势**：只有元数据在启动时预加载，SKILL.md 仅在 Skill 相关时读取
* **简洁性必要性**：即使采用按需加载机制，SKILL.md 简洁性仍然至关重要

#### 1.1.2 默认假设：Claude 的智能基础

**核心假设**：Claude 已经非常聪明，只需添加其缺失的上下文。

* **信息过滤原则**：质疑每一条信息的必要性
  * "Claude 真的需要这个解释吗？"
  * "我能假设 Claude 知道这个吗？"
  * "这段落值得它的令牌成本吗？"
* **知识基础认知**：假设 Claude 具备基础技术概念和常识
* **价值最大化目标**：确保每个令牌都为解决特定问题服务

#### 1.1.3 简洁与冗长的对比实例

**对比分析清楚表明**：简洁版本假设 Claude 具备基础知识，效果更好。

* **好的例子：简洁**（大约 50 个令牌）：
  * 直接使用 pdfplumber 进行文本提取
  * 假设 Claude 了解 PDF 基本概念
  * 聚焦于具体实现方法

````markdown  theme={null}
## 提取 PDF 文本

使用 pdfplumber 进行文本提取：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
````
````

* **不好的例子：过于冗长**（大约 150 个令牌）：
  * 解释 PDF 基本概念和用途
  * 详细说明库的选择过程
  * 包含安装和基础使用说明

```markdown  theme={null}
## 提取 PDF 文本

PDF（便携式文档格式）文件是一种常见的文件格式，包含
文本、图像和其他内容。要从 PDF 中提取文本，您需要
使用一个库。有许多库可用于 PDF 处理，但我们
建议使用 pdfplumber，因为它易于使用且能处理大多数情况。
首先，您需要使用 pip 安装它。然后您可以使用下面的代码...
```

### 1.2 自由度设置：精确控制指导程度

#### 1.2.1 自由度层次与任务匹配

**核心原则**：根据任务脆弱性和可变性精确匹配指导程度。

* **高自由度场景**：多种方法有效、决策依赖上下文、启发式指导
* **中等自由度场景**：存在首选模式、部分变化可接受、配置影响行为
* **低自由度场景**：操作脆弱易错、一致性至关重要、必须遵循特定序列

#### 1.2.2 高自由度：基于文本的说明

**适用场景**：多种方法都有效，需要根据上下文灵活决策。

* **使用特征**：
  * 多种方法都有效
  * 决策取决于上下文
  * 启发式方法指导方法
* **示例应用**：代码审查流程
  * 分析代码结构和组织
  * 检查潜在错误或边界情况
  * 建议改进可读性和可维护性
  * 验证是否遵守项目约定

```markdown  theme={null}
## 代码审查流程

1. 分析代码结构和组织
2. 检查潜在的错误或边界情况
3. 建议改进可读性和可维护性
4. 验证是否遵守项目约定
```

#### 1.2.3 中等自由度：参数化脚本

**适用场景**：存在首选模式，某些变化可以接受，配置影响行为。

* **使用特征**：
  * 存在首选模式
  * 某些变化是可以接受的
  * 配置影响行为
* **示例应用**：报告生成模板
  * 提供基础模板结构
  * 支持参数自定义
  * 允许根据需要调整

````markdown  theme={null}
## 生成报告

使用此模板并根据需要自定义：

```python
def generate_report(data, format="markdown", include_charts=True):
    # 处理数据
    # 以指定格式生成输出
    # 可选地包含可视化
````
````

#### 1.2.4 低自由度：精确执行指令

**适用场景**：操作脆弱且容易出错，一致性至关重要。

* **使用特征**：
  * 操作脆弱且容易出错
  * 一致性至关重要
  * 必须遵循特定的序列
* **示例应用**：数据库迁移
  * 必须按精确顺序运行
  * 不能修改命令或添加标志
  * 确保数据迁移安全性

````markdown  theme={null}
## 数据库迁移

运行完全相同的脚本：

```bash
python scripts/migrate.py --verify --backup
```

不要修改命令或添加其他标志。
````
````

#### 1.2.5 机器人路径类比

**类比说明**：不同场景需要不同的指导策略，正如导航一样。

* **狭窄桥场景**（低自由度）：
  * 两侧都是悬崖，只有一种安全方式
  * 提供具体护栏和精确说明
  * 例如：必须按精确顺序运行的数据库迁移
* **开放田野场景**（高自由度）：
  * 没有危险，许多路径都能成功
  * 给出一般方向，相信 Claude 找到最佳路线
  * 例如：上下文决定最佳方法的代码审查

### 1.3 跨模型测试策略

#### 1.3.1 多模型兼容性测试

**核心要求**：Skill 有效性取决于底层模型，需要跨模型测试验证。

* **模型差异考虑**：
  * **Claude Haiku**（快速、经济）：需要确认提供足够指导
  * **Claude Sonnet**（平衡）：需要验证清晰高效性
  * **Claude Opus**（强大推理）：需要避免过度解释
* **测试策略**：
  * 针对 Haiku 可能需要更多细节和明确指导
  * 针对 Opus 可以简化说明，避免冗余
  * 确保在所有目标模型中都能有效工作

## 2. Skill 结构设计

### 2.1 YAML 前置事项规范

#### 2.1.1 必填字段要求

**规范要求**：SKILL.md 前置事项需要 name 和 description 两个字段。

* **name 字段规范**：
  * 最多 64 个字符
  * 只能包含小写字母、数字和连字符
  * 不能包含 XML 标签
  * 不能包含保留字："anthropic"、"claude"
* **description 字段规范**：
  * 必须非空
  * 最多 1024 个字符
  * 不能包含 XML 标签
  * 应描述 Skill 的功能和使用时机

<Note>
  **YAML 前置事项**：SKILL.md 前置事项需要两个字段：

  `name`：

  * 最多 64 个字符
  * 只能包含小写字母、数字和连字符
  * 不能包含 XML 标签
  * 不能包含保留字："anthropic"、"claude"

  `description`：

  * 必须非空
  * 最多 1024 个字符
  * 不能包含 XML 标签
  * 应描述 Skill 的功能和使用时机

  有关完整的 Skill 结构详情，请参阅[Skill 概述](/zh-CN/docs/agents-and-tools/agent-skills/overview#skill-structure)。
</Note>

### 2.2 命名约定最佳实践

#### 2.2.1 动名词形式推荐

**最佳实践**：使用动名词形式命名，清楚描述 Skill 提供的活动和能力。

* **推荐命名示例（动名词形式）**：
  * `processing-pdfs`
  * `analyzing-spreadsheets`
  * `managing-databases`
  * `testing-code`
  * `writing-documentation`
* **命名优势**：
  * 清楚描述 Skill 的活动和能力
  * 便于理解和记忆
  * 符合一致性的最佳实践

#### 2.2.2 可接受的替代方案

**替代选择**：可以使用其他命名形式，但保持一致性。

* **名词短语**：`pdf-processing`、`spreadsheet-analysis`
* **面向行动**：`process-pdfs`、`analyze-spreadsheets`
* **注意事项**：在同一个 Skill 集合中保持命名模式一致

#### 2.2.3 避免的命名模式

**命名禁忌**：避免使用模糊、通用或保留的名称。

* **模糊名称**：`helper`、`utils`、`tools`
* **通用名称**：`documents`、`data`、`files`
* **保留字**：`anthropic-helper`、`claude-tools`
* **不一致模式**：在同一个集合中使用多种命名风格

#### 2.2.4 一致命名的好处

**一致性价值**：统一的命名模式带来多重优势。

* **文档和对话引用**：更容易在交流中指代特定 Skill
* **功能快速识别**：一目了然地理解 Skill 的功能
* **组织和搜索**：便于管理和查找多个 Skill
* **专业形象**：维护专业、统一的 Skill 库

### 2.3 有效描述编写技巧

#### 2.3.1 第三人称视角要求

**核心要求**：始终使用第三人称编写描述。

* **正确示例**："处理 Excel 文件并生成报告"
* **错误示例**：
  * "我可以帮助您处理 Excel 文件"
  * "您可以使用此功能处理 Excel 文件"
* **重要性**：描述被注入到系统提示中，不一致视角会导致发现问题

<Warning>
  **始终用第三人称编写**。**重要的是**，描述被注入到系统提示中，**因此**不一致的视角可能会导致发现问题。

  * **好的**："处理 Excel 文件并生成报告"
  * **避免**："我可以帮助您处理 Excel 文件"
  * **避免**："您可以使用此功能处理 Excel 文件"
</Warning>

#### 2.3.2 具体性与关键术语

**关键原则**：描述必须具体并包含关键术语。

* **描述功能**：清楚说明 Skill 能做什么
* **使用时机**：明确指出何时应该使用该 Skill
* **关键术语**：包含相关技术词汇和触发词
* **选择机制**：帮助 Claude 从 100+ 个可用 Skill 中正确选择

#### 2.3.3 有效描述示例

**优质示例**：具体、清晰、包含使用场景。

* **PDF 处理 Skill**：
  * 功能：从 PDF 文件中提取文本和表格、填充表单、合并文档
  * 使用时机：处理 PDF 文件或用户提及 PDF、表单或文档提取时

```yaml  theme={null}
description: 从 PDF 文件中提取文本和表格、填充表单、合并文档。在处理 PDF 文件或用户提及 PDF、表单或文档提取时使用。
```

* **Excel 分析 Skill**：
  * 功能：分析 Excel 电子表格、创建数据透视表、生成图表
  * 使用时机：分析 Excel 文件、电子表格、表格数据或 .xlsx 文件时

```yaml  theme={null}
description: 分析 Excel 电子表格、创建数据透视表、生成图表。在分析 Excel 文件、电子表格、表格数据或 .xlsx 文件时使用。
```

* **Git 提交助手 Skill**：
  * 功能：通过分析 git 差异生成描述性提交消息
  * 使用时机：用户要求帮助编写提交消息或审查暂存更改时

```yaml  theme={null}
description: 通过分析 git 差异生成描述性提交消息。当用户要求帮助编写提交消息或审查暂存更改时使用。
```

#### 2.3.4 模糊描述示例

**避免示例**：过于模糊，缺乏具体信息。

```yaml  theme={null}
description: 帮助处理文档
```

```yaml  theme={null}
description: 处理数据
```

```yaml  theme={null}
description: 对文件进行各种操作
```

### 2.4 渐进式披露模式

#### 2.4.1 SKILL.md 作为导航中心

**核心理念**：SKILL.md 作为概述，指向详细材料，如目录一样。

* **认知负荷管理**：避免一次性加载过多信息
* **按需访问**：Claude 仅在需要时读取详细文件
* **性能优化**：保持 SKILL.md 在 500 行以下
* **组织原则**：有效组织说明、代码和资源

#### 2.4.2 复杂度演进可视化

##### 视觉概览：从简单到复杂

**演进过程**：从单一文件到多文件结构的逐步演进。

* **基本 Skill**：仅包含一个 SKILL.md 文件
  * 元数据和说明都在一个文件中
  * 适用于简单的功能
* **进阶 Skill**：捆绑其他内容文件
  * FORMS.md：表单填充指南
  * reference.md：API 参考
  * examples.md：使用示例
  * scripts/：可执行脚本目录

**完整的 Skill 目录结构示例**：

```
pdf/
├── SKILL.md              # 主要说明（触发时加载）
├── FORMS.md              # 表单填充指南（根据需要加载）
├── reference.md          # API 参考（根据需要加载）
├── examples.md           # 使用示例（根据需要加载）
└── scripts/
    ├── analyze_form.py   # 实用脚本（执行，不加载）
    ├── fill_form.py      # 表单填充脚本
    └── validate.py       # 验证脚本
```

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="显示 YAML 前置事项和 markdown 正文的简单 SKILL.md 文件" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="捆绑其他参考文件，如 reference.md 和 forms.md。" data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

#### 2.4.3 组织模式一：高级指南与参考

##### 模式 1：高级指南与参考

**设计理念**：基础功能在主文件，高级功能指向参考文件。

* **快速开始**：在 SKILL.md 中提供基本使用方法
* **高级功能**：链接到专门的参考文件
  * 表单填充：参阅 [FORMS.md](FORMS.md)
  * API 参考：参阅 [REFERENCE.md](REFERENCE.md)
  * 使用示例：参阅 [EXAMPLES.md](EXAMPLES.md)
* **优势**：Claude 仅在需要时加载详细文件，提高效率

````markdown  theme={null}
---
name: pdf-processing
description: 从 PDF 文件中提取文本和表格、填充表单、合并文档。在处理 PDF 文件或用户提及 PDF、表单或文档提取时使用。
---

# PDF 处理

## 快速开始

使用 pdfplumber 提取文本：
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 高级功能

**表单填充**：参阅 [FORMS.md](FORMS.md) 获取完整指南
**API 参考**：参阅 [REFERENCE.md](REFERENCE.md) 获取所有方法
**示例**：参阅 [EXAMPLES.md](EXAMPLES.md) 获取常见模式
````

#### 2.4.4 组织模式二：特定领域分组

##### 模式 2：特定领域组织

**适用场景**：多领域复杂 Skill，避免加载无关上下文。

* **组织原则**：按业务领域分组，减少无关信息干扰
* **目录结构**：
  ```
  bigquery-skill/
  ├── SKILL.md (概述和导航)
  └── reference/
      ├── finance.md (收入、计费指标)
      ├── sales.md (机会、管道)
      ├── product.md (API 使用、功能)
      └── marketing.md (活动、归因)
  ```
* **导航机制**：主文件提供数据集索引，指向具体领域文件
* **搜索优化**：使用 grep 工具快速定位特定指标

````markdown SKILL.md theme={null}
# BigQuery 数据分析

## 可用数据集

**财务**：收入、ARR、计费 → 参阅 [reference/finance.md](reference/finance.md)
**销售**：机会、管道、账户 → 参阅 [reference/sales.md](reference/sales.md)
**产品**：API 使用、功能、采用 → 参阅 [reference/product.md](reference/product.md)
**营销**：活动、归因、电子邮件 → 参阅 [reference/marketing.md](reference/marketing.md)

## 快速搜索

使用 grep 查找特定指标：

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
````
````

#### 2.4.5 组织模式三：条件详情链接

##### 模式 3：条件详情

**设计策略**：显示基本内容，按需链接高级内容。

* **基本功能**：在主文件中直接说明
* **高级功能**：提供条件性链接
  * 跟踪更改：参阅 [REDLINING.md](REDLINING.md)
  * OOXML 详情：参阅 [OOXML.md](OOXML.md)
* **优势**：用户仅在需要特定功能时才读取相关文档

```markdown  theme={null}
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。参阅 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单编辑，直接修改 XML。

**对于跟踪更改**：参阅 [REDLINING.md](REDLINING.md)
**对于 OOXML 详情**：参阅 [OOXML.md](OOXML.md)
```

### 2.5 引用结构优化

#### 2.5.1 避免深层嵌套

**关键原则**：保持引用距离 SKILL.md 一级，确保完整信息获取。

* **问题识别**：深层嵌套可能导致信息不完整
  * Claude 可能使用 `head -100` 预览，而非读取完整文件
  * 遇到嵌套引用时可能错过重要信息
* **最佳实践**：所有参考文件直接从 SKILL.md 链接
* **错误示例**：SKILL.md → advanced.md → details.md（嵌套过深）
* **正确示例**：SKILL.md 直接链接所有参考文件（一级深度）

**避免的嵌套结构**：

```markdown  theme={null}
# SKILL.md
参阅 [advanced.md](advanced.md)...

# advanced.md
参阅 [details.md](details.md)...

# details.md
这是实际信息...
```

**推荐的扁平结构**：

```markdown  theme={null}
# SKILL.md

**基本使用**：[SKILL.md 中的说明]
**高级功能**：参阅 [advanced.md](advanced.md)
**API 参考**：参阅 [reference.md](reference.md)
**示例**：参阅 [examples.md](examples.md)
```

#### 2.5.2 长文件目录结构

**最佳实践**：长文件（>100行）在顶部包含目录。

* **目录优势**：
  * 确保部分读取时也能看到完整信息范围
  * 帮助 Claude 快速定位相关内容
  * 提高信息检索效率
* **目录内容**：
  * 身份验证和设置
  * 核心方法（创建、读取、更新、删除）
  * 高级功能（批量操作、webhooks）
  * 错误处理模式
  * 代码示例

**目录结构示例**：

```markdown  theme={null}
# API 参考

## 内容
- 身份验证和设置
- 核心方法（创建、读取、更新、删除）
- 高级功能（批量操作、webhooks）
- 错误处理模式
- 代码示例

## 身份验证和设置
...

## 核心方法
...
```

## 3. 工作流设计与反馈机制

### 3.1 复杂任务工作流化

#### 3.1.1 工作流分解原则

**核心方法**：将复杂操作分解为清晰的顺序步骤。

* **分解价值**：
  * 防止遗漏关键步骤
  * 提供清晰的执行路径
  * 便于跟踪和验证进度
* **清单机制**：提供可复制的进度跟踪工具
* **适用场景**：特别复杂的多步骤流程

#### 3.1.2 无代码技能工作流示例

**示例应用**：研究综合工作流（无代码场景）

* **工作流特点**：
  * 适用于分析任务和文档处理
  * 强调系统性思考过程
  * 包含验证和质量检查环节
* **五个核心步骤**：
  1. **阅读所有源文档**：记录主要论点和支持证据
  2. **识别关键主题**：寻找跨源模式和一致性
  3. **交叉引用声明**：验证声明在源材料中的存在
  4. **创建结构化摘要**：按主题组织发现，包括支持证据和矛盾观点
  5. **验证引用**：检查每个声明的源文档引用准确性

````markdown  theme={null}
## 研究综合工作流

复制此清单并跟踪您的进度：

```
研究进度：
- [ ] 步骤 1：阅读所有源文档
- [ ] 步骤 2：识别关键主题
- [ ] 步骤 3：交叉参考声明
- [ ] 步骤 4：创建结构化摘要
- [ ] 步骤 5：验证引用
```

**步骤 1：阅读所有源文档**

查看 `sources/` 目录中的每个文档。记下主要论点和支持证据。

**步骤 2：识别关键主题**

寻找跨源的模式。哪些主题重复出现？源在哪里一致或不一致？

**步骤 3：交叉参考声明**

对于每个主要声明，验证它出现在源材料中。记下哪个源支持每个点。

**步骤 4：创建结构化摘要**

按主题组织发现。包括：
- 主要声明
- 来自源的支持证据
- 相互矛盾的观点（如果有）

**步骤 5：验证引用**

检查每个声明是否引用了正确的源文档。如果引用不完整，返回步骤 3。
````

#### 3.1.3 有代码技能工作流示例

**示例应用**：PDF 表单填充工作流（有代码场景）

* **工作流特点**：
  * 结合脚本执行和人工验证
  * 强调错误预防和反馈循环
  * 包含中间输出验证机制
* **五个执行步骤**：
  1. **分析表单**：运行分析脚本，提取字段信息
  2. **创建字段映射**：人工编辑映射文件，添加字段值
  3. **验证映射**：运行验证脚本，修复错误
  4. **填充表单**：执行填充脚本，生成输出文件
  5. **验证输出**：运行验证脚本，确保结果正确

````markdown  theme={null}
## PDF 表单填充工作流

复制此清单并在完成项目时检查：

```
任务进度：
- [ ] 步骤 1：分析表单（运行 analyze_form.py）
- [ ] 步骤 2：创建字段映射（编辑 fields.json）
- [ ] 步骤 3：验证映射（运行 validate_fields.py）
- [ ] 步骤 4：填充表单（运行 fill_form.py）
- [ ] 步骤 5：验证输出（运行 verify_output.py）
```

**步骤 1：分析表单**

运行：`python scripts/analyze_form.py input.pdf`

这提取表单字段及其位置，保存到 `fields.json`。

**步骤 2：创建字段映射**

编辑 `fields.json` 为每个字段添加值。

**步骤 3：验证映射**

运行：`python scripts/validate_fields.py fields.json`

在继续之前修复任何验证错误。

**步骤 4：填充表单**

运行：`python scripts/fill_form.py input.pdf fields.json output.pdf`

**步骤 5：验证输出**

运行：`python scripts/verify_output.py output.pdf`

如果验证失败，返回步骤 2。
````

### 3.2 反馈循环实现

#### 3.2.1 验证-修复循环模式

**核心模式**：运行验证器 → 修复错误 → 重复

* **模式价值**：显著提高输出质量和可靠性
* **循环特点**：
  * 自动化验证过程
  * 及时发现和修复错误
  - 持续改进直至满足标准
* **应用场景**：质量关键任务和高风险操作

#### 3.2.2 无代码验证循环示例

**示例应用**：风格指南合规性检查

* **验证机制**：使用 STYLE_GUIDE.md 作为验证标准
* **验证内容**：
  * 术语一致性检查
  * 示例格式验证
  * 必需部分完整性确认
* **反馈循环**：
  1. 按指南起草内容
  2. 根据清单进行审查
  3. 发现问题时记录并修复
  4. 再次审查确认修复效果
  5. 满足所有要求后完成

```markdown  theme={null}
## 内容审查流程

1. 按照 STYLE_GUIDE.md 中的指南起草您的内容
2. 根据清单审查：
   - 检查术语一致性
   - 验证示例遵循标准格式
   - 确认所有必需部分都存在
3. 如果发现问题：
   - 用特定部分参考记录每个问题
   - 修改内容
   - 再次审查清单
4. 仅当满足所有要求时才继续
5. 完成并保存文档
```

#### 3.2.3 有代码验证循环示例

**示例应用**：文档编辑流程

* **验证工具**：使用 validate.py 脚本进行自动化验证
* **关键原则**：每次更改后立即验证
* **循环流程**：
  1. 对 XML 文件进行编辑
  2. 立即运行验证脚本
  3. 验证失败时查看错误消息并修复
  4. 再次运行验证确认修复
  5. 仅在验证通过时继续下一步
  6. 重建并测试最终文档

```markdown  theme={null}
## 文档编辑流程

1. 对 `word/document.xml` 进行编辑
2. **立即验证**：`python ooxml/scripts/validate.py unpacked_dir/`
3. 如果验证失败：
   - 仔细查看错误消息
   - 修复 XML 中的问题
   - 再次运行验证
4. **仅在验证通过时继续**
5. 重建：`python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. 测试输出文档
```

## 4. 内容创作指南

### 4.1 时间敏感性处理

#### 4.1.1 避免过期信息

**核心原则**：避免包含会过时的信息。

* **问题示例**：包含具体日期的 API 使用说明
  ```markdown
  如果您在 2025 年 8 月之前执行此操作，请使用旧 API。
  2025 年 8 月之后，使用新 API。
  ```
* **风险**：时间信息会变成错误，误导用户

#### 4.1.2 旧模式分离策略

**最佳实践**：使用"旧模式"部分提供历史背景。

* **当前方法**：在主要内容中说明当前推荐做法
* **旧模式部分**：使用折叠细节提供历史信息
  * 旧版 API 说明
  * 弃用时间信息
  * 迁移指导
* **优势**：保持主内容新鲜，同时提供必要的历史背景

**推荐的文档结构**：

```markdown  theme={null}
## 当前方法

使用 v2 API 端点：`api.example.com/v2/messages`

## 旧模式

<details>
<summary>旧版 v1 API（已弃用 2025-08）</summary>

v1 API 使用：`api.example.com/v1/messages`

此端点不再受支持。
</details>
```

### 4.2 术语一致性

#### 4.2.1 统一术语选择

**核心要求**：在整个 Skill 中使用一致的术语。

* **一致性价值**：
  * 帮助 Claude 理解和遵循说明
  * 减少概念混淆
  * 提高用户体验
* **好的实践示例**：
  * 始终"API 端点"
  * 始终"字段"
  * 始终"提取"
* **避免的不一致示例**：
  * 混合"API 端点"、"URL"、"API 路由"、"路径"
  * 混合"字段"、"框"、"元素"、"控件"
  * 混合"提取"、"拉取"、"获取"、"检索"

## 5. 常见设计模式

### 5.1 模板模式

#### 5.1.1 输出格式模板化

**核心方法**：为输出格式提供模板，根据需求调整严格程度。

#### 5.1.2 严格要求模板

**适用场景**：API 响应、数据格式等严格要求场景。

* **特点**：必须使用精确的模板结构
* **内容结构**：
  * 分析标题
  * 执行摘要（关键发现概述）
  * 关键发现（带支持数据）
  * 建议（具体可行的建议）

````markdown  theme={null}
## 报告结构

始终使用此精确的模板结构：

```markdown
# [分析标题]

## 执行摘要
[关键发现的一段概述]

## 关键发现
- 带有支持数据的发现 1
- 带有支持数据的发现 2
- 带有支持数据的发现 3

## 建议
1. 具体可行的建议
2. 具体可行的建议
```
````

#### 5.1.3 灵活指导模板

**适用场景**：需要根据分析内容灵活调整的情况。

* **特点**：提供默认格式，允许根据分析调整
* **灵活性体现**：
  * 根据发现内容调整部分结构
  * 根据具体背景定制建议
  * 保持总体框架但允许局部变化

````markdown  theme={null}
## 报告结构

这是一个合理的默认格式，但根据分析使用您的最佳判断：

```markdown
# [分析标题]

## 执行摘要
[概述]

## 关键发现
[根据您发现的内容调整部分]

## 建议
[根据具体背景定制]
```

根据特定分析类型根据需要调整部分。
````
````

### 5.2 示例模式

#### 5.2.1 输入输出对演示

**核心方法**：提供输入/输出对，帮助理解风格和细节要求。

* **模式优势**：
  * 比单独描述更清楚地理解风格
  * 提供具体的格式参考
  * 展示期望的细节程度
* **应用示例**：提交消息格式规范
  * 提供多个输入输出示例
  * 展示不同的提交类型
  * 说明风格要求和格式标准

````markdown  theme={null}
## 提交消息格式

按照这些示例生成提交消息：

**示例 1：**
输入：使用 JWT 令牌添加用户身份验证
输出：
```
feat(auth): 实现基于 JWT 的身份验证

添加登录端点和令牌验证中间件
```

**示例 2：**
输入：修复日期在报告中显示不正确的错误
输出：
```
fix(reports): 修正时区转换中的日期格式

在报告生成中一致使用 UTC 时间戳
```

**示例 3：**
输入：更新依赖项并重构错误处理
输出：
```
chore: 更新依赖项并重构错误处理

- 将 lodash 升级到 4.17.21
- 跨端点标准化错误响应格式
```

遵循此风格：type(scope): 简短描述，然后详细说明。
````

### 5.3 条件工作流模式

#### 5.3.1 决策点引导

**核心方法**：通过决策点引导 Claude 选择正确的工作流。

* **决策机制**：
  * 首先确定操作类型
  * 根据类型选择对应工作流
  * 提供清晰的分支指导
* **应用场景**：复杂的多类型操作处理
* **实现方式**：
  * 使用条件判断语句
  * 提供明确的分支路径
  * 为每个工作流提供详细步骤

```markdown  theme={null}
## 文档修改工作流

1. 确定修改类型：

   **创建新内容？** → 遵循下面的"创建工作流"
   **编辑现有内容？** → 遵循下面的"编辑工作流"

2. 创建工作流：
   - 使用 docx-js 库
   - 从头开始构建文档
   - 导出为 .docx 格式

3. 编辑工作流：
   - 解包现有文档
   - 直接修改 XML
   - 每次更改后验证
   - 完成时重新打包
```

<Tip>
  如果工作流变得很大或复杂，有许多步骤，考虑将它们推送到单独的文件中，并告诉 Claude 根据任务读取适当的文件。
</Tip>

## 6. 评估与迭代开发

### 6.1 评估驱动开发

#### 6.1.1 先评估后文档

**核心原则**：在编写大量文档之前创建评估。

* **方法价值**：
  * 确保 Skill 解决真实问题
  * 避免记录想象的问题
  * 基于实际需求进行开发
* **开发流程**：
  1. **识别差距**：运行 Claude 处理代表性任务，记录失败和缺失上下文
  2. **创建评估**：构建三个场景测试这些差距
  3. **建立基线**：测量无 Skill 的 Claude 性能
  4. **编写最少说明**：创建足够内容解决差距并通过评估
  5. **迭代改进**：执行评估，与基线比较并持续改进

#### 6.1.2 评估结构示例

**评估构成**：包含技能、查询、文件和预期行为。

* **评估示例**：
  * 技能：["pdf-processing"]
  * 查询：从此 PDF 文件中提取所有文本并将其保存到 output.txt
  * 文件：["test-files/document.pdf"]
  * 预期行为：
    * 成功读取 PDF 文件
    * 提取所有页面文本内容
    * 保存为格式清晰的文本文件

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "从此 PDF 文件中提取所有文本并将其保存到 output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "使用适当的 PDF 处理库或命令行工具成功读取 PDF 文件",
    "从文档中的所有页面提取文本内容，不遗漏任何页面",
    "将提取的文本保存到名为 output.txt 的文件中，格式清晰易读"
  ]
}
```

<Note>
  此示例演示了具有简单测试标准的数据驱动评估。我们目前不提供运行这些评估的内置方式。用户可以创建自己的评估系统。**重要的是**，评估是衡量 Skill 有效性的真实来源。
</Note>

### 6.2 与 Claude 协作迭代

#### 6.2.1 双角色协作模式

**核心方法**：使用两个 Claude 实例协作开发 Skill。

* **角色分工**：
  * **Claude A**：帮助设计和改进说明的专家
  * **Claude B**：使用 Skill 执行真实工作的代理
* **协作优势**：
  * Claude 理解如何编写有效说明和代理需求
  * 真实任务测试验证 Skill 实用性
  * 基于观察行为而非假设进行改进

#### 6.2.2 新技能创建流程

**七个步骤创建新 Skill**：

1. **无 Skill 完成任务**：使用常规提示解决问题，注意重复提供的信息
2. **识别可重用模式**：识别对未来任务有用的上下文模式
3. **要求 Claude A 创建 Skill**：让 Claude 根据观察到的模式生成 Skill
4. **审查简洁性**：检查是否添加了不必要的解释
5. **改进信息架构**：要求更有效地组织内容
6. **在类似任务上测试**：使用 Claude B 测试相关用例
7. **根据观察迭代**：基于 Claude B 的表现进行针对性改进

#### 6.2.3 现有技能迭代流程

**持续改进的协作循环**：

* **协作模式**：在三个角色间循环
  * 与 Claude A 合作（改进 Skill 的专家）
  * 与 Claude B 测试（执行真实工作的代理）
  * 观察 Claude B 行为并将见解带回 Claude A
* **迭代步骤**：
  1. **真实工作流测试**：给 Claude B 实际任务
  2. **行为观察**：记录困难、成功和意外选择
  3. **专家分析**：向 Claude A 分享观察并请求改进建议
  4. **改进应用**：使用 Claude A 的建议更新 Skill
  5. **重复测试**：在类似请求上再次测试
  6. **持续循环**：遇到新场景时继续改进

#### 6.2.4 团队反馈整合

**反馈收集方法**：

1. **分享观察**：与队友分享 Skill 并观察使用情况
2. **关键问题**：
   * Skill 在预期时激活吗？
   * 说明清楚吗？
   * 缺少什么？
3. **盲点识别**：合并反馈解决自己使用模式中的盲点

#### 6.2.5 协作模式有效性原理

**方法有效的根本原因**：

* **Claude A 理解代理需求**：知道代理需要什么信息
* **用户提供领域专业知识**：贡献专业知识和经验
* **Claude B 通过真实使用揭示差距**：展示实际问题和改进空间
* **基于观察的迭代改进**：根据真实行为而非假设改进 Skill

### 6.3 导航行为观察

#### 6.3.1 使用模式分析

**观察重点**：Claude 在实践中如何使用 Skill。

* **关键观察指标**：
  * **意外的探索路径**：文件读取顺序与预期不符
  * **错过的连接**：未能遵循重要文件引用
  * **对某些部分的过度依赖**：反复读取同一文件
  * **忽略的内容**：从不访问的捆绑文件
* **观察价值**：
  * 识别结构不直观的问题
  * 发现链接需要更明确的地方
  * 确定内容应该放在主文件中的部分
  * 识别不必要的或信号不良的内容
* **迭代原则**：基于观察而非假设进行改进

* **元数据重要性**：name 和 description 字段特别关键
  * Claude 使用这些字段决定是否触发 Skill
  * 必须清楚描述功能和使用时机

## 7. 反模式识别与避免

### 7.1 路径规范问题

#### 7.1.1 路径分隔符统一

**核心原则**：始终使用正斜杠，确保跨平台兼容性。

* **正确做法**：`scripts/helper.py`、`reference/guide.md`
* **错误做法**：`scripts\helper.py`、`reference\guide.md`
* **兼容性考虑**：
  * Unix 风格路径在所有平台都有效
  * Windows 风格路径在 Unix 系统上会导致错误

### 7.2 选择过多问题

#### 7.2.1 默认值优先原则

**核心原则**：除非必要，否则不要呈现多种方法。

* **问题示例**：令人困惑的多种选择
  ```
  您可以使用 pypdf、或 pdfplumber、或 PyMuPDF、或 pdf2image、或...
  ```
* **最佳实践**：提供默认值和逃生舱口
  * 主要方法：使用 pdfplumber 进行文本提取
  * 特殊情况：需要 OCR 的扫描 PDF 改用 pdf2image 与 pytesseract

````markdown  theme={null}
**不好的例子：太多选择**（令人困惑）：
"您可以使用 pypdf、或 pdfplumber、或 PyMuPDF、或 pdf2image、或..."

**好的例子：提供默认值**（带有逃生舱口）：
"使用 pdfplumber 进行文本提取：
```python
import pdfplumber
```

对于需要 OCR 的扫描 PDF，改用 pdf2image 与 pytesseract。"
````
````

## 8. 高级实现：可执行代码集成

### 8.1 错误处理策略

#### 8.1.1 解决而非推卸原则

**核心原则**：编写 Skill 脚本时处理错误条件，而不是推卸给 Claude。

* **好的实践**：明确处理错误
  * 文件不存在时创建默认文件
  * 权限错误时提供替代方案
  * 提供有用的错误信息
* **不好的实践**：简单推卸给 Claude
  * 直接失败并让 Claude 弄清楚
  * 不提供任何错误处理或指导

**错误处理示例**：

```python  theme={null}
def process_file(path):
    """处理文件，如果不存在则创建它。"""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # 创建具有默认内容的文件而不是失败
        print(f"文件 {path} 未找到，创建默认值")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # 提供替代方案而不是失败
        print(f"无法访问 {path}，使用默认值")
        return ''
```

#### 8.1.2 参数文档化

**核心要求**：配置参数应该被证明和记录，避免"巫毒常数"。

* **问题根源**：如果不知道正确值，Claude 如何确定它？
* **好的实践**：自文档化参数
  * 说明参数选择的原因
  * 提供决策背景
  * 包含性能和可靠性考虑

**参数文档化示例**：

```python  theme={null}
# HTTP 请求通常在 30 秒内完成
# 更长的超时考虑了慢速连接
REQUEST_TIMEOUT = 30

# 三次重试平衡可靠性与速度
# 大多数间歇性故障在第二次重试时解决
MAX_RETRIES = 3
```

**避免的魔法数字**：

```python  theme={null}
TIMEOUT = 47  # 为什么是 47？
RETRIES = 5   # 为什么是 5？
```

### 8.2 实用脚本优势

#### 8.2.1 预制脚本价值

**核心价值**：预制脚本比生成的代码更可靠。

* **四大优势**：
  * **比生成的代码更可靠**：经过测试和验证
  * **节省令牌**：无需在上下文中包含代码
  * **节省时间**：无需代码生成过程
  * **确保一致性**：跨使用保持统一行为

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="将可执行脚本与说明文件捆绑在一起" data-og-width="2048" width="2048" data-og-height="1154" height="1153" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

#### 8.2.2 执行与引用区分

**重要区别**：明确说明 Claude 应该执行脚本还是作为参考读取。

* **执行脚本**（最常见）："运行 `analyze_form.py` 来提取字段"
* **作为参考读取**（复杂逻辑）："参阅 `analyze_form.py` 了解字段提取算法"
* **选择原则**：大多数实用脚本优先选择执行，因为更可靠和高效

#### 8.2.3 脚本文档示例

**实用脚本文档结构**：

* **脚本功能说明**：清楚描述每个脚本的作用
* **使用方法**：提供具体的执行命令
* **输出格式**：说明脚本的输出结构和格式

````markdown  theme={null}
## 实用脚本

**analyze_form.py**：从 PDF 中提取所有表单字段

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

输出格式：
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**：检查重叠的边界框

```bash
python scripts/validate_boxes.py fields.json
# 返回："OK"或列出冲突
```

**fill_form.py**：将字段值应用于 PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
````
`````

### 8.3 视觉分析集成

#### 8.3.1 图像输入处理

**核心方法**：当输入可以呈现为图像时，让 Claude 进行视觉分析。

* **应用场景**：表单布局分析、文档理解、图像处理
* **处理流程**：
  1. 将文档转换为图像格式
  2. Claude 分析页面图像识别元素
  3. 利用视觉能力理解布局和结构

````markdown  theme={null}
## 表单布局分析

1. 将 PDF 转换为图像：
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. 分析每个页面图像以识别表单字段
3. Claude 可以在视觉上看到字段位置和类型
````
`````

<Note>
  在此示例中，您需要编写 `pdf_to_images.py` 脚本。
</Note>

### 8.4 验证机制设计

#### 8.4.1 计划-验证-执行模式

**核心方法**：通过创建中间计划文件并进行验证来及早捕获错误。

* **问题背景**：复杂开放式任务中 Claude 可能犯错
* **解决方案**：计划-验证-执行模式
  1. Claude 创建结构化计划
  2. 脚本验证计划的正确性
  3. 执行验证通过的计划
* **示例场景**：根据电子表格更新 PDF 中的 50 个表单字段
  * 风险：引用不存在字段、创建冲突值、遗漏必需字段
  * 解决：添加中间 `changes.json` 文件进行验证

#### 8.4.2 模式有效性原理

**四个关键优势**：

* **及早捕获错误**：验证在更改应用前发现问题
* **机器可验证**：脚本提供客观验证标准
* **可逆计划**：Claude 可以迭代计划而不影响原件
* **清晰调试**：错误消息指向特定问题

**适用场景**：
* 批量操作
* 破坏性更改
* 复杂验证规则
* 高风险操作

**实现提示**：使用详细验证脚本和特定错误消息，帮助 Claude 修复问题。

### 8.5 依赖管理

#### 8.5.1 平台特定限制

**核心认知**：不同平台有不同的包管理能力。

* **claude.ai 平台**：
  * 可以从 npm 和 PyPI 安装包
  * 可以从 GitHub 存储库拉取
* **Anthropic API 平台**：
  * 没有网络访问权限
  * 没有运行时包安装
* **实践要求**：
  * 在 SKILL.md 中列出所需包
  * 验证包在目标平台可用性

### 8.6 运行时环境理解

#### 8.6.1 文件系统架构

**核心架构**：基于文件系统的渐进式披露机制。

**Claude 访问 Skill 的方式**：

1. **元数据预加载**：启动时加载所有 Skill 的名称和描述
2. **按需读取文件**：使用 bash 读取工具访问 SKILL.md 和其他文件
3. **高效执行脚本**：通过 bash 执行脚本，无需加载完整内容
4. **大文件无上下文惩罚**：参考文件在实际读取前不消耗令牌

#### 8.6.2 创作实践指导

* **文件路径重要性**：使用正斜杠导航目录结构
* **描述性命名**：使用指示内容的名称
* **领域组织**：按域或功能组织目录
* **资源捆绑**：包括完整文档、示例、数据集
* **脚本优先**：对确定性操作优先使用预制脚本
* **明确执行意图**：清楚说明是执行还是引用

**架构示例**：

```
bigquery-skill/
├── SKILL.md (概述，指向参考文件)
└── reference/
    ├── finance.md (收入指标)
    ├── sales.md (管道数据)
    └── product.md (使用分析)
```

**工作原理**：用户询问收入时，Claude 读取 SKILL.md，看到对 `reference/finance.md` 的参考，仅读取该文件。其他文件保留在文件系统上，不消耗令牌。

### 8.7 MCP 工具集成

#### 8.7.1 完全限定名称

**核心要求**：始终使用完全限定的工具名称。

* **格式**：`ServerName:tool_name`
* **示例**：
  * `BigQuery:bigquery_schema` 工具检索表架构
  * `GitHub:create_issue` 工具创建问题
* **组成部分**：
  * `BigQuery` 和 `GitHub`：MCP 服务器名称
  * `bigquery_schema` 和 `create_issue`：服务器中的工具名称
* **重要性**：没有服务器前缀，Claude 可能无法定位工具

### 8.8 依赖假设避免

#### 8.8.1 明确依赖说明

**核心原则**：不假设包可用，明确说明依赖。

* **不好的做法**：假设安装
  ```
  使用 pdf 库来处理文件。
  ```
* **好的做法**：明确依赖
  ```
  安装所需的包：`pip install pypdf`

  然后使用它：
  ```python
  from pypdf import PdfReader
  reader = PdfReader("file.pdf")
  ```
  ```

````markdown  theme={null}
**不好的例子：假设安装**：
"使用 pdf 库来处理文件。"

**好的例子：明确关于依赖项**：
"安装所需的包：`pip install pypdf`

然后使用它：
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````
````

## 9. 技术规范说明

### 9.1 YAML 前置事项要求

#### 9.1.1 字段验证规则

**核心规范**：SKILL.md 前置事项需要 name 和 description 字段。

* **name 字段规则**：
  * 最多 64 个字符
  * 仅小写字母/数字/连字符
  * 无 XML 标签
  * 无保留字
* **description 字段规则**：
  * 最多 1024 个字符
  * 非空
  * 无 XML 标签

### 9.2 令牌预算管理

#### 9.2.1 内容长度限制

**性能要求**：保持 SKILL.md 正文在 500 行以下。

* **优化方法**：使用渐进式披露模式拆分长内容
* **架构支持**：基于文件系统的架构支持内容拆分

## 10. 质量检查清单

### 10.1 核心质量标准

#### 10.1.1 内容质量验证

**核心质量检查项目**：

* [ ] 描述具体并包含关键术语
* [ ] 描述包括 Skill 的功能和使用时机
* [ ] SKILL.md 正文在 500 行以下
* [ ] 其他详情在单独的文件中（如果需要）
* [ ] 没有时间敏感信息（或在"旧模式"部分中）
* [ ] 整个 Skill 中术语一致
* [ ] 示例具体，不抽象
* [ ] 文件引用一级深
* [ ] 适当使用渐进式披露
* [ ] 工作流有清晰的步骤

### 10.2 代码质量标准

#### 10.2.1 脚本质量要求

* [ ] 脚本解决问题而不是推卸给 Claude
* [ ] 错误处理明确且有帮助
* [ ] 没有"巫毒常数"（所有值都有理由）
* [ ] 所需的包在说明中列出并验证为可用
* [ ] 脚本有清晰的文档
* [ ] 没有 Windows 风格的路径（所有正斜杠）
* [ ] 关键操作的验证/验证步骤
* [ ] 包含质量关键任务的反馈循环

### 10.3 测试覆盖标准

#### 10.3.1 多模型测试

* [ ] 至少创建了三个评估
* [ ] 使用 Haiku、Sonnet 和 Opus 进行了测试
* [ ] 使用真实使用场景进行了测试
* [ ] 合并了团队反馈（如果适用）

## 11. 学习资源与后续步骤

### 11.1 入门指南

<CardGroup cols={2}>
  <Card title="开始使用代理 Skill" icon="rocket" href="/zh-CN/docs/agents-and-tools/agent-skills/quickstart">
    创建您的第一个 Skill
  </Card>

  <Card title="在 Claude Code 中使用 Skill" icon="terminal" href="/zh-CN/docs/claude-code/skills">
    在 Claude Code 中创建和管理 Skill
  </Card>

  <Card title="在代理 SDK 中使用 Skill" icon="cube" href="/zh-CN/api/agent-sdk/skills">
    在 TypeScript 和 Python 中以编程方式使用 Skill
  </Card>

  <Card title="使用 API 使用 Skill" icon="code" href="/zh-CN/api/skills-guide">
    以编程方式上传和使用 Skill
  </Card>
</CardGroup>