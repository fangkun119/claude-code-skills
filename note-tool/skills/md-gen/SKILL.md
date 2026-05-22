---
name: md-gen
description: |
  将 PDF/DOCX/DOC/PPT/PPTX/HTML 批量转换为 Markdown。
  依赖 markitdown 0.1.3，运行在 Python 3.12+ 虚拟环境。
allowed-tools:
  - Bash
---

# 1 目的（Purpose）
提供一条可复制、可审计的单一命令流，把常见办公文档（PDF、Word、PowerPoint、HTML）自动转为 Markdown，保证：
- 输出格式统一
- 转换过程可追踪
- 版本升级可回滚

# 2 适用范围（Scope）
适用于 Claude Code 交互式会话中需要文档转 Markdown 的全部场景，覆盖：
- 单文件手动转换
- 当前工作区批量转换

不适用于扫描版 PDF 的 OCR 需求（需额外流程）。

# 3 定义与缩写（Definitions）
| 术语/缩写 | 含义 |
|-----------|------|
| venv      | Python 虚拟环境目录，固定名 `.venv` |
| md-gen    | 本技能在 Claude Code 中的注册名 |
| TUNA      | 清华大学 PyPI 镜像，用于加速依赖下载 |

# 4 职责（Responsibility）
| 岗位/角色 | 职责 |
|-----------|------|
| 用户（User） | 1. 提供待转文件&lt;br&gt;2. 检查输出结果 |
| md-gen Skill | 1. 自动检测依赖&lt;br&gt;2. 执行转换命令&lt;br&gt;3. 返回状态码与日志 |

# 5 前提条件（Prerequisites）
执行本 SOP 前，系统必须满足：
1. Python ≥3.12 已安装且可在 `$PATH` 调用
2. `uv` 包管理器已安装（`uv --version` 可返回版本号）
3. 工作目录可写（用于创建 `.venv` 与输出 `.md`）

若 1-3 任一项缺失，Skill 立即退出并提示用户修正，不继续后续步骤。

# 6 操作步骤（Procedure）

## 6.1 环境准备

```bash
# 1. 创建/复用虚拟环境
if [ -d ".venv" ]; then
  echo "[INFO] 复用已有 .venv"
else
  uv venv --python=3.12 .venv
fi
source .venv/bin/activate
```

## 6.2 安装 markitdown

```bash
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
uv pip install markitdown[all]==0.1.3
markitdown --version # 预期该命令可以成功执行
```

## 6.3 单文件转换

```bash
markitdown file_to_path.pdf > file_to_path.md
markitdown file_to_path.docx > file_to_path.md
markitdown file_to_path.doc > file_to_path.md
markitdown file_to_path.pptx > file_to_path.md
markitdown file_to_path.ppt > file_to_path.md
markitdown file_to_path.html > file_to_path.md
```

输入扩展名：pdf / doc / docx / ppt / pptx / html
输出文件名：与输入文件同名，扩展名改为 .md
编码：统一 UTF-8

## 6.4 批量转换示例

```bash
# 转换当前目录全部 PDF
for f in *.pdf; do
  markitdown "$f" > "${f%.pdf}.md"
done
```

其余格式（doc/docx/ppt/pptx/html）循环写法同上，仅需替换通配符与扩展名变量。

## 7 记录与输出（Records）

| 记录名称         | 存储位置            | 保留时长    |
| ------------ | --------------- | ------- |
| 转换日志（stdout） | Claude Code 对话流 | 随对话生命周期 |
| 生成的 `.md` 文件 | 原文件同级目录         | 由用户自行管理 |


## 8 注意事项（Warnings & Cautions）

1. 输出文件默认覆盖同名 .md，不保留旧版本；如需版本管理，请提前 git add。
2. 复杂排版、合并单元格、批注、动画等元素可能丢失，需人工校验。
3. 扫描版 PDF 不含文本层时，转换结果为空，请先执行 OCR。
4. 本 Skill 锁定 markitdown==0.1.3，升级须走变更控制（参见第 9 章）。


## 9 相关文件与附件（References）

* markitdown 官方文档：https://github.com/microsoft/markitdown
* 清华大学 PyPI 镜像使用说明：https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

## 10 修订历史（Changelog）

| 版本   | 日期         | 修订人    | 变更摘要                                  |
| ---- | ---------- | ------ | ------------------------------------- |
| v1.0 | 2025-06-01 | Claude | 首版，支持 pdf/doc/docx/ppt/pptx/html → md |


