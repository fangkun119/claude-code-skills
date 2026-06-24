/skill-creator

在 note plugin 中创建一个用于文档改写的claude code skill，名称为 md-rewrite 

文档改写流程介绍文档见 @repo-desktop/chats/note-tool/specs/md-rewrite-spec.md   

创建 Skill 之前请先阅读这个文档，理解改写流程，仔细思考该如何和把它转换为一个 Skill 并且符合 /skill-creator的要求。

测试文件在 @regression/note-tool/md-rewrite/test-case/ 目录下，其中
1. sample_file.md 是改写文档的内容来源
2. prompt.md 是提示词参考、它引用的 requirements.md、workflow_implementation.md 帮你独立完成自动化测试
你可以基于执行目录的变化，参考 prompt.md 生成你自己的提示词来调用 Skill 进行测试

注意上面的测试文件很大，你可以先模仿它，创建一些小文件进行测试和评估，最后再再一个拥有独立上下文的Sub Agent中用这个大文件进行测试（它非常大、需要通过独立上下文的Sub Agent来节省主Agent的上下文）

think ultra hard

