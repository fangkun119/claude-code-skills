# 创建Skill

创建一个claude color skill，用来根据用户的要求，为文档中选中的文字设置样式。它会用HTLM的`<span>`标签包裹被选中的文字，并根据用户传入的要求，在`<span>`标签中选择合适的style属性更改文字样式。

注意，包裹style属性的引号必须是英文引号（绝不可以是中文引号）

例子如下

| 属性名称 | 说明 | 例子 | 用户要求举例 |
|---------|------|------|------------|
| **color** | 设置文本颜色 | `<span style="color: red;">被选中的文本</span>` | "红色" |
| **background-color** | 设置背景颜色 | `<span style="background-color: yellow;">被选中的文本</span>` | "黄色背景" |
| **font-size** | 设置字体大小 | `<span style="font-size: 16px;">被选中的文本</span>` | "16像素" |
| **font-family** | 设置字体族 | `<span style="font-family: Arial;">被选中的文本</span>` | "Arial字体" |
| **font-weight** | 设置字体粗细 | `<span style="font-weight: bold;">被选中的文本</span>` | "加粗" |
| **font-style** | 设置字体样式（斜体等） | `<span style="font-style: italic;">被选中的文本</span>` | "斜体" |
| **text-decoration** | 设置文本装饰（下划线等） | `<span style="text-decoration: underline;">被选中的文本</span>` | "下划线" |
| **text-align** | 设置文本对齐方式 | `<span style="text-align: center;">被选中的文本</span>` | "居中" |
| **line-height** | 设置行高 | `<span style="line-height: 1.5;">被选中的文本</span>` | "行高1.5倍" |
| **letter-spacing** | 设置字母间距 | `<span style="letter-spacing: 2px;">被选中的文本</span>` | "字母间距2px" |
| **word-spacing** | 设置单词间距 | `<span style="word-spacing: 4px;">被选中的文本</span>` | "单词间距4px" |
| **text-indent** | 设置文本缩进 | `<span style="text-indent: 20px;">被选中的文本</span>` | "首行缩进20px" |
| **text-transform** | 设置文本转换（大写等） | `<span style="text-transform: uppercase;">被选中的文本</span>` | "全部大写" |
| **white-space** | 设置空白符处理 | `<span style="white-space: nowrap;">被选中的文本</span>` | "不换行" |
| **opacity** | 设置透明度 | `<span style="opacity: 0.5;">被选中的文本</span>` | "半透明" |
| **border** | 设置边框 | `<span style="border: 1px solid black;">被选中的文本</span>` | "黑色边框" |
| **padding** | 设置内边距 | `<span style="padding: 5px;">被选中的文本</span>` | "内边距5px" |
| **margin** | 设置外边距 | `<span style="margin: 10px;">被选中的文本</span>` | "外边距10px" |
| **cursor** | 设置鼠标指针样式 | `<span style="cursor: pointer;">被选中的文本</span>` | "手型指针" |
| **box-shadow** | 设置阴影效果 | `<span style="box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">被选中的文本</span>` | "阴影效果" |
| **border-radius** | 设置圆角 | `<span style="border-radius: 5px;">被选中的文本</span>` | "圆角5px" |
