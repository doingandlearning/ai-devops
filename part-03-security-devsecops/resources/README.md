# Black Duck AI Assistant - Resources

This directory contains resources for **Mini-Lab A: License/IP (Black Duck reality)**.

## Files

- **`wifi_hal.c`** - Source file with copyright/license issues identified by Black Duck
- **`bd-report.txt`** - Black Duck Jira ticket (BD-1290) with compliance notes
- **`blackduck_ai_assistant.py`** - Python script that demonstrates the hybrid approach for copyright compliance

## Demo Script: `blackduck_ai_assistant.py`

This script demonstrates three key concepts:

1. **Extracting code to reduce token usage** - Only sends relevant code sections to LLM
2. **Using BD report to decrease hallucinations** - Structured input provides context
3. **Using LLM to enhance but get structured responses** - JSON output with evidence

### Usage

```bash
# Extract code sections only (no LLM call)
python blackduck_ai_assistant.py \
  --bd-report bd-report.txt \
  --source wifi_hal.c \
  --outdir compliance \
  --extract-only

# Full demo: Extract + LLM analysis
python blackduck_ai_assistant.py \
  --bd-report bd-report.txt \
  --source wifi_hal.c \
  --outdir compliance \
  --model gpt-4o
```

### Environment Setup

```bash
# Install dependencies
pip install openai

# Set API key (or pass via --api-key)
export OPENAI_API_KEY=your_key_here
```

### Output

The script generates two artifacts:

1. **`compliance/extracted_code.json`** - Extracted code sections (like a git diff)
   - Shows which lines were referenced in BD report
   - Includes context around each reference
   - Demonstrates token savings

2. **`compliance/ai_notice.json`** - Structured LLM response
   - `notice_additions`: Lines to add to NOTICE file
   - `license_additions`: License text to add to LICENSE file
   - `evidence`: File paths, line numbers, and reasoning
   - `confidence`: high/medium/low
   - `review_required`: Boolean flag

### Example Output

```json
{
  "metadata": {
    "source_file": "wifi_hal.c",
    "bd_report": "bd-report.txt",
    "extracted_sections": 3,
    "confidence": "high",
    "review_required": true
  },
  "notice_additions": [
    "Code from iw is:\nCopyright (c) {{ YEAR }} {{ COPYRIGHT HOLDER }}\nLicensed under the ISC License"
  ],
  "license_additions": [
    "ISC License text..."
  ],
  "evidence": [
    {
      "file": "wifi_hal.c",
      "lines": [30, 36],
      "why": "Copyright notice for rxStatsInfo_callback found in comments"
    }
  ],
  "confidence": "high",
  "review_required": true
}
```

## Demo Flow

### Step 1: Extract Code Sections
- Parse BD report for file:line references
- Extract relevant code sections with context
- Save as `extracted_code.json` artifact
- **Result:** Token usage reduced by 80-90% vs. sending full file

### Step 2: Call LLM with Structured Prompt
- Combine extracted code + BD report notes
- Use prompt template from README.md (lines 30-46)
- Request structured JSON response
- **Result:** LLM provides evidence-backed compliance suggestions

### Step 3: Save Structured Results
- Parse LLM JSON response
- Add metadata (confidence, review flags)
- Save as `ai_notice.json`
- **Result:** Reviewable, evidence-backed compliance artifacts

## Key Takeaways

1. **Hybrid Approach:** Extract code first, then analyze (like log triage Lab 1)
2. **Structured Input:** BD report provides context to reduce hallucinations
3. **Structured Output:** JSON format ensures consistent, reviewable results
4. **Evidence Required:** All suggestions must cite file paths and line numbers
5. **Human Review:** Always required - AI assists, doesn't replace

## Integration with Lab

This script is used in **Part 3, Mini-Lab A (14:05-14:25)**:

1. Run script to extract code sections
2. Review `extracted_code.json` to see what was extracted
3. Run script with LLM to generate compliance suggestions
4. Review `ai_notice.json` for evidence and confidence levels
5. Discuss: How does this compare to manual BD analysis?

## Troubleshooting

**Error: OPENAI_API_KEY not set**
```bash
export OPENAI_API_KEY=your_key_here
# OR
python blackduck_ai_assistant.py --api-key your_key_here ...
```

**Error: Could not parse JSON from LLM response**
- LLM may have returned markdown-wrapped JSON
- Script attempts to extract JSON from code blocks
- If still fails, check LLM response format

**No references found in BD report**
- Check BD report format matches expected patterns
- Script looks for: `filename:line`, `before line`, function names
- Add more patterns in `_parse_bd_references()` if needed

