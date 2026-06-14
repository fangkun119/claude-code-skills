---
name: md-img-to-html
description: |
  将 Markdown 格式的图片转换为 HTML <img> 标签格式。支持 wikilink 格式 (![[路径]]) 和标准 Markdown 格式 (![alt](路径))。
  支持宽度参数（如 |600px）并保持替换文字。当用户提到"转换图片为 HTML"、"Markdown 图片转 HTML"、"img 标签"、"图片格式转换"时触发。
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# Markdown 图片转 HTML Skill

将文档中的所有 Markdown 格式图片转换为 HTML `<img>` 标签格式。

## 支持的 Markdown 图片格式

### Wikilink 格式
- `![[图片路径]]` - 基本格式
- `![[图片路径|宽度]]` - 带宽度参数

### 标准 Markdown 格式
- `![替换文字](图片路径)` - 基本格式
- `![替换文字|宽度](图片路径)` - 带宽度参数

## 转换规则

### 基本转换
**输入**: `![[图片路径]]` 或 `![替换文字](图片路径)`

**输出**: `<img src="图片路径" style="display: block; width: 100%;" alt="替换文字">`

注意：
- Wikilink 格式没有替换文字，alt 为空字符串 `""`
- 未指定宽度时，默认 `width: 100%`
- `display: block;` 确保图片独占一行

### 带宽度的转换
**输入**: `![[图片路径|600px]]` 或 `![替换文字|600px](图片路径)`

**输出**: `<img src="图片路径" style="display: block; width: 600px;" alt="替换文字">`

注意：
- 从 `|600px` 提取宽度值
- 将宽度值直接应用到 style 的 width 属性

### 边界情况处理

| 输入格式 | 替换文字 (alt) | 宽度 (width) |
|---------|---------------|-------------|
| `![[路径]]` | `""` | `100%` |
| `![[路径\|600px]]` | `""` | `600px` |
| `![文本](路径)` | `"文本"` | `100%` |
| `![文本\|600px](路径)` | `"文本"` | `600px` |
| `![](路径)` | `""` | `100%` |

## 工作流程

**重要**: 必须按照从下到上的逆序处理图片，避免修改影响位置索引。

### 步骤 1: 分析文件

1. **读取文件内容** - 使用 Read 工具读取目标 Markdown 文件
2. **识别所有图片** - 扫描文件中的所有 Markdown 图片格式
3. **提取图片信息** - 对每个图片记录：
   - **位置** - 在文件中的起始位置（行号和字符位置）
   - **原始格式** - 完整的 Markdown 图片语法
   - **图片路径** - src 值
   - **替换文字** - alt 值（可能为空）
   - **宽度** - 像素值或百分比（未指定则为 100%）
   - **图片格式类型** - wikilink 或标准 Markdown

### 步骤 2: 列出转换计划

在开始修改前，向用户展示找到的所有图片及其转换计划：

```
找到 N 个 Markdown 图片：

1. [第 X 行] ![[path/to/image.png|600px]]
   → <img src="path/to/image.png" style="display: block; width: 600px;" alt="">

2. [第 Y 行] ![Logo](./assets/logo.png)
   → <img src="./assets/logo.png" style="display: block; width: 100%;" alt="Logo">

...
```

### 步骤 3: 逆序执行转换

按在文件中出现的**从下到上**的顺序执行转换：

1. **从最后一个图片开始** - 处理位置最靠后的图片
2. **执行替换** - 使用 Edit 工具将原始 Markdown 图片替换为 HTML 标签
3. **继续向上** - 处理倒数第二个，依此类推
4. **完成** - 直到处理完第一个图片

**为什么逆序？** 先修改下面的图片，不会改变上面图片在文件中的位置，确保之前列出的计划依旧可行。

### 步骤 4: 验证结果

转换完成后：
1. 确认所有图片都已转换
2. 检查 HTML 标签格式正确
3. 验证 alt、width、src 属性符合预期

## 转换示例

### 示例 1: Wikilink 无宽度
**原文**:
```markdown
这是图片

![[assets/diagram.png]]

后面的内容
```

**转换后**:
```markdown
这是图片

<img src="assets/diagram.png" style="display: block; width: 100%;" alt="">

后面的内容
```

### 示例 2: 标准格式带宽度
**原文**:
```markdown
# 系统架构

![架构图|800px](./docs/architecture.png)

如图所示...
```

**转换后**:
```markdown
# 系统架构

<img src="./docs/architecture.png" style="display: block; width: 800px;" alt="架构图">

如图所示...
```

### 示例 3: 混合格式
**原文**:
```markdown
## 截图对比

旧版本：
![[screenshot/old.png|600px]]

新版本：
![[screenshot/new.png|600px]]

变化：
![改进说明](changes.md)  ← 这是链接，不是图片，不转换
```

**转换后**:
```markdown
## 截图对比

旧版本：
<img src="screenshot/old.png" style="display: block; width: 600px;" alt="">

新版本：
<img src="screenshot/new.png" style="display: block; width: 600px;" alt="">

变化：
![改进说明](changes.md)  ← 这是链接，不是图片，不转换
```

## 正则表达式模式识别

用于识别 Markdown 图片的模式：

### Wikilink 格式
```regex
!\[\[([^\]|]+)(\|(\d+px))?\]\]
```
捕获组：
- Group 1: 图片路径
- Group 3: 宽度值（可选，如 "600"）

### 标准 Markdown 格式
```regex
!\[([^\]]*)\|?(\d+px)?\]\(([^)]+)\)
```
捕获组：
- Group 1: 替换文字（可能为空）
- Group 2: 宽度值（可选）
- Group 3: 图片路径

注意：需要区分 `![](url)` 图片链接和 `[text](url)` 普通链接，只转换前者。

## 范围边界

- ✅ 转换 Markdown 文档中的图片语法
- ✅ 支持 Wikilink 和标准 Markdown 两种格式
- ✅ 保留宽度和替换文字信息
- ✅ 逆序处理避免位置偏移
- ❌ 不处理 HTML `<img>` 标签（已经是目标格式）
- ❌ 不处理普通链接 `[text](url)`（只转换 `![](url)`）
- ❌ 不修改其他 Markdown 语法

## 注意事项

1. **严格的逆序处理** - 必须从文件末尾开始向前处理，不能跳过或改变顺序
2. **引号使用 ASCII 英文引号** - HTML 属性值必须使用英文引号 `"` 或 `'`
3. **默认宽度为 100%** - 未指定宽度时使用 `width: 100%`
4. **保持其他内容不变** - 只转换图片语法，不改动其他文本
5. **验证路径有效性** - 转换前确认图片路径是否需要调整（相对路径保持不变）
