# Benchmark: transcription-correct

## Summary

| Configuration | Pass Rate | Time (s) | Tokens |
|---|---|---|---|
| with_skill | 75.0% ± 0.0% | 44.3 ± 2.1 | 85000 ± 3000 |
| without_skill | 75.0% ± 0.0% | 39.3 ± 1.5 | 75000 ± 3000 |

## Deltas (with_skill - without_skill)
- Pass Rate: +0.0%
- Time: +5.0s
- Tokens: +10000

## Per-Eval Breakdown

### seata-technical-transcription
- with_skill: 75.0%, 45.0s, 85000 tokens
### auto-detect-domain-context
- with_skill: 75.0%, 42.0s, 82000 tokens
### specify-correction-rounds
- with_skill: 75.0%, 46.0s, 88000 tokens