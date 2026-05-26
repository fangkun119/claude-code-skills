# text-style Verification Spec

## 测试环境前提

- Claude Code 已安装 text-style skill
- 工作目录可写
- 支持 HTML/CSS 输出

---

## TC-TS-01: 基础红色文字

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"重要提示"改成红色
```

**预期输出**：
```html
<span style="color: red;">重要提示</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: red` CSS 属性
- 使用英文引号 `"` 包裹 style 属性值
- 目标文本 "重要提示" 正确包含在输出中
- 不包含中文引号 `""` 或 `''`

---

## TC-TS-02: 黄色背景高亮

**前置条件**：text-style skill 已加载。

**用户输入**：
```
给"注意事项"加上黄色背景
```

**预期输出**：
```html
<span style="background-color: yellow;">注意事项</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `background-color: yellow` CSS 属性
- 使用英文引号
- 目标文本正确

---

## TC-TS-03: 字体大小和字体族

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"标题"使用 20px 的 Arial 字体
```

**预期输出**：
```html
<span style="font-size: 20px; font-family: Arial;">标题</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `font-size: 20px` 和 `font-family: Arial` 两个属性
- 多个属性用分号分隔
- 使用英文引号

---

## TC-TS-04: 加粗文字

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"重点内容"加粗
```

**预期输出**：
```html
<span style="font-weight: bold;">重点内容</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `font-weight: bold` CSS 属性
- 使用英文引号

---

## TC-TS-05: 卡片样式（多属性组合）

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"警告"做成卡片样式：黑色边框、内边距5px、圆角3px
```

**预期输出**：
```html
<span style="border: 1px solid black; padding: 5px; border-radius: 3px;">警告</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `border`、`padding: 5px`、`border-radius: 3px` 三个属性
- 所有属性用分号分隔
- 使用英文引号

---

## TC-TS-06: 透明度设置

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"半透明文字"的透明度为50%
```

**预期输出**：
```html
<span style="opacity: 0.5;">半透明文字</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `opacity: 0.5` CSS 属性
- 使用英文引号

---

## TC-TS-07: 行高设置

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"多行文本"的行高设置为1.5倍
```

**预期输出**：
```html
<span style="line-height: 1.5;">多行文本</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `line-height: 1.5` CSS 属性
- 使用英文引号

---

## TC-TS-08: 字母间距

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"英文文本"的字母间距为2px
```

**预期输出**：
```html
<span style="letter-spacing: 2px;">英文文本</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `letter-spacing: 2px` CSS 属性
- 使用英文引号

---

## TC-TS-09: 文本大写转换

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"text"全部大写
```

**预期输出**：
```html
<span style="text-transform: uppercase;">text</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `text-transform: uppercase` CSS 属性
- 使用英文引号

---

## TC-TS-10: 文本不换行

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"长文本"不换行
```

**预期输出**：
```html
<span style="white-space: nowrap;">长文本</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `white-space: nowrap` CSS 属性
- 使用英文引号

---

## TC-TS-11: 首行缩进

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"段落文本"首行缩进20px
```

**预期输出**：
```html
<span style="text-indent: 20px;">段落文本</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `text-indent: 20px` CSS 属性
- 使用英文引号

---

## TC-TS-12: 单词间距

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"english text"的单词间距为4px
```

**预期输出**：
```html
<span style="word-spacing: 4px;">english text</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `word-spacing: 4px` CSS 属性
- 使用英文引号

---

## TC-TS-13: 红色加粗组合样式

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"重要提示"改成红色加粗
```

**预期输出**：
```html
<span style="color: red; font-weight: bold;">重要提示</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: red` 和 `font-weight: bold` 两个属性
- 多个属性用分号分隔
- 使用英文引号

---

## TC-TS-14: 十六进制颜色值

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"文字"改成深红色 #FF0000
```

**预期输出**：
```html
<span style="color: #FF0000;">文字</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: #FF0000` CSS 属性
- 使用英文引号
- 支持十六进制颜色格式

---

## TC-TS-15: RGB 颜色值

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"文字"改成 RGB 红色 (255, 0, 0)
```

**预期输出**：
```html
<span style="color: rgb(255, 0, 0);">文字</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: rgb(255, 0, 0)` CSS 属性
- 使用英文引号
- 支持 RGB 颜色格式

---

## TC-TS-16: 中文引号检测（否定测试）

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"测试"改成红色
```

**预期输出**：
```html
<span style="color: red;">测试</span>
```

**验证点**：
- **必须不包含**中文引号 `""` 或 `''`
- **必须只使用**英文引号 `"` 或 `'`
- 包含 `color: red` CSS 属性

---

## TC-TS-17: 空格处理

**前置条件**：text-style skill 已加载。

**用户输入**：
```
给"有 空格 的文字"加上蓝色背景
```

**预期输出**：
```html
<span style="background-color: blue;">有 空格 的文字</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `background-color: blue` CSS 属性
- 目标文本中的空格被正确保留
- 使用英文引号

---

## TC-TS-18: 特殊字符文本

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"<tag>"改成绿色
```

**预期输出**：
```html
<span style="color: green;"><tag></span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: green` CSS 属性
- 目标文本中的特殊字符 `<` 和 `>` 被正确转义或保留
- 使用英文引号

---

## TC-TS-19: 长文本处理

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"这是一段很长的文字内容，包含多个句子和标点符号，用来测试 skill 对长文本的处理能力。"改成橙色
```

**预期输出**：
```html
<span style="color: orange;">这是一段很长的文字内容，包含多个句子和标点符号，用来测试 skill 对长文本的处理能力。</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: orange` CSS 属性
- 长文本内容完整保留
- 使用英文引号

---

## TC-TS-20: 边框样式组合

**前置条件**：text-style skill 已加载。

**用户输入**：
```
给"边框测试"加上1px的红色实线边框
```

**预期输出**：
```html
<span style="border: 1px solid red;">边框测试</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `border: 1px solid red` CSS 属性
- 边框样式包含宽度、类型、颜色三个值
- 使用英文引号

---

## TC-TS-21: 内边距设置

**前置条件**：text-style skill 已加载。

**用户输入**：
```
给"内边距测试"设置10px的内边距
```

**预期输出**：
```html
<span style="padding: 10px;">内边距测试</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `padding: 10px` CSS 属性
- 使用英文引号

---

## TC-TS-22: 圆角设置

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"圆角测试"的圆角设为5px
```

**预期输出**：
```html
<span style="border-radius: 5px;">圆角测试</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `border-radius: 5px` CSS 属性
- 使用英文引号

---

## TC-TS-23: 字体族（带后备字体）

**前置条件**：text-style skill 已加载。

**用户输入**：
```
让"字体测试"使用 Arial 字体，后备无衬线字体
```

**预期输出**：
```html
<span style="font-family: Arial, sans-serif;">字体测试</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `font-family` 属性，可能包含多个字体值
- 使用英文引号
- 字体族名称正确处理

---

## TC-TS-24: 自然语言表达变体

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"变体测试"的文字颜色设为蓝色
```

**预期输出**：
```html
<span style="color: blue;">变体测试</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: blue` CSS 属性
- skill 能理解不同的自然语言表达方式
- 使用英文引号

---

## TC-TS-25: 多样式综合测试

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"综合测试"改成：红色、加粗、20px、Arial字体、黄色背景
```

**预期输出**：
```html
<span style="color: red; font-weight: bold; font-size: 20px; font-family: Arial; background-color: yellow;">综合测试</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含所有请求的 CSS 属性：`color: red`、`font-weight: bold`、`font-size: 20px`、`font-family: Arial`、`background-color: yellow`
- 多个属性用分号正确分隔
- 使用英文引号
- 属性顺序可以不同

---

## TC-TS-26: 英文输入测试

**前置条件**：text-style skill 已加载。

**用户输入**：
```
Make "important text" red and bold
```

**预期输出**：
```html
<span style="color: red; font-weight: bold;">important text</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: red` 和 `font-weight: bold` 属性
- skill 能处理英文输入
- 使用英文引号

---

## TC-TS-27: 混合中英文目标文本

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"Hello 世界"改成蓝色
```

**预期输出**：
```html
<span style="color: blue;">Hello 世界</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: blue` CSS 属性
- 目标文本中的中英文混合内容正确保留
- 使用英文引号

---

## TC-TS-28: 引号内的引号（边界测试）

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把包含引号的"文本'测试'"改成绿色
```

**预期输出**：
```html
<span style="color: green;">文本'测试'</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `color: green` CSS 属性
- 目标文本中的引号被正确保留
- 使用英文引号包裹 style 属性
- 不混淆目标文本中的引号和 style 属性的引号

---

## TC-TS-29: 非常小的字体

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"小字"改成 8px 字体
```

**预期输出**：
```html
<span style="font-size: 8px;">小字</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `font-size: 8px` CSS 属性
- 支持小尺寸字体
- 使用英文引号

---

## TC-TS-30: 非常大的字体

**前置条件**：text-style skill 已加载。

**用户输入**：
```
把"大字"改成 72px 字体
```

**预期输出**：
```html
<span style="font-size: 72px;">大字</span>
```

**验证点**：
- 包含 `<span>` 标签
- 包含 `font-size: 72px` CSS 属性
- 支持大尺寸字体
- 使用英文引号
