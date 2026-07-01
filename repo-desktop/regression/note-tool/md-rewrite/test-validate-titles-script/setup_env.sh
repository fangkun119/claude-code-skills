#!/bin/bash
# validate_titles.py 测试环境准备脚本

echo "🔧 validate_titles.py 测试环境准备"
echo "======================================"

# 检查 Python 版本（要求 ≥3.12）
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请安装 Python 3.12 或更高版本"
    exit 1
fi

# 获取 Python 版本
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python 版本: $PYTHON_VERSION"

# 检查版本是否满足要求（≥3.12）
MAJOR_VERSION=$(python3 -c 'import sys; print(sys.version_info.major)')
MINOR_VERSION=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 12 ]); then
    echo "❌ 错误: Python 版本过低，需要 ≥3.12，当前为 $PYTHON_VERSION"
    echo "请升级 Python 版本"
    exit 1
fi

echo "✅ Python 版本满足要求 (≥3.12)"

# 验证脚本存在（从测试目录定位项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../../" && pwd)"
SCRIPT_PATH="$PROJECT_ROOT/note/skills/md-rewrite/scripts/validate_titles.py"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误: 脚本不存在 $SCRIPT_PATH"
    exit 1
fi

echo "✅ 脚本路径验证成功: $SCRIPT_PATH"

# 测试脚本语法正确性
if ! python3 -m py_compile "$SCRIPT_PATH" &> /dev/null; then
    echo "❌ 错误: 脚本存在语法错误"
    exit 1
fi

echo "✅ 脚本语法验证成功"

echo ""
echo "🎉 环境准备完成！"
echo "======================================"
echo "可以开始运行测试："
echo "  - 自动化测试: python3 run_tests.py"
echo "  - 快速测试: ./quick_test.sh"
echo "  - 手动测试: python3 $SCRIPT_PATH <测试文件.md>"
echo ""