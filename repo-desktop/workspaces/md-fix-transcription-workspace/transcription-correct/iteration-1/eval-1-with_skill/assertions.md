# Assertions for Seata Technical Transcription Test

## Objective Assertions

1. **Output file exists with correct naming**
   - Check that `transcription-sample_corrected.md` or similar with `_corrected` suffix exists in outputs directory
   - Expected: File exists

2. **Output file is not empty**
   - Check that output file has content (> 1000 characters for a 7000+ word input)
   - Expected: File size is reasonable

3. **Key technical terminology preserved**
   - Check that critical SEATA terms are present in output
   - Terms to verify: "Seata", "TC", "TM", "RM", "AT mode", "undo log", "global lock", "local lock", "@GlobalTransactional", "两阶段提交", "2PC"
   - Expected: All key terms present

4. **Output is valid markdown**
   - Check that file has proper markdown structure
   - Expected: File parses as markdown without errors

5. **Original file not modified**
   - Check that original transcription-sample.md is unchanged
   - Expected: Original file unchanged
