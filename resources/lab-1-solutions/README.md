# Lab 1 Solutions

This directory contains **solution scripts** for Lab 1: Build/Log Failure Triage.

**Note:** These are reference implementations. Students should try to write their own first, then compare with these solutions.

## Files

- **`build.log`** - Sample RDK build log (173 lines, realistic telemetry component build)
- **`01_grep.sh`** - Grep/awk approach (deterministic, fast, free)
- **`02_python_analysis.py`** - Python approach (structured, maintainable, free)
- **`03_llm_api_call.py`** - LLM approach (full log, intelligent, expensive)
- **`04_hybrid_approach.py`** - Hybrid approach (deterministic + LLM, recommended) ⭐
- **`03_llm_approach.md`** - LLM prompt template documentation
- **`04_hybrid_approach.md`** - Hybrid approach documentation

## Usage

### For Students

1. **Try writing your own first** - Don't look at solutions until you've attempted the exercise
2. **Compare your approach** - See how these solutions differ from yours
3. **Learn from differences** - What did the solutions do that you didn't?

### For Instructors

- Use these as reference implementations
- Show outputs during demo
- Compare student solutions with these
- Highlight best practices

## Approach Comparison

| Approach | Script | Speed | Cost | Accuracy | Auditability | Best For |
|----------|--------|-------|------|----------|--------------|----------|
| **Grep/Awk** | `01_grep.sh` | ⚡⚡⚡ Fast | 💰 Free | ⚠️ Low | ✅✅✅ High | Simple patterns |
| **Python** | `02_python_analysis.py` | ⚡⚡ Fast | 💰 Free | ⚠️ Medium | ✅✅✅ High | Structured parsing |
| **LLM (full)** | `03_llm_api_call.py` | ⚡ Slow | 💰💰💰 Expensive | ✅✅✅ High | ⚠️ Low | Complex analysis |
| **Hybrid** | `04_hybrid_approach.py` | ⚡⚡ Medium | 💰💰 Moderate | ✅✅✅ High | ✅✅ Medium | **Production use** ⭐ |

## Key Insights

1. **Hybrid approach is recommended** for production use
   - 70-90% cost savings vs. full log
   - Deterministic filtering (auditable)
   - LLM analysis (intelligent)
   - Best balance of speed, cost, accuracy

2. **Use deterministic methods first** - Always filter with grep/Python before sending to LLM

3. **Cost control is critical** - Track token usage, set limits, use hybrid approach

4. **Always validate LLM output** - Check evidence, verify line numbers, review confidence levels

## Running the Solutions

### Prerequisites

```bash
# From repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Each Approach

```bash
# Navigate to solutions directory
cd resources/lab-1-solutions

# 1. Grep approach
chmod +x 01_grep.sh
./01_grep.sh

# 2. Python approach
python3 02_python_analysis.py

# 3. LLM approach (requires API key)
export OPENAI_API_KEY=your_key
python3 03_llm_api_call.py

# 4. Hybrid approach (recommended)
python3 04_hybrid_approach.py --outdir .hybrid_out
cat .hybrid_out/hybrid_result.json
```

## Expected Outputs

### Grep Approach
- Error lines with line numbers
- Error count summary
- Top 3 error patterns

### Python Approach
- Error lines with line numbers
- Categorized error counts
- Top 3 error patterns by message

### LLM Approach
- JSON with root causes, evidence, confidence, next actions
- Human-readable summary
- Full log analysis

### Hybrid Approach
- Filtered error sections
- Token savings estimate
- LLM analysis of filtered data
- Same output format as LLM approach, but cheaper

## RDK Context

These solutions are designed for analyzing **github.com/rdkcentral** build logs - the RDK Software Stack codebase managed by the CMF team.

**Addresses pain point #1:** Log file analysis - understanding build failures quickly.

**For production use:**
- Integrate into Jenkins pipelines (see Lab 3)
- Use hybrid approach for cost efficiency
- Track costs and ROI
- Always validate LLM output

