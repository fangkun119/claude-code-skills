# 2026-05-22

/init 这是一个Claude Code Plugin Marketplace的Repo, 下面是用来生成 CLAUDE.md 的辅助信息：

交付给用户的最终结果
@.claude-plugin 目录是这个 MarketPlace 的配置
@note-tool 和 @pyramid 目录是 MarketPlace 目前已有的两个Plugin的代码（后续如果添加新的Plugin，需要相应地同步更新 CLAUDE.md）

用于开发和调试的目录
@repo-desktop 用于开发Plugin的工作目录，并不是交付给用户的最终结果，其中:
@repo-desktop/chats 是开发和升级Plugin时用到的提示词
@repo-desktop/regression 是用于回归测试的测试用例
@repo-desktop/workspaces 是用于开发和调试的文件
@repo-desktop/temp 是用于调试和测试的临时目录，任何测试和调试工作都在这个目录下进行，完成后清空该目录

编写Plugin时准寻的约定
(1) 如果Plugin中的Skill或Sub Agent需要使用Python：它应该只依赖Python 3和UV，如果用户没有安装，会直接退出并提示用户；它使用 .venv 中的Python 3来运行，如果用户的工作目录已有 .venv 则直接复用，如果没有则用 UV 基于 Python 3.12 创建 .venv

