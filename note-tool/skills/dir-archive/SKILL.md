---
name: dir-archive
description: |
  将目录归档为 .tar.gz 文件。传入目录路径，自动创建或增量更新对应的 tar.gz 归档。
  支持新增文件、覆盖已有文件，不会删除归档中已有但磁盘上已不存在的文件。
  当用户提到归档、archive、打包目录、备份目录、tar.gz、增量归档时，使用此 skill。
allowed-tools:
  - Bash
---

# dir-archive — 目录归档 Skill

将指定目录归档为 `.tar.gz` 文件。如果归档已存在，则增量更新（添加新文件、覆盖已修改文件，不删除归档中的旧文件）。

## 使用方式

```markdown
/dir-archive "./path/to/target_dir/"
```

参数：一个目录路径（相对或绝对路径均可，末尾的 `/` 可省略）。

## 执行步骤

### 1. 定位脚本

脚本位于本 skill 的 `scripts/archive_dir.py`，使用项目 `.venv` 中的 Python 执行。

### 2. 运行归档

```bash
.venv/bin/python note-tool/skills/dir-archive/scripts/archive_dir.py "<用户传入的目录路径>"
```

### 3. 输出说明

脚本会输出日志信息：
- `[INFO] Creating new archive: <path>` — 首次创建归档
- `[INFO] Updating existing archive: <path>` — 增量更新已有归档
- `[DONE]` — 操作完成，附带更新和新增文件数量

归档文件生成在目标目录的同级路径下，文件名为 `<目录名>.tar.gz`。

## 行为规则

| 场景 | 行为 |
|------|------|
| tar.gz 不存在 | 创建新归档，包含目录下所有文件 |
| tar.gz 已存在，文件未修改 | 跳过，不重复写入 |
| tar.gz 已存在，文件已修改 | 用磁盘上的新版本覆盖归档中的旧版本 |
| 磁盘上有新文件 | 添加到归档 |
| 磁盘上已删除的文件 | 归档中保留，不删除 |

## 前提条件

- Python 3.12+（项目 `.venv` 已配置）
- 目标目录存在且可读
- 输出路径可写
