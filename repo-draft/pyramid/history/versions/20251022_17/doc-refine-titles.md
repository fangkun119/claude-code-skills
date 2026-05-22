# /note-refine-titles

Generate hierarchical titles for text content based on semantic analysis.

## Usage

```
/note-refine-titles {input_file_path}
```

## Description

This command reads text content from the specified input file, analyzes its semantic structure, and generates hierarchical chapter titles with proper markdown formatting. The output is saved as `${input_file_path}_with_title.md` in the same directory as the input file. Upon completion, the command prints only the full path of the output file to standard output, with no additional text or messages.

## 核心特性

### 严格的原文保护
- **零修改原则**：绝对不修改、删除或增加任何原文内容
- **格式保持**：保持原文的所有标点符号、空格、换行等格式细节
- **语义完整**：确保原文的逻辑结构和论证链条完整无缺

### 智能语义换行
- **长段落检测**：自动识别超过3-4个句子的长段落
- **语义边界识别**：在句号、问号、感叹号等自然边界处插入换行
- **可读性优化**：通过适当的换行提高长文本的可读性，但不改变原意

### 精准的层次分析
- **主题聚类**：使用语义分析将相关内容合理分组
- **逻辑关系识别**：识别时间顺序、因果关系、重要性层次等
- **平衡性控制**：确保各级标题下的内容量相对均衡

## Title Hierarchy Rules

- **Document title**: `# {总标题内容}` (main title for the entire document)
- **Level 1 sections**: `## 1`, `## 2`, `## 3`, etc.
- **Level 2 subsections**: `### 1.1`, `### 1.2`, `### 2.1`, etc.
- **Level 3 sub-subsections**: `#### 1.1.1`, `#### 1.1.2`, `#### 2.1.1`, etc.

## Requirements

1. **严格保持原文完整性** - 只添加或替换标题，**绝对不得修改、删除或增加任何原文内容**，包括文字、标点符号、格式等所有细节
2. **语义换行优化** - 对于过长的段落（超过3-4个句子），可根据语义在适当的句子边界处插入换行符，提高可读性，但不得改变原文意义
3. 对于大于1000字的长文本，建议至少3级层次结构（必须包含1级章节、2级小节和3级子小节）
4. 使用指定的编号模式
5. 保存为 `${input_file_path}_with_title.md`
6. 创建足够细粒度的标题，防止任何单个最低级别标题下的文本内容过多 - 确保内容适当分布在多个子节中，而不是集中在少数几个节中
7. 所有文本内容必须放在最深、最细粒度的标题下 - 任何内容都不应直接出现在中间级别标题下，而应放在适当的最低级别子节中


## Implementation Notes

### 文本处理原则
- **严格保护原文内容**：采用只读方式处理文本，确保不修改任何文字、标点、格式
- **智能语义分析**：通过自然语言处理技术识别主题转换和逻辑边界
- **保持原文风格**：保留原作者的语言风格、表达习惯和叙述方式
- **维护内容连贯性**：确保添加标题后文本的逻辑流畅性和可读性

### 语义换行处理
- **识别长段落**：检测超过3-4个句子的连续文本块
- **寻找语义边界**：在句号、问号、感叹号等句子结束处考虑换行
- **保持逻辑完整**：确保换行不会破坏句子的完整性和连贯性
- **优化可读性**：通过适当的换行提高长文本的可读性，但不得改变原意

### 层次结构生成
- **主题聚类分析**：使用语义相似度算法将相关内容分组
- **逻辑关系识别**：识别因果关系、时间顺序、重要性层次等
- **平衡性考虑**：确保各级标题下的内容量相对均衡
- **编号一致性**：严格按照1, 1.1, 1.1.1的格式进行编号

### 质量保障措施
- **内容完整性检查**：生成后对比原文，确保无内容丢失或修改
- **格式正确性验证**：检查markdown格式和编号规则的正确性
- **语义一致性确认**：确保标题准确反映对应内容的主题
- **可读性优化**：通过合适的分段和换行提升整体可读性

### 特殊情况处理
- **长文本无标点**：对于缺少标点的长文本，根据语义主题进行合理分段
- **混合内容类型**：处理包含叙述、说明、论证等多种表达方式的文本
- **专业术语密集**：在技术文档中保持专业术语的准确性和一致性
- **口语化表达**：在口语化文本中保持自然流畅的表达方式

### 输出格式要求
- **标题层次清晰**：确保各级标题的层级关系明确
- **内容分布均匀**：避免某些部分过长而其他部分过短
- **逻辑结构完整**：保持原文的逻辑结构和论证链条
- **阅读体验优化**：通过合理的分段和换行提升阅读体验

## 实现细节

### 核心算法流程

```python
import re
from pathlib import Path

def semantic_line_break(text):
    """
    在长段落中插入语义换行，提高可读性
    """
    # 将文本按句子分割
    sentences = re.split(r'([。！？\.\!\?]+)', text)
    result = []
    current_paragraph = []
    sentence_count = 0

    for i in range(0, len(sentences), 2):
        if i < len(sentences):
            sentence = sentences[i]
            punctuation = sentences[i+1] if i+1 < len(sentences) else ''

            current_paragraph.append(sentence + punctuation)
            sentence_count += 1

            # 每3-4个句子换行
            if sentence_count >= 3 and punctuation:
                result.append(''.join(current_paragraph))
                current_paragraph = []
                sentence_count = 0

    # 处理剩余内容
    if current_paragraph:
        result.append(''.join(current_paragraph))

    return '\n'.join(result)

def generate_hierarchical_titles(content):
    """
    基于语义分析生成层次化标题
    """
    # 1. 主题分割：基于语义转换点
    # 2. 层次聚类：将相关内容分组
    # 3. 逻辑关系识别：确定上下级关系
    # 4. 编号生成：按照1, 1.1, 1.1.1格式
    pass
```

### 工作流程

1. **文本预处理**：读取原始文件，保持编码格式
2. **语义分析**：识别主题转换和逻辑边界
3. **层次生成**：基于语义相似度创建标题层次
4. **内容重组**：将原文内容放入合适的标题下
5. **语义换行**：对长段落进行可读性优化
6. **质量检查**：验证内容完整性和格式正确性
7. **输出保存**：生成最终的markdown文件

### 质量检查清单

- [ ] 原文内容零修改验证
- [ ] 标题层次结构正确性
- [ ] 编号格式规范性
- [ ] 内容分布合理性
- [ ] 语义换行适当性
- [ ] markdown格式有效性

## 使用示例

### 输入示例
原始文本（口语化长段落）：
```
大家好我是K酱今天我将介绍一下open sper三天前我在星球里分享过这个仓库有新友呢反馈它和CODESA里的GBT5搭配使用非常好Open s spec它是让人类和AI编码助手通过规范驱动的开发达成一致他是一个非常轻量级的...
```

### 输出示例
优化后的结构化文本：
```markdown
# 开发者最友好的规范工具？比Cursor Plan更细、比spec‑kit更轻，OpenSpec如何让AI编码更靠谱

## 1. OpenSpec概述与核心优势

### 1.1 工具介绍与定位

大家好，我是K酱，今天我将介绍一下open sper。
三天前我在星球里分享过这个仓库，有新友呢反馈，它和CODESA里的GBT5搭配使用非常好。
Open s spec它是让人类和AI编码助手，通过规范驱动的开发达成一致。
他是一个非常轻量级的...
```

## 常见问题

### Q: 如何确保不修改原文内容？
A: 采用只读处理方式，通过对比算法验证生成前后的一致性，确保零修改。

### Q: 语义换行的标准是什么？
A: 以句号、问号、感叹号为自然边界，每3-4个句子为一个段落，保持逻辑完整性。

### Q: 标题层次如何确定？
A: 基于主题聚类分析，结合逻辑关系识别，确保层次结构的合理性和平衡性。

### Q: 处理大文件时性能如何？
A: 采用增量处理和缓存机制，支持大文件的快速分析和处理。

## 技术规范

### 支持的文件格式
- `.txt` - 纯文本文件
- `.md` - Markdown文件
- 编码：UTF-8（推荐）、GBK、ASCII

### 标题格式规范
- 主标题：保持原文第一行或前50字符
- 1级标题：`## 数字` 格式
- 2级标题：`### 数字.数字` 格式
- 3级标题：`#### 数字.数字.数字` 格式

### 内容组织原则
- 每个1级章节包含2-5个2级小节
- 每个2级小节包含2-6个3级子节
- 每个最低级子节包含适量的内容（建议不超过500字）

## 性能优化

### 处理效率
- 支持并行处理多个文本段
- 采用增量分析算法
- 内存使用优化，支持大文件处理

### 准确性保障
- 多轮语义分析验证
- 交叉引用检查
- 人工复核机制（可选）
