# Sample Command to Run the Agent

# V 1.0.0 - 1.0.3

## 1. 文章改写

按照金字塔原理，对文章进行改写

```bash
@agent-doc-rewriter @research/pyramid/test/tech_doc.md  
# 类似地，也可以用其它文件做测试
# @agent-doc-rewriter @research/pyramid/test/expository.txt
# @agent-doc-rewriter @research/pyramid/test/narrative.txt 
# @agent-doc-rewriter @research/pyramid/test/persuasive_1.txt 
# @agent-doc-rewriter @research/pyramid/test/persuasive_2.txt 
```

检查改写文章的信息覆盖程度

[./test/tech_doc_cov_check.md](./test/tech_doc_cov_check.md)


## 2. 根据信息丢失情况，重新进行改写


```bash
根据 `@research/pyramid/test/tech_doc_cov_check.md` 指出的问题生成requirements参数
然后重新执行 `@agent-doc-rewriter @research/pyramid/test/tech_doc.txt "{requirements}"` 进行改写
```

查看检查结果
[./test/tech_doc_cov_check.md](./test/tech_doc_cov_check.md)

## 3. 文档润色

```bash
@agent-doc-polisher @research/pyramid/test/tech_doc_rewritten.md 

# 类似地，还可以对其它改写结果进行润色
# @agent-doc-polisher @research/pyramid/test/expository.txt
# @agent-doc-polisher @research/pyramid/test/narrative_rewritten.txt "流畅" 
# @agent-doc-polisher @research/pyramid/test/persuasive_1_rewritten.txt "check logic"
# @agent-doc-polisher @research/pyramid/test/persuasive_2_rewritten.txt "check logic"
```

也可以让 claude code 启动一批 sub agent，每个 sub agent 有自己独立的上下文
```bash
执行`@agent-doc-polisher @research/pyramid/test/expository.txt`, 执行`@agent-doc-polisher @research/pyramid/test/narrative_rewritten.txt "流畅"`, 执行`@agent-doc-polisher @research/pyramid/test/persuasive_1_rewritten.txt "缺陷检测"`, 执行`@agent-doc-polisher @research/pyramid/test/persuasive_2_rewritten.txt "缺陷检测"`
```

## 附录：其它命令 

在claude CLI中执行下列命令

```bash
@agent-doc-rewriter @research/pyramid/example/claude_agent_skills/skills.md

@agent-doc-rewriter @research/pyramid/example/claude_agent_skills/overview.md
根据 `@research/pyramid/example/claude_agent_skills/overview_cov_check.md` 指出的问题生成requirements参数，然后重新执行 `@agent-doc-rewriter @research/pyramid/example/claude_agent_skills/overview.md "{requirements}"` 进行改写

@agent-doc-rewriter @research/pyramid/example/claude_agent_skills/quickstart.md

@agent-doc-rewriter @research/pyramid/example/claude_agent_skills/best_practices.md


```


# V 0.1.0 

```text
先执行 @agent-pyramid:md-rewriter 处理 @research/pyramid/example/rewriter-with-charts/long_complex_book.md , 然后用 @agent-pyramid:md-content-gap-filler 处理生成的 long_complex_book_rewritten.md , 最后再用 @agent-pyramid:md-chapter-refiner 依次完善 long_complex_book_rewritten.md 中的每一章


先执行 @agent-pyramid:md-content-gap-filler @research/pyramid/example/rewriter-with-charts/long_complex_book_rewritten.md 然后再用 @agent-pyramid:md-chapter-refiner 完善 
@research/pyramid/example/rewriter-with-charts/long_complex_book_rewritten.md 中的每一章, 结果更新到 @research/pyramid/example/rewriter-with-charts/long_complex_book_rewritten.md 
```




