```json
{
  "document_purposes": {
    "clarification_question": "改写后的文档将用于哪些场景？",
    "answers": [
      "AI 编程教程（精炼实用）",
      "项目快速参考手册",
      "项目 Check List"
    ]
  },
  "audience_and_needs": {
    "clarification_question": "改写后的文档面向哪些读者？他们各自的核心诉求是什么？",
    "answers": [
      "初学 AI 编程工程师（结合案例系统全面掌握）",
      "熟练 AI 编程工程师（快速回顾方法论、查看check list）"
    ]
  },
  "rewriter_personas": {
    "clarification_question": "改写时应扮演什么角色身份？该角色擅长什么？",
    "answers": [
      "资深 AI 编程方法论讲师（把方法论讲透，方法论提炼强）",
      "Claude Code 实战架构师（熟悉文中的技术栈，讲清实操细节）",
      "技术教程写作专家（把抽象方法论拆成清晰可执行步骤与表格）",
      "企业级项目导师（结合企业项目场景，讲清落地与团队协作）"
    ]
  },
  "writing_style": {
    "clarification_question": "改写后的文档应采用怎样的表达风格？",
    "answers": [
      "精炼实用，结构清晰，条目化呈现",
      "方法论手册风 + 实战教材风（第一部分速查，第二部分解释 why）",
      "保留实战感",
      "图表化关键流程与决策（Mermaid 流程图、表格、对比）"
    ]
  },
  "hard_constraints": {
    "clarification_question": "改写过程中有哪些不可违反的硬性规则？",
    "answers": [
      "不丢关键信息",
      "实战紧扣文中使用的技术栈，避免空谈理论",
      "方法论表述必须具体可操作，不设虚泛口号",
      "Code block里面的东西不要改写",
      "要分辨是不是代码、命令行输出、配置示例、提示词、Ascii或Mermaid图，这些内容都要放在 Markdown 的 Code Block 中、而不是使用普通正文格式",
      "不要使用'课程'、'第n讲'这样的课程表述，改成'系列'、'第n篇'等文章表述",
      "将第一人称表述改成第三人称表述"
    ]
  },
  "additional_clarifications": {
    "clarification_question": "还有其他需要澄清的问题吗？",
    "answers": [
      "两部分结构按需拆分：第一部分方法论提炼（前几章）；第二部分实战演示（后几章）",
      "第一部分加一份可裁剪的 Check List，供项目阶段快速查阅",
      "在开头加一张全文导读地图（Mermaid），帮两类不同的读者快速定位章节"
    ]
  },
  "user_initial_requirements_summary": {
    "goal": "制作一篇精炼实用的 AI 编程教程",
    "audience": "学习 AI 编程的工程师，想掌握 AI 编程方法论、具备指导 AI 做项目的架构思维",
    "structure": "两部分：第一部分方法论提炼（前 1-2 章，参考手册风，不深入技术栈）；第二部分实战演示（后续章节，结合原文例子、技术栈、项目背景复现项目过程，深入解释 why）",
    "content_focus": "围绕 AI 编程方法论，主导思考什么内容是高价值的，进行内容选择和组织"
  }
}
```
