---
name: transcription-correct
description: Correct voice recognition errors in markdown transcription files. Use this skill when the user wants to fix transcription errors in voice-to-text markdown files, especially for technical content with domain-specific terminology like distributed systems (Seata, Spring Cloud, etc.). The skill handles large files by chunking content and uses iterative correction rounds to thoroughly fix recognition errors. Trigger on phrases like "fix transcription", "correct voice text", "fix voice recognition errors", or when users mention transcription files with errors.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
---

# Transcription Correction Skill

This skill corrects voice recognition errors in markdown transcription files using domain knowledge and iterative refinement.

## Input Parameters

When invoked, this skill accepts:

1. **File path** (required): Path to the markdown transcription file to correct
2. **Domain context** (optional): Knowledge domain hints or technical terminology relevant to the content
3. **Correction rounds** (optional): Number of correction iterations (default: auto-determined based on file size)

## Output

Creates a corrected file with `_corrected.md` suffix. For example:
- Input: `path/to/transcription.md`
- Output: `path/to/transcription_corrected.md`

**Never modifies the original file.**

## Workflow

### Step 1: Read and Analyze Input

1. Read the transcription file
2. If no domain context provided, analyze content to infer technical domain:
   - Identify key terms, technologies, and subject matter
   - Extract technical terminology patterns
3. Determine correction rounds based on file size:
   - Small files (<5K words): 2 rounds
   - Medium files (5K-15K words): 3 rounds
   - Large files (>15K words): 4 rounds

### Step 2: Chunk the Content

For files over 2000 words, split into chunks:
- Chunk size: ~1500-2000 words
- Overlap: 100-200 words between chunks for context continuity
- Respect markdown boundaries (avoid splitting headings, code blocks, lists)

### Step 3: Iterative Correction with Sub-agents

For each correction round, spawn a sub-agent to process chunks:

**Sub-agent prompt template:**
```
You are correcting voice recognition errors in a technical transcription chunk.

Domain context: {domain_context}

Correct errors by:
1. Fixing homophone errors (e.g., "two" → "to", "write" → "right")
2. Correcting technical terminology using domain knowledge
3. Fixing punctuation and sentence structure
4. Preserving the original meaning and tone

Return ONLY the corrected markdown content without explanations or commentary.
```

**Process each chunk:**
- Send chunk + domain context to sub-agent
- Collect corrected chunk
- Proceed to next chunk

**After each round:**
- Reassemble chunks into complete document
- For rounds > 1, pass full corrected content as next round's input

### Step 4: Final Assembly and Output

1. After final correction round, write the complete corrected content to `{filename}_corrected.md`
2. Report summary to user:
   - Number of correction rounds performed
   - File sizes (original vs corrected)
   - Any significant corrections made

## Key Principles

- **Context-aware correction**: Use domain knowledge to distinguish homophones (e.g., "Seata" not "seater", "AT mode" not "at mode")
- **Preserve meaning**: Only change what's clearly a recognition error; preserve speaker's original phrasing
- **Technical accuracy**: Ensure code, technical terms, API names are correct
- **Markdown integrity**: Maintain proper markdown formatting (headings, lists, code blocks)

## Example Usage

```
User: "Fix the transcription errors in my Seata lecture transcription"
User: "Correct the voice text in transcriptions/seata-lecture.md"
User: "Fix transcription for this file about distributed transactions"
```

## When to Use This Skill

Trigger on user phrases like:
- "fix transcription"
- "correct voice text"
- "fix voice recognition errors"
- "transcription has errors"
- "voice-to-text needs correction"
- Files with transcription in the name/path that need fixing

**Do not trigger for**:
- General document editing (use standard editing instead)
- Translation tasks
- Content rewriting/style changes (use md-pyramid-rewrite instead)
