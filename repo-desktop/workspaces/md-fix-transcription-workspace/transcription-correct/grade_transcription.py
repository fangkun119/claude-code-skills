#!/usr/bin/env python3
"""Grade transcription correction test runs."""

import os
import json
import sys
from pathlib import Path

def grade_run(run_dir):
    """Grade a single test run."""
    results = []

    # Find output file
    outputs_dir = Path(run_dir) / "outputs"
    output_files = list(outputs_dir.glob("*corrected*.md"))

    # Assertion 1: Output file exists with correct naming
    if output_files:
        results.append({
            "text": "Output file exists with _corrected suffix",
            "passed": True,
            "evidence": f"Found: {output_files[0].name}"
        })
    else:
        results.append({
            "text": "Output file exists with _corrected suffix",
            "passed": False,
            "evidence": "No file with '_corrected' suffix found"
        })

    if not output_files:
        return results

    output_file = output_files[0]
    content = output_file.read_text(encoding='utf-8')

    # Assertion 2: Output file is not empty
    results.append({
        "text": "Output file has reasonable content size",
        "passed": len(content) > 1000,
        "evidence": f"File size: {len(content)} characters"
    })

    # Assertion 3: Key technical terminology preserved
    key_terms = [
        "Seata", "TC", "TM", "RM", "AT mode", "undo log",
        "global lock", "local lock", "@GlobalTransactional",
        "两阶段提交", "2PC", "分布式事务", "全局事务"
    ]

    missing_terms = [term for term in key_terms if term not in content]
    results.append({
        "text": "Key technical terminology preserved",
        "passed": len(missing_terms) == 0,
        "evidence": f"All terms present" if not missing_terms else f"Missing: {', '.join(missing_terms)}"
    })

    # Assertion 4: Output is valid markdown (basic check)
    has_markdown_structure = any(char in content for char in ['#', '##', '*', '-', '1.', '2.'])
    results.append({
        "text": "Output has markdown structure",
        "passed": has_markdown_structure,
        "evidence": "Markdown formatting detected" if has_markdown_structure else "No clear markdown structure"
    })

    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_dir = sys.argv[1]
        grading = {
            "assertions": grade_run(run_dir)
        }
        print(json.dumps(grading, indent=2, ensure_ascii=False))
    else:
        print("Usage: grade_transcription.py <run_dir>")
