/skill-creator 帮我 note-tool plugin 新增一个 Claude Code Skill，它用来纠正语音转录稿（markdown格式）中的语音识别错误。用户调用这个 skill 的时候需要传入：(1) 语音转录稿的文件路径；(2) 与这个转录稿有关的内容或知识领域提示，如果用户没有提供、需要Skill自己根据转入稿内容推测。 (3) 用户希望处理多少轮纠错，如果用户没有传入，Skill 自己根据文章的内容大小来自行决定. Skill不会直接在原文上进行更改, 他会给原文的base name加上一个后缀”_corrected.md" 作为纠正后文输出的文件（例如原文是 path/to/transcription.md , 那么改写后的文档就是 path/to/transcription_corrected.md 。

Skill 可以参考用户传入的信息分析错误识别的词语所对应的正确的内容是什么。用户传入的语音转录稿通常会比较大，一次难以全部处理。 Skill 需要对文件内容分块，一部分一部分的处理。Skill 也需要借助 Sub Agent 合理控制上下文的占用，Subagent 在执行完它的子任务之后，就会释放上下文，借助这个特性，Skill 可以避免上下文被撑得太满，从而保持处理能力。 语音转录稿很可能存在大量的识别错误，一次很难全部处理干净，Skill 需要对这个转录稿处理多次，可以根据文件的大小、以及用户输入内容是否指定处理多少次，来决定处理次数。 

@repo-desktop/workspaces/note-tool/transcription-correct/transcription-sample.md  是给你的测试文件，用户调用 Skills 处理这个语音转录稿时传入的知识领域提示为：这是一篇关于SEATA的语音转录稿，内容涉及Seata、Spring Cloud Alibaba、Spring Boot、分布式事务、AT模式、TC、TM、RM、XA、TCC、SAGA、两阶段提交、2PC、全局事务、分支事务、XID、undo log、全局锁、本地锁、@GlobalTransactional、@GlobalLock、OpenFeign、Netty、Remoting协议、读隔离、写隔离、脏读、读已提交、读未提交、SELECT FOR UPDATE、tx-service-group、JDBC、IndexOutOfBoundsException、server.enableParallelRequestHandler、MySQL、Oracle、达梦数据库、前置镜像、后置镜像、feature-dev分支

帮我 note-tool plugin 新增一个 Claude Code Skill ， 它用来纠正语音转录稿（markdown格式）中的语音识别错误，用户调用这个 skill 的时候需要传入语音转录稿的文件路径，及与这个转录稿有关的内容或者所涉及的知识领域等等。Skill 可以参考用户传入的信息分析错误识别的词语所对应的正确的内容是什么。 用户传入的语音转录稿通常会比较大，一次难以全部处理。 Skill 需要对文件内容分块，一部分一部分的处理。Skill 也需要借助 Sub Agent 合理控制上下文的占用，Subagent 在执行完它的子任务之后，就会释放上下文，借助这个特性，Skill 可以避免上下文被撑得太满，从而保持处理能力。 语音转录稿很可能存在大量的识别错误，一次很难全部处理干净，Skill 需要对这个转录稿处理多次，可以根据文件的大小、以及用户输入内容是否指定处理多少次，来决定处理次数。


