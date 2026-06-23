# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This repo is a **Claude Code plugin marketplace** (`office-tool-marketplace`) containing two plugins published via the Claude Code plugin system. It also houses development workspaces, regression tests, and chat transcripts for plugin development.

## Plugin Architecture

### Marketplace Entry Point

`.claude-plugin/marketplace.json` registers all plugins with their source paths. Plugins are installed by users via `/plugin marketplace add` and `/plugin install`.

### note-tool Plugin

Document format conversion, content styling, directory archiving, and document rewriting.

- **skills/doc-to-md/**: Converts PDF/DOCX/DOC/PPT/PPTX/HTML to Markdown using `markitdown==0.1.3` in a Python 3.12+ venv. Uses TUNA PyPI mirror for dependency installation.
- **skills/dir-archive/**: Archives directories to `.tar.gz` with incremental update support. Includes a Python script at `scripts/archive_dir.py`.
- **skills/md-img-to-html/**: Converts all image formats in Markdown documents to HTML `<img>` tags. Supports standard Markdown format `![alt](path)` and Obsidian wikilink format `![[path]]`, including their width variants. Handles alt attribute checking and filling for existing HTML `<img>` tags.
- **skills/text-style/**: Applies HTML/CSS styles to specified text content using `<span>` tags with style attributes. Supports color, font size, background, borders, padding, and other CSS properties.
- **skills/transcription-correct/**: Corrects voice recognition errors in markdown transcription files using domain knowledge and iterative refinement. Handles large files by chunking content and uses multiple correction rounds.
- **skills/md-rewrite/**: Four-phase Markdown document rewriting skill: Phase 1 environment setup → Phase 2 requirements clarification (6-round interaction) → Phase 3 content rewriting → Phase 4 quality checks and title system validation. Supports writing style adjustment, chapter restructuring, content optimization, and target audience adaptation.

### Key Convention: Plugin Structure

Each plugin lives in its own top-level directory with:
```
<plugin-name>/
  .claude-plugin/
    plugin.json          # name, description, version, author
  agents/                # sub-agents (markdown frontmatter: name, description, model, color)
  commands/              # slash commands (markdown with usage instructions)
  skills/                # skills (SKILL.md with frontmatter: name, description, allowed-tools)
```

## Development Directories

- **repo-desktop/workspaces/**: Development workspaces for each plugin (pyramid, note-tool). Temporary files generated during the development and testing are all placed in this directory.
- **repo-desktop/regression/**: Regression test specs (markdown format) for plugin features
- **repo-desktop/chats/**: Chat transcripts and notes from plugin development sessions
- **.claude/commands/**: Project-level slash commands (e.g., `md-fix-voice-text`)


## Python Development

Use `uv` to create a Python 3.12 venv (`.venv`) for any Python code in this repo. Reuse existing `.venv` if present.

## Runtime Dependencies

- Python ≥3.12 + `uv` package manager (for note-tool skills)
- `markitdown[all]==0.1.3` (installed on-demand into `.venv`)
- TUNA PyPI mirror (`https://pypi.tuna.tsinghua.edu.cn/simple/`) used for Chinese network acceleration


## Naming Convensions

Naming must use precise, clear, and concise phrasing to express its meaning. For example, you can use names like ‘titles_scripts_tests’ to precisely indicate the test subject, while names like ‘quest_check_tests’ that are vague and general should not be used.


<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->


