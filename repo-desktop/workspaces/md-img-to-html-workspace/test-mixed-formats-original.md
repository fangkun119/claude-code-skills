# 图片格式测试文档

## 基本格式测试

### Wikilink 无宽度

![[assets/diagram1.png]]

### Wikilink 带宽度

![[assets/diagram2.png|600px]]

### 标准 Markdown 格式

![系统架构图](./docs/architecture.png)

### 标准 Markdown 带宽度

![用户界面截图|800px](./screenshots/ui.png)

### 无替换文字的标准格式

![](./images/anonymous.png)

### 无替换文字带宽度

![]|900px](./images/anonymous-wide.png)

## 多图片场景

下面是两张对比图片：

旧版本：
![[screenshots/old-version.png|700px]]

新版本：
![[screenshots/new-version.png|700px]]

## 边界情况

这是普通链接，不应该被转换：
[点击查看文档](./docs/readme.md)

这是已经转换过的 HTML 标签，不应该再次处理：
<img src="already-converted.png" style="display: block; width: 100%;" alt="Already HTML">

## 结尾测试

文档最后的图片：

![[final-image.png|500px]]
