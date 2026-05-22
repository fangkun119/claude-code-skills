# claude-code-research

## 1. 项目用途

研究各类使用 Claude Code 提高工作效率的方法。
通过实验和调优，实现相关的 Slash Command、Sub Agents、Skills，通过 Claude Code Plugin 发布。

## 2. 插件使用方法

本仓库包含一个Claude Code插件市场 `office-tool-marketplace`，提供两个实用插件：

### 可用插件

1. **pyramid** - 基于金字塔原理的文档重写工具
   - 功能：根据Barbara Minto的《金字塔原理》重写文本文档（txt, md）
   - 包含命令：文档重构、说服力分析、标题优化、逻辑检查等

2. **note-tool** - 文档格式转换工具
   - 功能：将各种文档格式（pdf, docx, doc, pptx, ppt）转换为Markdown
   - 使用markitdown工具进行转换

### 安装方法

从GitHub仓库安装插件市场：

```bash
# 1. 添加插件市场
/plugin marketplace add git@github.com:fangkun119/claude-code-research.git

# 2. 浏览可用插件（推荐）
/plugin

# 3. 或者直接安装特定插件
/plugin install pyramid@office-tool-marketplace
/plugin install note-tool@office-tool-marketplace
```

还可以从本地添加`插件市场`，下面是演示

```bash
# 在terminal克隆claude-code-research repo到本地
mkdir -p /User/ken/code && cd /User/ken/code
git clone git@github.com:fangkun119/claude-code-research.git

# 进入claude CLI
claude 

# 执行/plugin命令添加marketplace
/plugin marketplace add /Users/ken/Code/claude-code-research/
```

### 使用方法

安装完成后，重启Claude Code，然后可以使用以下方式验证安装：

使用金字塔原理对文章进行改写

```bash
@agent-pyramid:md-rewriter @myfile.txt 
@agent-pyramid:md-polisher @my_file_rewritten.md "检查逻辑" 
```

文档转换技能：通过自然语言触发，如果在提示词中提到这个skill的名称`note-tool:md-gen`可以对skill触发率有更好的保证

```txt
将 @to_path/myfile.docx 转换成 markdown
```

### 管理插件

```bash
# 启用/禁用插件
/plugin enable pyramid@office-tool-marketplace
/plugin disable pyramid@office-tool-marketplace

# 卸载插件
/plugin uninstall pyramid@office-tool-marketplace

# 移除插件市场
/plugin marketplace remove office-tool-marketplace
```

## 3. 目录介绍

### 3.1 `.claude`

功能：Claude Code权限配置文件

文件存储：

* `settings.local.json`：Claude Code本地权限配置，定义允许执行的命令和操作

### 3.2 `.claude-plugin`

功能：Claude Code插件市场配置文件

文件存储：

* `marketplace.json`：定义插件市场信息和可用插件列表

### 3.3 `pyramid`

功能：基于金字塔原理的文档重写插件

目录结构：

* `.claude-plugin/`：插件配置文件
* `agents/`：包含文档润色和重写的Sub-Agents
* `commands/`：包含文档重构、标题优化等Slash Commands

### 3.4 `note-tool`

功能：文档格式转换插件

目录结构：

* `.claude-plugin/`：插件配置文件
* `skills/`：包含PDF、PPT、Word转Markdown的技能

### 3.5 `research`

功能：用于插件开发和调试

目录结构：

* `pyramid/`：金字塔原理插件的开发和调试
* `note-tool/`：文档转换插件的开发和调试

