#!/bin/bash
# 快速测试脚本 - 重点测试代码块感知功能

echo "🚀 快速测试 validate_titles.py 代码块感知功能"
echo "================================================"

# 获取脚本目录和项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../../.." && pwd)"
VALIDATE_SCRIPT="$PROJECT_ROOT/note/skills/md-rewrite/scripts/validate_titles.py"

echo "📂 项目根目录: $PROJECT_ROOT"
echo "📜 验证脚本: $VALIDATE_SCRIPT"
echo ""

# 检查脚本是否存在
if [ ! -f "$VALIDATE_SCRIPT" ]; then
    echo "❌ 错误: validate_titles.py 脚本不存在"
    exit 1
fi

# 创建临时测试文件
TEMP_TEST="$SCRIPT_DIR/temp_quick_test.md"

echo "📝 创建临时测试文件..."

# 测试核心代码块感知功能
cat > "$TEMP_TEST" << 'EOF'
# 快速测试：代码块感知功能

## 1.1 正确的文档标题

这是文档的真实内容，应该被正确识别为标题。

```python
# 这是代码块内的注释，不应该被识别为标题
## 代码块内的井号符号
### 继续代码块内容
def test_function():
    # 更多代码注释
    ## 不应触发标题验证
    return "test"
```

## 1.2 代码块后的真实标题

这是另一个应该被正确识别的文档标题。

```javascript
## 代码块内的内容
// 这些都不应该被当作标题处理
function jsTest() {
    return true;
}
```

## 2.1 嵌套代码块测试

测试不同数量反引号的代码块。

````
四个反引号围栏
# 这些是代码内容
## 不应触发标题检测
```
内部包含三个反引号
### 仍然在代码块内
````

## 2.2 围栏后的正常标题

这是嵌套代码块后应该被正确识别的标题。

## 预期结果：
- 只识别：1.1, 1.2, 2.1, 2.2 四个真实文档标题
- 所有代码块内的 # 符号都被忽略
- 不报告任何标题格式错误
EOF

echo "✅ 测试文件创建完成"
echo ""
echo "🔍 运行验证脚本..."
echo "================================================"

# 运行验证脚本
python "$VALIDATE_SCRIPT" "$TEMP_TEST"

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ 脚本执行成功"
    echo ""
    echo "📊 验证要点："
    echo "1. 检查输出中是否只识别了 1.1, 1.2, 2.1, 2.2 四个标题"
    echo "2. 确认代码块内的 # 符号没有触发标题验证"
    echo "3. 验证嵌套代码块（四个反引号）被正确处理"
    echo ""
else
    echo ""
    echo "================================================"
    echo "❌ 脚本执行失败"
    echo "请检查脚本是否有错误"
    echo ""
fi

# 清理临时文件
rm -f "$TEMP_TEST"

echo "🧹 临时测试文件已清理"
echo ""
echo "🎯 如需完整测试，请运行: python run_tests.py"
echo "📖 查看详细说明，请阅读: README.md"