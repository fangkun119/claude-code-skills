# validate_titles.py 测试用例集

## 概述

这是为 `validate_titles.py` 脚本设计的全面测试用例集，专门测试 Markdown 文档标题验证功能的各个方面，包括新增的代码块感知功能。

## 测试用例列表

### 📋 基础功能测试
- **[01_basic_four_level_titles.md](01_basic_four_level_titles.md)** - 基础四级标题体系测试
  - 测试标准的四级标题结构识别
  - 验证标题层级关系正确性

### 🔧 代码块感知测试（新功能重点）
- **[02_code_block_awareness_basic.md](02_code_block_awareness_basic.md)** - 基础代码块感知测试
  - 验证脚本正确跳过代码块内部的标题符号
  - 确保代码内容不被误判为文档标题

- **[03_nested_code_blocks.md](03_nested_code_blocks.md)** - 嵌套代码块测试
  - 测试不同数量反引号的围栏识别
  - 验证嵌套代码块的正确处理

### ❌ 格式错误检测测试
- **[04_invalid_title_formats.md](04_invalid_title_formats.md)** - 标题格式错误检测测试
  - 测试各种标题格式错误的识别
  - 验证编号格式、层级格式的错误检测

### 🚨 边界情况测试
- **[05_overflow_and_edge_cases.md](05_overflow_and_edge_cases.md)** - 越级标题和边界情况测试
  - 测试 Level 5+ 越级标题检测
  - 验证空标题、层级跳跃等边界情况

### 🔢 编号连续性测试
- **[06_numbering_sequence.md](06_numbering_sequence.md)** - 标题编号连续性和层级关系测试
  - 测试编号连续性检查功能
  - 验证层级关系的合理性检查

### 🎯 特殊内容检查测试
- **[07_empty_and_special_cases.md](07_empty_and_special_cases.md)** - 空标题和特殊内容检查测试
  - 测试空标题检测功能
  - 验证特殊格式标题的处理

### 🌐 真实场景测试
- **[08_real_document_scenario.md](08_real_document_scenario.md)** - 真实文档场景综合测试
  - 模拟真实的技术文档结构
  - 测试多种代码语言混合的复杂场景

### 🌍 多语言支持测试
- **[09_multilingual_unicode.md](09_multilingual_unicode.md)** - 多语言和 Unicode 字符支持测试
  - 测试中文、英文、日文、韩文等多语言支持
  - 验证 RTL 语言（阿拉伯语、希伯来语）的处理
  - 测试 Emoji、数学符号等特殊 Unicode 字符

### ⚡ 性能测试
- **[10_performance_large_files.md](10_performance_large_files.md)** - 性能和大文件处理测试
  - 测试大量标题和代码块的处理性能
  - 验证超长标题、深层嵌套等极端情况

### 🛡️ 错误恢复测试
- **[11_error_recovery_edge_cases.md](11_error_recovery_edge_cases.md)** - 错误恢复和极限边界测试
  - 测试不完整代码块的处理
  - 验证特殊字符、编码问题的健壮性
  - 测试异常格式的恢复能力

## 测试环境设置

### 环境前提

- **Python ≥3.12** 已安装
- **工作目录可写**

### 环境准备

`validate_titles.py` 脚本仅使用 Python 标准库，无需安装外部依赖。

**检查 Python 版本**：
```bash
python3 --version  # 应显示 Python 3.12 或更高版本
```

**环境验证**：
```bash
# 验证脚本可执行
python3 note/skills/md-rewrite/scripts/validate_titles.py --help
```

**注意**：与其他 note 技能不同，此脚本不需要 `uv`、虚拟环境或 `markitdown` 依赖。

### 环境准备脚本（可选）

如果需要与其他测试保持一致的环境管理，可以使用以下脚本：

```bash
# 检查 Python 版本（要求 ≥3.12）
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python 版本: $PYTHON_VERSION"

# 验证脚本存在
SCRIPT_PATH="note/skills/md-rewrite/scripts/validate_titles.py"
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误: 脚本不存在 $SCRIPT_PATH"
    exit 1
fi

echo "✅ 环境准备完成，可以开始测试"
```

## 使用方法

### 自动化测试运行

使用提供的 Python 测试运行器：

```bash
# 进入测试目录
cd repo-desktop/regression/note-tool/md-rewrite/test-validate-titles-script

# 运行所有测试
python3 run_tests.py
```

测试运行器会：
1. 自动发现所有测试用例文件
2. 逐个运行 `validate_titles.py` 脚本
3. 收集和分析结果
4. 生成 Markdown 和 JSON 格式的测试报告

### 快速环境验证

首先验证测试环境：

```bash
# 进入测试目录
cd repo-desktop/regression/note-tool/md-rewrite/test-validate-titles-script

# 运行环境准备脚本
./setup_env.sh
```

### 手动测试

对单个测试用例进行手动测试：

```bash
# 从项目根目录运行
python3 note/skills/md-rewrite/scripts/validate_titles.py \
  repo-desktop/regression/note-tool/md-rewrite/test-validate-titles-script/02_code_block_awareness_basic.md
```

或使用绝对路径：

```bash
python3 /Users/ken/Code/cursor/claude-skills/note/skills/md-rewrite/scripts/validate_titles.py \
  /Users/ken/Code/cursor/claude-skills/repo-desktop/regression/note-tool/md-rewrite/test-validate-titles-script/02_code_block_awareness_basic.md
```

## 测试报告

测试运行后会生成以下报告文件：

- **Markdown 报告** (`test_report_YYYYMMDD_HHMMSS.md`) - 人类可读的详细测试报告
- **JSON 报告** (`test_report_YYYYMMDD_HHMMSS.json`) - 机器可读的结构化测试数据

## 测试覆盖范围

### 功能覆盖
- ✅ 四级标题体系识别
- ✅ 代码块感知（新增核心功能）
- ✅ 标题格式验证
- ✅ 编号连续性检查
- ✅ 层级关系验证
- ✅ 越级标题检测
- ✅ 空标题检测
- ✅ 特殊字符处理

### 场景覆盖
- ✅ 正常文档结构
- ✅ 代码块混合内容
- ✅ 嵌套代码块
- ✅ 多语言内容
- ✅ 大文件处理
- ✅ 边界情况
- ✅ 错误恢复

### 技术覆盖
- ✅ 不同代码语言（Python, Java, JavaScript, YAML, 等）
- ✅ 不同 Markdown 格式
- ✅ Unicode 字符支持
- ✅ 性能和内存效率

## 预期测试结果

### 代码块感知功能测试（重点）
- ✅ 代码块内的 `#` 符号应被完全忽略
- ✅ 支持 3、4、5 等不同数量的反引号围栏
- ✅ 正确处理嵌套代码块
- ✅ 最多支持 3 个空格缩进的代码块

### 标题验证功能
- ✅ 正确识别符合规范的标题
- ✅ 检测格式错误的标题
- ✅ 验证编号连续性
- ✅ 检查层级关系合理性

### 边界情况处理
- ✅ 优雅处理不完整的代码块
- ✅ 正确处理空标题
- ✅ 支持各种 Unicode 字符
- ✅ 处理超长标题内容

## 添加新测试

要添加新的测试用例：

1. 创建新的 Markdown 文件，命名格式：`XX_test_name.md`
2. 使用以下结构：
   ```markdown
   # 测试用例 XX: 测试名称

   ## 测试目的
   描述测试的目标和验证内容

   ## 测试内容
   实际的 Markdown 测试内容

   ## 预期结果
   描述期望的测试结果
   ```

3. 运行测试时，新的测试用例会自动被包含

## 故障排除

### 环境问题
**Python 版本错误**：
```bash
# 检查 Python 版本
python3 --version

# 如果版本 < 3.12，需要升级 Python
```

**脚本路径错误**：
```bash
# 验证脚本路径是否正确
ls -la note/skills/md-rewrite/scripts/validate_titles.py

# 或使用绝对路径
python3 /Users/ken/Code/cursor/claude-skills/note/skills/md-rewrite/scripts/validate_titles.py --help
```

### 脚本执行失败
- 检查 `validate_titles.py` 脚本路径是否正确
- 确认 Python 版本 ≥3.12
- 验证脚本文件权限：`chmod +x validate_titles.py`（如果需要）

### 测试结果分析
- 查看 Markdown 报告中的详细分析
- 检查 JSON 报告中的结构化数据
- 对比预期结果和实际输出

### 代码块识别问题
- 确认反引号数量是否匹配
- 检查缩进是否超过 3 个空格
- 验证代码块边界是否正确识别

## 贡献指南

这个测试集是持续改进的，欢迎：
- 添加新的测试场景
- 改进现有测试用例
- 完善测试运行器功能
- 优化测试报告格式

## 版本历史

- **v1.0** (2026-06-29) - 初始版本，包含 11 个测试用例，重点测试代码块感知功能