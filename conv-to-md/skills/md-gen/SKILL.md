---
name: md-gen
description: 从 PDF、DOCX、DOC、PPT、PPTX、HTML 文件生成 Markdown 文档。使用 markitdown 工具将各种文档格式转换为 Markdown。在需要将 PDF、PowerPoint、Word、HTML 文档转换为 Markdown 格式时使用。
allowed-tools:
  - Bash
---
# Markdown 文档生成

将 PDF、DOCX、DOC、PPTX、PPT 文件转换为 Markdown 格式。

## 前提条件

在使用此技能之前，请确保系统中已安装以下依赖，如果没有安装，直接退出并提示用户

- **Python 3.12+**: 用于运行 markitdown 工具
- **uv**: Python 包管理工具，用于创建虚拟环境和安装依赖包


## 快速开始

```bash
# 步骤1：安装环境
#!/bin/bash
if [ -d ".venv" ]; then
  echo ".venv exists!"
else
  uv venv --python=3.12 .venv
fi

# 步骤2： 激活虚拟环境
source .venv/bin/activate

# 步骤3： 安装 markitdown
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install markitdown[all]==0.1.3
markitdown --version

# 步骤4：转换文档
markitdown your-document.pdf > your-document.md
```

## 步骤参考

### 步骤1：安装环境

```bash
#!/bin/bash
if [ -d ".venv" ]; then
  echo ".venv exists!"
else
  uv venv --python=3.12 .venv
fi
```

### 步骤2： 激活虚拟环境

markitdown 安装在虚拟环境中，使用时需要激活环境

```bash
source .venv/bin/activate
```

### 步骤3： 安装markitdown

```bash
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install markitdown[all]==0.1.3
markitdown --version
```


### 步骤4： 转换文档

#### 支持的文件格式

- PDF 文件：`.pdf`
- PowerPoint 文件：`.ppt`, `.pptx`
- Word 文件：`.doc`, `.docx`
- HTML 文件：`.html`

#### 基本转换

```bash
# 激活虚拟环境
source .venv/bin/activate

# 转换 PDF 文件
markitdown path-to-file.pdf > path-to-file.md

# 转换 Word 文件
markitdown path-to-file.doc > path-to-file.md
markitdown path-to-file.docx > path-to-file.md

# 转换 PowerPoint 文件
markitdown path-to-file.ppt > path-to-file.md
markitdown path-to-file.pptx > path-to-file.md

# 转换 HTTP 文件
markitdown path-to-file.html > path-to-file.md
```

#### 批量转换

```bash
# 激活虚拟环境
source .venv/bin/activate

# 转换当前目录下所有 PDF 文件
for file in *.pdf; do
    markitdown "$file" > "${file%.pdf}.md"
done

# 转换当前目录下所有 Word 文件
for file in *.docx; do
    markitdown "$file" > "${file%.docx}.md"
done

for file in *.doc; do
    markitdown "$file" > "${file%.docx}.md"
done

# 转换当前目录下所有的PPT文件
for file in *.pptx; do
    markitdown "$file" > "${file%.docx}.md"
done

for file in *.ppt; do
    markitdown "$file" > "${file%.docx}.md"
done

# 转换当前目录下所有的HTML文件
for file in *.html; do
    markitdown "$file" > "${file%.docx}.md"
done
```

## 输出文件命名

输出文件名与输入文件名相同，扩展名改为 `.md`。例如：

- `document.pdf` → `document.md`
- `presentation.pptx` → `presentation.md`
- `presentation.ppt` → `presentation.md`
- `report.docx` → `report.md`
- `report.doc` → `report.md`
- `page.html` → `page.md`

## 注意事项

1. 确保 markitdown 已正确安装
2. 输出文件将覆盖同名的现有 Markdown 文件
3. 转换质量取决于原始文档的格式和内容复杂度
4. 对于扫描的 PDF，可能需要额外的 OCR 处理
