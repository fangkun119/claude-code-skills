# 图片格式测试文档

## 基本格式测试

### Wikilink 无宽度

<img src="assets/diagram1.png" style="display: block; width: 100%;" alt="">

### Wikilink 带宽度

<img src="assets/diagram2.png" style="display: block; width: 600px;" alt="">

### 标准 Markdown 格式

<img src="./docs/architecture.png" style="display: block; width: 100%;" alt="系统架构图">

### 标准 Markdown 带宽度

<img src="./screenshots/ui.png" style="display: block; width: 800px;" alt="用户界面截图">

### 无替换文字的标准格式

<img src="./images/anonymous.png" style="display: block; width: 100%;" alt="">

### 无替换文字带宽度

<img src="./images/anonymous-wide.png" style="display: block; width: 900px;" alt="">

## 多图片场景

下面是两张对比图片：

旧版本：
<img src="screenshots/old-version.png" style="display: block; width: 700px;" alt="">

新版本：
<img src="screenshots/new-version.png" style="display: block; width: 700px;" alt="">

## 边界情况

这是普通链接，不应该被转换：
[点击查看文档](./docs/readme.md)

这是已经转换过的 HTML 标签，不应该再次处理：
<img src="already-converted.png" style="display: block; width: 100%;" alt="Already HTML">

## 结尾测试

文档最后的图片：

<img src="final-image.png" style="display: block; width: 500px;" alt="">
