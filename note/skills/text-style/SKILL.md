---
name: text-style
description: |
  为指定的文字内容应用 HTML/CSS 样式，使用 <span> 标签包裹并根据用户要求设置 style 属性。
  当用户提到"文字颜色"、"字体大小"、"字体样式"、"文字样式"、"文本样式"、"高亮"、"加粗"、"颜色"等样式相关需求时触发。
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Edit
---

# Text Style Skill

为指定的文字内容应用 HTML/CSS 样式，使用 `<span>` 标签包裹并设置相应的 style 属性。

## 核心原则

1. **引号必须使用 ASCII 英文引号** - HTML/CSS 只能识别英文引号 `”` 或 `’`，中文引号 `””` 或 `’’` 会导致代码无效
2. **语法严格性** - 生成符合 HTML/CSS 规范的代码
3. **智能识别** - 根据用户的自然语言描述，映射到对应的 CSS 属性

## CSS 属性映射表

| 用户要求示例 | CSS 属性 | 示例输出 |
|------------|---------|---------|
| "红色"、"红色文字"、"文字变红" | `color: red;` | `<span style="color: red;">文本</span>` |
| "黄色背景"、"背景黄色" | `background-color: yellow;` | `<span style="background-color: yellow;">文本</span>` |
| "16像素"、"字体16px"、"字号16" | `font-size: 16px;` | `<span style="font-size: 16px;">文本</span>` |
| "Arial字体"、"使用Arial" | `font-family: Arial;` | `<span style="font-family: Arial;">文本</span>` |
| "加粗"、"粗体"、"font-weight bold" | `font-weight: bold;` | `<span style="font-weight: bold;">文本</span>` |
| "字母间距2px"、"字间距2px" | `letter-spacing: 2px;` | `<span style="letter-spacing: 2px;">文本</span>` |
| "单词间距4px"、"词间距4px" | `word-spacing: 4px;` | `<span style="word-spacing: 4px;">文本</span>` |
| "首行缩进20px"、"缩进20" | `text-indent: 20px;` | `<span style="text-indent: 20px;">文本</span>` |
| "全部大写"、"转大写"、"uppercase" | `text-transform: uppercase;` | `<span style="text-transform: uppercase;">文本</span>` |
| "不换行"、"单行显示" | `white-space: nowrap;` | `<span style="white-space: nowrap;">文本</span>` |
| "半透明"、"透明度50%" | `opacity: 0.5;` | `<span style="opacity: 0.5;">文本</span>` |
| "黑色边框"、"1px边框" | `border: 1px solid black;` | `<span style="border: 1px solid black;">文本</span>` |
| "内边距5px"、"padding 5px" | `padding: 5px;` | `<span style="padding: 5px;">文本</span>` |
| "圆角5px"、"圆角" | `border-radius: 5px;` | `<span style="border-radius: 5px;">文本</span>` |
| "行高1.5倍"、"line-height 1.5" | `line-height: 1.5;` | `<span style="line-height: 1.5;">文本</span>` |

## 颜色值支持

支持多种颜色表达方式：
- **颜色名称**: `red`, `blue`, `green`, `yellow`, `black`, `white`, `gray`, `orange`, `purple`, `pink`, `brown` 等
- **十六进制**: `#FF0000`, `#00FF00`, `#0000FF`
- **RGB**: `rgb(255, 0, 0)`
- **RGBA**: `rgba(255, 0, 0, 0.5)`

## 常见样式组合

### 高亮效果
`<span style="background-color: yellow;">被高亮的文本</span>`

### 红色加粗
`<span style="color: red; font-weight: bold;">红色加粗文本</span>`

### 大字体 + 加粗
`<span style="font-size: 24px; font-weight: bold;">大号加粗文本</span>`

### 卡片式效果
`<span style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">卡片内容</span>`

## 工作流程

1. **识别目标文本** - 确定需要应用样式的文本内容
2. **解析用户需求** - 根据用户的自然语言描述，识别需要的 CSS 属性
3. **生成 span 标签** - 创建带有正确 style 属性的 `<span>` 标签
4. **验证输出语法** - 确保生成的 HTML/CSS 代码使用英文引号，符合 Web 标准
5. **应用样式** - 用生成的 span 标签包裹目标文本

## 范围边界

- ✅ 处理基本的 CSS 样式属性（颜色、字体、间距、边框等）
- ✅ 支持多个样式属性组合
- ❌ 不处理 CSS 动画（transition、@keyframes）
- ❌ 不处理响应式设计（@media、flexbox、grid）
- ❌ 不处理 JavaScript 交互
- ❌ 不修改 HTML 结构，只添加 span 标签和 style 属性

## 注意事项

- 始终使用英文引号 `"` 或 `'` 包裹 style 属性值
- 输出纯文本 HTML，不要包裹在代码块（```）或其他格式中
- 多个样式属性用分号 `;` 分隔
- 属性名和属性值用冒号 `:` 分隔
- 保持属性的简洁性，只添加用户明确要求的样式
- 如果用户没有指定具体值，使用合理的默认值

## 示例对话

**用户**: 把这段文字"重要提示"改成红色加粗

**输出**: `<span style="color: red; font-weight: bold;">重要提示</span>`

---

**用户**: 给"注意事项"加上黄色背景

**输出**: `<span style="background-color: yellow;">注意事项</span>`

---

**用户**: 让"标题"使用 20px 的 Arial 字体

**输出**: `<span style="font-size: 20px; font-family: Arial;">标题</span>`
