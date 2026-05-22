# dir-archive Verification Spec

## 测试环境前提

- Python ≥3.12 已安装
- `uv` 已安装
- 工作目录可写

所有测试在临时目录中执行，测试结束后清理。

---

## TC-DA-01: 首次归档 — 创建新 tar.gz

**前置条件**：目标目录存在，同级路径下没有对应的 `.tar.gz` 文件。

**输入**：包含以下文件的目录 `my-project/`：
- `my-project/README.md`（内容：`# Hello`）
- `my-project/src/main.py`（内容：`print("hi")`）

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**预期输出**：
- stdout 包含 `[INFO] Creating new archive: ./my-project.tar.gz`
- stdout 包含 `[DONE] Created ./my-project.tar.gz`
- 同级路径下生成 `my-project.tar.gz`

**验证**：
```bash
tar tzf my-project.tar.gz | sort
```
输出包含：
```
my-project
my-project/README.md
my-project/src/main.py
```
- 解压后 `README.md` 内容为 `# Hello`
- 解压后 `src/main.py` 内容为 `print("hi")`

---

## TC-DA-02: 增量更新 — 已修改文件被覆盖

**前置条件**：`my-project.tar.gz` 已存在（基于 TC-DA-01 的状态）。

**操作**：修改磁盘上的文件内容：
- `my-project/README.md` 内容改为 `# Hello World`

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**预期输出**：
- stdout 包含 `[INFO] Updating existing archive: ./my-project.tar.gz`
- stdout 包含 `[DONE] Updated ./my-project.tar.gz (1 updated, 0 added)`

**验证**：
- 解压后 `README.md` 内容为 `# Hello World`（新版本）
- 解压后 `src/main.py` 内容不变

---

## TC-DA-03: 增量更新 — 新增文件被添加

**前置条件**：`my-project.tar.gz` 已存在。

**操作**：在磁盘上新增文件：
- `my-project/src/utils.py`（内容：`def add(a, b): return a + b`）

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**预期输出**：
- stdout 包含 `[DONE] Updated ./my-project.tar.gz (0 updated, 1 added)`

**验证**：
- 归档中包含 `my-project/src/utils.py`，内容为 `def add(a, b): return a + b`
- 原有文件 `README.md` 和 `src/main.py` 仍完整保留

---

## TC-DA-04: 增量更新 — 磁盘上已删除的文件保留在归档中

**前置条件**：`my-project.tar.gz` 已存在（包含 `README.md`、`src/main.py`、`src/utils.py`）。

**操作**：删除磁盘上的 `my-project/src/utils.py`。

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**预期输出**：
- stdout 包含 `[DONE] Updated ./my-project.tar.gz (0 updated, 0 added)`

**验证**：
- 归档中仍包含 `my-project/src/utils.py`（不删除）
- 其他文件不受影响

---

## TC-DA-05: 增量更新 — 未修改文件跳过

**前置条件**：`my-project.tar.gz` 已存在。

**操作**：不修改任何文件，直接再次归档。

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**预期输出**：
- stdout 包含 `[DONE] Updated ./my-project.tar.gz (2 updated, 0 added)` 或类似（文件未修改但仍被写入，因为脚本基于文件名匹配而非内容比较）

**验证**：
- 归档内容与之前一致

---

## TC-DA-06: 错误处理 — 目录不存在

**输入**：传入一个不存在的路径。

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./nonexistent-dir/"
```

**预期输出**：
- stderr 包含 `[ERROR] './nonexistent-dir/' is not a directory or does not exist.`
- 退出码为 1
- 不生成任何 `.tar.gz` 文件

---

## TC-DA-07: 错误处理 — 传入文件路径而非目录

**前置条件**：工作目录下存在普通文件 `some-file.txt`。

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./some-file.txt"
```

**预期输出**：
- stderr 包含 `[ERROR]`
- 退出码为 1

---

## TC-DA-08: 路径格式 — 末尾有无斜杠均可

**前置条件**：目标目录 `my-project/` 存在，且同级路径下没有 `.tar.gz`。

**执行 A**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**执行 B**（清理 tar.gz 后）：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project"
```

**预期**：两次执行均成功，生成的归档文件名均为 `my-project.tar.gz`。

---

## TC-DA-09: 环境准备 — .venv 不存在时自动创建

**前置条件**：工作目录下没有 `.venv` 目录。

**执行**：
```bash
if [ -d ".venv" ]; then
  echo "[INFO] 复用已有 .venv"
else
  uv venv --python=3.12 .venv
fi
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**预期**：
- `.venv` 目录被创建
- 归档正常完成

---

## TC-DA-10: 环境准备 — .venv 已存在时复用

**前置条件**：`.venv` 已存在。

**执行**：
```bash
if [ -d ".venv" ]; then
  echo "[INFO] 复用已有 .venv"
else
  uv venv --python=3.12 .venv
fi
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./my-project/"
```

**预期**：
- stdout 包含 `[INFO] 复用已有 .venv`
- 不重新创建 `.venv`
- 归档正常完成

---

## TC-DA-11: 绝对路径支持

**前置条件**：目录 `/tmp/test-archive/my-project/` 存在。

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "/tmp/test-archive/my-project"
```

**预期**：
- 归档生成在 `/tmp/test-archive/my-project.tar.gz`
- stdout 包含 `[INFO] Creating new archive: /tmp/test-archive/my-project.tar.gz`

---

## TC-DA-12: 空目录归档

**前置条件**：空目录 `empty-dir/` 存在。

**执行**：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./empty-dir/"
```

**预期**：
- 成功创建 `empty-dir.tar.gz`
- 归档仅包含目录条目本身，无文件条目

---

## TC-DA-13: 参数错误 — 无参数或多个参数

**执行 A**（无参数）：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py
```

**执行 B**（多个参数）：
```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "./dir1" "./dir2"
```

**预期**：
- stderr 包含 `Usage: python archive_dir.py <directory_path>`
- 退出码为 1
