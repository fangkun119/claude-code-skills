# Phase 3 文档改写执行路径说明

## 概述

Phase 3 在独立上下文的 Sub Agent 中执行，包含三个子步骤：
1. 确定执行方式
2. 文档图片预处理
3. 文档重写（两种执行路径）

关于 (1) 确定执行方式 和 (2) 文档图片预处理的详细说明，参见 SKILL.md 的 Phase 3 章节。本参考文档专注于 (3) 文档重写的两条执行路径——Option A 与 Option B 的详细操作说明。

## Option A：保持原文章节顺序

**适用场景**：原文的章节组织合理，只需优化各章内容。

### Operation 1：章拆分

由一个独立 Sub Agent 完成，对 `{rewritten_file_path}` 进行章节划分。

**执行前使用第一性原理思考**：在不更改正文内容和顺序的前提下（仅通过添加/修改/删除章标题 `## {n}.` 来拆分），如何划分章节能帮助读者——

1. 确定文档的主题边界与覆盖范围
2. 建立主题之间的逻辑关系
3. 为不同读者提供最粗粒度的导航入口

按思考结论制定计划并执行。

### Operation 2：逆序逐一改写

由一个调度 Sub Agent 管理，按**从下到上逆序**为每章创建一个独立 Sub Agent 执行改写。

**逆序执行设计动机**：避免后续章节改写时上下文漂移导致前面的章节与已改写的后面章节风格不一致；先改后面的章节，前面章节的 Sub Agent 能参考已改写部分的风格参照。

**关于章节编号**：`spec_{chapter_number}.md` 中的 `{chapter_number}` 指**该章在文档中的位置编号**（即章标题 `## {n}.` 中的 `n`，从 1 递增），与改写的执行顺序无关。例如文档有 3 章，逆序改写顺序是 3 → 2 → 1，但生成的规格文件始终是 `spec_1.md`、`spec_2.md`、`spec_3.md`（按位置编号）。

负责各章的 Sub Agent 执行两步：

1. **Step 1 — 产出规格**：结合本章内容，在遵守 System Rules 的前提下，判断 `{initial_requirements}` 和 `{workspace_directory}/requirements.md` 中哪些需求与本章相关、如何改写。将规格保存至 `{workspace_directory}/spec_{chapter_number}.md`（`{chapter_number}` 为 Operation 1 章拆分后各章的序号，从 1 递增）。

   规格中须包含本章的**写作结构方案**——即内容以何种逻辑顺序与层次关系组织（如因果递进、问题驱动、概念分层、结论先行等），以最有效地向目标读者传达本章内容。可使用成熟的写作框架，也可自行设计结构，选择时须确保：
   - ① 适合单章改写的粒度
   - ② 符合 `{workspace_directory}/requirements.md` 中的需求设定
   - ③ 与本章内容匹配

2. **Step 2 — 执行改写**：参考 `{workspace_directory}/spec_{chapter_number}.md` 完成本章改写。

   文档中图片下方附有 Markdown 注释（由 (2) 文档图片预处理步骤添加），记录了图片的路径、用途和内容描述，改写时可参考这些注释理解图片内容。

   若工作量较大，该 Sub Agent 可自行决定进一步拆分子任务到更多 Sub Agent 串行完成以节省上下文。

## Option B：重排章节顺序

**适用场景**：原文的章节组织需要重组，可能涉及合并、拆分、重排章节。

以下三个 Operation 在一个拥有独立上下文的 Sub Agent 中串行执行。

### Operation 1：改写结果规格分析

启动独立上下文的 Sub Agent 完成：

1. 用第一性原理思考：要达成 `{initial_requirements}` 和 `{workspace_directory}/requirements.md` 中的要求，`{rewritten_file_path}` 应改写成什么样子？
2. 将分析结果保存为规格文档 `{workspace_directory}/spec.md`，内容须足够清晰，使无相关上下文的 Sub Agent 也能独立使用。
3. **审慎原则**：不假设用户已完全清楚自己想要什么。若动机和目标不清晰，停下来与用户讨论；若目标清晰但路径非最优，告知用户并建议更好的方案。

### Operation 2：任务拆分与计划制定

启动独立上下文的 Sub Agent 完成整个任务拆分和计划制定：

1. 以 `{workspace_directory}/spec.md` 为准，参考 `{initial_requirements}` 和 `{workspace_directory}/requirements.md`，制定执行计划。
2. 执行计划应分为若干步骤，依次为每个步骤生成步骤描述，存放在 `{workspace_directory}/step_{step_number}.md`，内容应包含：
   - **(a) 输出目标**：即写出什么样的一段内容
   - **(b) 内容来源**：即这一步的改写内容来自原文的哪些部分
   - **(c) 写作结构方案**：即以何种逻辑顺序与层次关系组织（如因果递进、问题驱动、概念分层、结论先行等）来最有效地向目标读者传达信息。可使用成熟的写作框架，也可自行设计结构。选择结构方案时须确保：
     - ① 符合 `{workspace_directory}/requirements.md` 中的需求设定
     - ② 与该步骤负责改写的文档内容相匹配
   - **(d) 清晰度要求**：内容要足够清晰，使无相关上下文的 Sub Agent 也能独立使用
3. 将整个计划完整记录在 `{workspace_directory}/plan.md` 中，包含所有步骤的任务目标描述以及对应的 `{workspace_directory}/step_{step_number}.md` 引用。

### Operation 3：计划执行

启动独立上下文的 Sub Agent 负责调度。这个调度 Sub Agent 对 `{workspace_directory}/plan.md` 中的每一步执行如下操作：

1. 以这一步的提示词和 `{workspace_directory}/step_{step_number}.md` 为主，以 `{initial_requirements}` 和 `{workspace_directory}/requirements.md` 作为辅助和参考，来生成提示词，创建一个拥有独立上下文用于执行的 Sub Agent。
   
   **每个步骤使用一个独立执行 Sub Agent**——是为了节省上下文，让每个步骤都有充足的上下文，保持执行效果和质量。

2. 负责执行的 Sub Agent，基于调度 Agent 给它的提示词以及 `{workspace_directory}/step_{step_number}.md` 中的步骤描述，完成这一步的改写。

3. 负责执行的 Sub Agent，在处理文中的图片时，可以借助图片上方或下方的 Markdown 注释（由 (2) 文档图片预处理步骤添加，包含图片路径、用途、内容描述）作为参考理解图片内容，从而避免花费上下文进行图像理解。

## 并发控制规则（Option A 和 Option B 共用）

Phase 3 中可能同时拆分出多个 Sub Agent。为避免触发大模型 API 并发度限制，多个 Sub Agent 必须 **2 个 2 个地分配运行**——即同时最多 2 个 Sub Agent 在执行，待其中一组完成后再启动下一组。
