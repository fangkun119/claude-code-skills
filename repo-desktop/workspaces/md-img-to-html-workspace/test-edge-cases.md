# 边界情况测试

## 普通链接不应该被转换

这是一个图片链接：
[图片链接](./images/photo.png)

这是一个文档链接：
[文档](./readme.md)

## 已存在的 HTML 标签

这是一个已经是 HTML 格式的图片，不应该被处理：
<img src="existing.png" style="display: block; width: 100%;" alt="Existing">

## 空文件

本节没有图片，只是文字内容。

## 特殊路径

带空格的路径：
<img src="path with spaces/image.png" style="display: block; width: 100%;" alt="">

带特殊字符的路径：
<img src="path-with-dashes_underscores.png" style="display: block; width: 800px;" alt="">

相对路径：
<img src="../parent-folder/image.png" style="display: block; width: 100%;" alt="相对路径示例">

绝对 URL：
<img src="https://example.com/external.png" style="display: block; width: 600px;" alt="外部图片">

## 嵌套在列表中的图片

- 项目 1
  - 子项目 <img src="nested.png" style="display: block; width: 300px;" alt="">
- 项目 2
- 项目 3

## 表格中的图片

| 列 1 | 列 2 |
|------|------|
| 文字 | <img src="table.png" style="display: block; width: 100%;" alt=""> |
| 更多 | <img src="./table-image.png" style="display: block; width: 400px;" alt="表格图片"> |
