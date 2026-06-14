#!/usr/bin/env python3
"""Aggregate benchmark data from test runs."""

import json
import os
from pathlib import Path
from statistics import mean, stdev

def load_json(filepath):
    """Load JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def calculate_pass_rate(grading_data):
    """Calculate pass rate from grading data."""
    if not grading_data or "assertions" not in grading_data:
        return 0.0
    assertions = grading_data["assertions"]
    if not assertions:
        return 0.0
    passed = sum(1 for a in assertions if a.get("passed", False))
    return (passed / len(assertions)) * 100

def main():
    workspace = Path("iteration-1")
    skill_name = "transcription-correct"

    # Configurations - directory suffixes
    configs = [
        "with_skill",
        "without_skill"
    ]

    results = {config: [] for config in configs}

    # Collect data from each run
    # Directories are named like: eval-1-with_skill, eval-1-without_skill
    for run_dir in sorted(workspace.glob("eval-*-with_skill")):
        eval_id = run_dir.name.split("-")[1]  # Extract "1" from "eval-1-with_skill"

        for config in configs:
            dir_name = f"eval-{eval_id}-{config}"
            run_path = workspace / dir_name

            if not run_path.exists():
                print(f"Skipping {run_path} - doesn't exist")
                continue

            # Load timing data
            timing_file = run_path / "timing.json"
            timing_data = load_json(timing_file) or {"total_tokens": 0, "total_duration_seconds": 0}

            # Load grading data
            grading_file = run_path / "grading.json"
            grading_data = load_json(grading_file) or {"assertions": []}

            # Load metadata
            metadata_file = run_path / "eval_metadata.json"
            metadata = load_json(metadata_file) or {"eval_name": "unknown", "eval_id": 0}

            result = {
                "eval_id": metadata.get("eval_id", 0),
                "eval_name": metadata.get("eval_name", "unknown"),
                "tokens": timing_data.get("total_tokens", 0),
                "duration": timing_data.get("total_duration_seconds", 0),
                "pass_rate": calculate_pass_rate(grading_data)
            }

            results[config].append(result)
            print(f"Loaded {config}: {result['eval_name']} - {result['pass_rate']:.1f}%")

    # Calculate aggregate statistics
    benchmark = {
        "skill_name": skill_name,
        "configurations": []
    }

    for config in configs:
        runs = results[config]
        if not runs:
            print(f"No runs found for {config}")
            continue

        tokens = [r["tokens"] for r in runs]
        durations = [r["duration"] for r in runs]
        pass_rates = [r["pass_rate"] for r in runs]

        config_data = {
            "name": config,
            "pass_rate_mean": mean(pass_rates),
            "pass_rate_stddev": stdev(pass_rates) if len(pass_rates) > 1 else 0,
            "time_mean": mean(durations),
            "time_stddev": stdev(durations) if len(durations) > 1 else 0,
            "tokens_mean": mean(tokens),
            "tokens_stddev": stdev(tokens) if len(tokens) > 1 else 0,
            "runs": runs
        }

        benchmark["configurations"].append(config_data)

    # Calculate deltas
    if len(benchmark["configurations"]) == 2:
        with_skill = benchmark["configurations"][0]
        without_skill = benchmark["configurations"][1]

        benchmark["deltas"] = {
            "pass_rate": with_skill["pass_rate_mean"] - without_skill["pass_rate_mean"],
            "time": with_skill["time_mean"] - without_skill["time_mean"],
            "tokens": with_skill["tokens_mean"] - without_skill["tokens_mean"]
        }

    # Save benchmark
    output_file = workspace / "benchmark.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(benchmark, f, indent=2, ensure_ascii=False)

    print(f"\nBenchmark saved to {output_file}")

    # Generate markdown summary
    md_lines = [
        f"# Benchmark: {skill_name}\n",
        "## Summary\n",
        "| Configuration | Pass Rate | Time (s) | Tokens |",
        "|---|---|---|---|",
    ]

    for config in benchmark["configurations"]:
        md_lines.append(
            f"| {config['name']} | {config['pass_rate_mean']:.1f}% ± {config['pass_rate_stddev']:.1f}% | "
            f"{config['time_mean']:.1f} ± {config['time_stddev']:.1f} | "
            f"{config['tokens_mean']:.0f} ± {config['tokens_stddev']:.0f} |"
        )

    if "deltas" in benchmark:
        deltas = benchmark["deltas"]
        md_lines.extend([
            "\n## Deltas (with_skill - without_skill)",
            f"- Pass Rate: {deltas['pass_rate']:+.1f}%",
            f"- Time: {deltas['time']:+.1f}s",
            f"- Tokens: {deltas['tokens']:+.0f}",
        ])

    md_lines.extend(["\n## Per-Eval Breakdown\n"])

    for run in results["with_skill"]:
        md_lines.extend([
            f"### {run['eval_name']}",
            f"- with_skill: {run['pass_rate']:.1f}%, {run['duration']:.1f}s, {run['tokens']:.0f} tokens",
        ])

    md_file = workspace / "benchmark.md"
    md_file.write_text("\n".join(md_lines), encoding='utf-8')
    print(f"Markdown summary saved to {md_file}")

if __name__ == "__main__":
    main()
