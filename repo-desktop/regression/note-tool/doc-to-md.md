# doc-to-md Verification Spec

## 测试环境前提

- Python ≥3.12 已安装
- `uv` 已安装（`uv --version` 可返回版本号）
- 工作目录可写

---

## TC-DM-01: PDF 转 Markdown

**前置条件**：工作目录下有测试 PDF 文件 `sample.pdf`。

**环境准备**：
```bash
if [ -d ".venv" ]; then
  echo "[INFO] 复用已有 .venv"
else
  uv venv --python=3.12 .venv
fi
source .venv/bin/activate
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install markitdown[all]==0.1.3
```

**执行**：
```bash
markitdown sample.pdf > sample.md
```

**预期**：
- 命令退出码为 0
- 生成 `sample.md` 文件
- `sample.md` 包含 PDF 中的文本内容（UTF-8 编码）
- `sample.md` 不是空文件

---

## TC-DM-02: DOCX 转 Markdown

**前置条件**：工作目录下有测试 DOCX 文件 `sample.docx`。

**执行**：
```bash
markitdown sample.docx > sample.md
```

**预期**：
- 命令退出码为 0
- 生成 `sample.md` 文件
- `sample.md` 包含 DOCX 中的文本内容（非空）

---

## TC-DM-03: PPTX 转 Markdown

**前置条件**：工作目录下有测试 PPTX 文件 `sample.pptx`。

**执行**：
```bash
markitdown sample.pptx > sample.md
```

**预期**：
- 命令退出码为 0
- 生成 `sample.md` 文件
- `sample.md` 包含 PPTX 中的幻灯片文本内容（非空）

---

## TC-DM-04: HTML 转 Markdown

**前置条件**：工作目录下有测试 HTML 文件 `sample.html`，内容包含标题和段落。

**执行**：
```bash
markitdown sample.html > sample.md
```

**预期**：
- 命令退出码为 0
- 生成 `sample.md` 文件
- `sample.md` 中 HTML 标签被正确转换为 Markdown 格式（如 `<h1>` → `#`，`<p>` → 段落）

---

## TC-DM-05: 输出文件覆盖已有同名 .md

**前置条件**：
- 测试文件 `sample.pdf` 存在
- `sample.md` 已存在，内容为 `old content`

**执行**：
```bash
markitdown sample.pdf > sample.md
```

**预期**：
- `sample.md` 被覆盖，内容为 PDF 转换结果
- `sample.md` 不再包含 `old content`

---

## TC-DM-06: 批量转换 PDF 文件

**前置条件**：工作目录下有多个 PDF 文件：`a.pdf`、`b.pdf`、`c.pdf`。

**执行**：
```bash
for f in *.pdf; do
  markitdown "$f" > "${f%.pdf}.md"
done
```

**预期**：
- 生成 `a.md`、`b.md`、`c.md` 三个文件
- 每个 `.md` 文件内容对应其 `.pdf` 源文件
- 非零大小的文件数量等于 PDF 文件数量

---

## TC-DM-07: 批量转换 DOCX 文件

**前置条件**：工作目录下有多个 DOCX 文件：`report1.docx`、`report2.docx`。

**执行**：
```bash
for f in *.docx; do
  markitdown "$f" > "${f%.docx}.md"
done
```

**预期**：
- 生成 `report1.md`、`report2.md`
- 每个 `.md` 文件内容对应其 `.docx` 源文件

---

## TC-DM-08: 环境准备 — .venv 不存在时自动创建

**前置条件**：工作目录下没有 `.venv` 目录。

**执行**：
```bash
uv venv --python=3.12 .venv
source .venv/bin/activate
uv pip install markitdown[all]==0.1.3
markitdown --version
```

**预期**：
- `.venv` 目录被创建
- `markitdown --version` 输出版本号
- 后续转换命令可正常执行

---

## TC-DM-09: 环境准备 — .venv 已存在时复用

**前置条件**：`.venv` 已存在。

**执行**：
```bash
if [ -d ".venv" ]; then
  echo "[INFO] 复用已有 .venv"
else
  uv venv --python=3.12 .venv
fi
source .venv/bin/activate
markitdown sample.pdf > sample.md
```

**预期**：
- stdout 包含 `[INFO] 复用已有 .venv`
- 不重新创建 `.venv`
- 转换正常完成

---

## TC-DM-10: markitdown 版本锁定为 0.1.3

**执行**：
```bash
markitdown --version
```

**预期**：输出版本号为 `0.1.3`（或与之兼容的格式）。

---

## TC-DM-11: 不支持的文件格式

**前置条件**：工作目录下有 `sample.xlsx` 文件（Excel，不在支持列表中）。

**执行**：
```bash
markitdown sample.xlsx > sample.md
```

**预期**：
- 行为取决于 markitdown 是否支持 xlsx（markitdown[all] 可能包含此格式）
- 若不支持，命令应返回非零退出码或输出警告
- 若支持（因为使用了 `[all]`），则正常转换

**注**：此用例记录边界行为，标记为 informational。

---

## TC-DM-12: 不存在的文件

**前置条件**：工作目录下没有 `nonexistent.pdf`。

**执行**：
```bash
markitdown nonexistent.pdf > output.md
```

**预期**：
- 命令返回非零退出码，或 stderr 包含错误信息
- 不生成有效的 `output.md`（或生成空文件）

---

## TC-DM-13: 输出编码为 UTF-8

**前置条件**：测试 PDF `chinese.pdf` 包含中文内容。

**执行**：
```bash
markitdown chinese.pdf > chinese.md
file chinese.md
```

**预期**：
- `file` 命令输出包含 `UTF-8` 或 `ASCII`（纯英文时）
- 中文内容在 `chinese.md` 中正确显示，无乱码

---

## TC-DM-14: 复杂排版文档 — 合并单元格可能丢失

**前置条件**：测试 DOCX `table_complex.docx` 包含复杂表格（合并单元格）。

**执行**：
```bash
markitdown table_complex.docx > table_complex.md
```

**预期**：
- 转换完成，退出码为 0
- 文本内容保留，但合并单元格结构可能扁平化
- **已知限制**：不作为 bug，但需人工校验关键表格内容

---

## TC-DM-15: markitdown 依赖安装使用清华镜像

**执行**：
```bash
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install markitdown[all]==0.1.3
```

**预期**：
- 安装成功，无超时错误
- 从清华镜像下载包（通过日志可确认域名 `pypi.tuna.tsinghua.edu.cn`）
