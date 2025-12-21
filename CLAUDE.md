# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research and experimentation repository for Claude Code capabilities, focusing on implementing Slash Commands, MCP (Model Context Protocol) servers, Sub-Agents, and document processing workflows.

## Repository Structure

### Core Directories

- **`.claude/`**: Claude Code configuration and permissions
  - `settings.local.json`: Permissions configuration for allowed commands
- **`tasks/`**: Main workspace for different task types
  - `tasks/note/`: Document rewriting and note generation workflows
  - `tasks/convert/`: Document conversion (PDF, PPT) processing

### Document Processing Architecture

The repository implements a sophisticated document processing pipeline based on the Pyramid Principle:

#### Reference Materials (`tasks/note/reference/`)
- **Pyramid Principle guides**: Comprehensive writing methodology based on Barbara Minto's framework
- **Persuasive writing techniques**: Methods for argument construction and issue analysis
- These serve as knowledge bases for agent prompt engineering

#### Test Files (`tasks/note/test/`)
- Sample documents for testing: narrative, expository, persuasive texts
- Used for validating document processing workflows

#### Historical Versions (`tasks/note/history/versions/`)
- Timestamped snapshots of agent and command configurations
- Tracks evolution of document processing capabilities
- Format: `YYYYMMDD_HH/` containing agents/ and commands/ subdirectories

## Claude Code Components

### Permissions Configuration
The `.claude/settings.local.json` defines allowed operations:
- Directory creation commands
- Document processing slash commands (`/re-wt:md-*`)
- Specific workflow commands for text refinement

### Slash Commands (Historical)
Located in versioned directories, these commands implement:
- `/doc-pyramid-rewrite`: Document restructuring using Pyramid Principle
- `/doc-highlight-persuasive-structure`: Persuasive analysis enhancement
- `/doc-refine-titles`: Title optimization
- `/doc-fluent`: Text fluency improvement
- `/doc-warn-logic-flaw`: Logic validation
- `/doc-check-coverage`: Content coverage analysis

### Sub-Agents (Historical)
Specialized agents for document processing:
- `doc-polisher`: Text fluency and readability enhancement
- `doc-rewriter`: Comprehensive document restructuring pipeline

## Development Workflow

### Document Processing Tasks
1. **Input**: Raw text files in `tasks/note/test/`
2. **Processing**: Apply specialized agents/commands based on document type
3. **Output**: Rewritten documents with enhanced structure, logic, and readability

### Agent Development
- Agents are configured as markdown files with specific prompts
- Historical versions track prompt evolution and effectiveness
- New agents should follow the established naming convention and directory structure

### Command Development
- Slash commands are defined as markdown workflows
- Commands leverage the Pyramid Principle methodology
- Permission updates required in `.claude/settings.local.json` for new commands

## Key Methodologies

### Pyramid Principle Application
This repository heavily implements Barbara Minto's Pyramid Principle:
- **Conclusion first**: Start with main conclusions
- **Logical grouping**: MECE (Mutually Exclusive, Collectively Exhaustive) categorization
- **Hierarchical structure**: Clear parent-child relationships between ideas
- **Question-answer flow**: Natural progression from reader questions to answers

### Document Types Handled
- **Narrative texts**: Storytelling and descriptive content
- **Expository texts**: Informational and educational content
- **Persuasive texts**: Argumentative and analytical content
- **Technical documentation**: Process and technical explanations

## Common Development Tasks

### Adding New Document Processing Workflows
1. Create test cases in `tasks/note/test/`
2. Develop agent configurations in appropriate versioned directory
3. Update permissions in `.claude/settings.local.json`
4. Test with existing reference materials

### Managing Agent Versions
- Use timestamped directories for version control
- Maintain backward compatibility when possible
- Document changes in agent configuration files

### Processing New Document Types
- Add reference materials to `tasks/note/reference/`
- Create specialized test cases
- Develop targeted processing workflows

## Notes

- This is primarily a research repository for Claude Code capabilities
- Focus is on document processing and text enhancement workflows
- Version history is maintained for both development and research purposes
- The repository structure supports systematic experimentation with different AI-assisted writing methodologies.
- 再加一点限制,code block前面要有一行空行,并且```不要有任何缩进. 你看看这个限制加在提示词哪里比较好 @pyramid/commands/md-pyramid-rewrite.md