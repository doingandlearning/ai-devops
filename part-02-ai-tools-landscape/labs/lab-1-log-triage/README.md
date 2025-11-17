# Lab 1: Build/Log Failure Triage

**Time:** 45 minutes  
**Addresses your pain point #1: Log file analysis**

**You'll do:** baseline automation → AI/hybrid → prompt hardening → compare

## Setup

```bash
# From repo root
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Navigate to lab directory
cd part-02-ai-tools-landscape/labs/lab-1-log-triage

# Copy solution scripts (if provided)
cp ../../../../resources/lab-1-solutions/*.sh .
cp ../../../../resources/lab-1-solutions/*.py .

# Verify files
ls build.log 01_grep.sh 02_python_analysis.py 03_llm_api_call.py 04_hybrid_approach.py
```

## Exercise 2.1: Baseline Automation (15 minutes)

**Task:** Extract top 3 error patterns from the build log using deterministic methods.

### Option A: Grep/Awk

```bash
chmod +x 01_grep.sh
./01_grep.sh | tee out_grep.txt
```

### Option B: Python

```bash
python3 02_python_analysis.py | tee out_python.txt
```

### Option C: Write Your Own

Create your own script to extract error patterns. Compare with the provided solutions.

### Capture Results

Fill in this table:

| Metric | Value |
|--------|-------|
| Time to run | {{ PLACEHOLDER }} |
| Top 3 patterns (with line numbers) | {{ PLACEHOLDER }} |
| What breaks if log format changes? | {{ PLACEHOLDER }} |
| Accuracy (did it find real errors?) | {{ PLACEHOLDER }} |
| Maintainability (easy to modify?) | {{ PLACEHOLDER }} |

## Exercise 2.2: AI-Assisted Analysis (20 minutes)

**Task:** Use LLM approaches to analyze the build log and extract actionable fixes.

### Option A: Full Log Approach

```bash
# Set API key (choose one)
export OPENAI_API_KEY={{ YOUR_KEY }}
# OR
export ANTHROPIC_API_KEY={{ YOUR_KEY }}
# OR use Ollama (local)
# ollama serve  # in another terminal

# Run full log analysis
python3 03_llm_api_call.py | tee out_llm_full.json
```

**Note:** This sends the entire build log to the LLM. More expensive but comprehensive.

### Option B: Hybrid Approach (Recommended) ⭐

```bash
# Run hybrid approach (deterministic filtering + LLM)
python3 04_hybrid_approach.py --outdir .hybrid_out | tee out_llm_hybrid.txt

# View results
cat .hybrid_out/hybrid_result.json
```

**Note:** This filters errors first, then sends only relevant sections to LLM. 70-90% cost savings.

### Compare Approaches

Fill in this comparison table:

| Approach | Time | Evidence lines? | Actionable next step? | Est. tokens | Cost | Notes |
|----------|------|----------------|----------------------|-------------|------|-------|
| Grep | {{}} | {{Yes/No}} | {{}} | 0 | Free | {{}} |
| Python | {{}} | {{Yes/No}} | {{}} | 0 | Free | {{}} |
| LLM Full | {{}} | {{Yes/No}} | {{}} | {{}} | ~$0.04-0.10 | {{}} |
| Hybrid | {{}} | {{Yes/No}} | {{}} | {{}} | ~$0.004-0.01 | {{}} |

### Production Decision

**Which approach would you ship to production tomorrow? Why?**

{{ PLACEHOLDER - 1-2 sentences }}

## Exercise 2.3: Prompt Hardening (10 minutes)

**Task:** Improve the prompt to reduce hallucinations and increase reliability.

### Update Prompt Requirements

Modify the prompt in `04_hybrid_approach.py` (or create a new version) to require:

1. **Valid JSON schema** with `root_causes[*].evidence[].line + snippet`
2. **Evidence requirement:** "Quote the exact log line for each root cause"
3. **Uncertainty handling:** "If unsure → confidence: low + missing_data note"
4. **No invention:** "Do not invent symbols or error messages not in the log"

### Example Hardened Prompt

```python
prompt = """You are assisting the RDK CMF team. Analyse the following error sections from a CI build log.

I've already filtered the log to show only error lines with their surrounding context.

Return a JSON object with:
- root_causes: Array of top 3 failure causes, each with:
  * cause: Brief description of the root cause
  * evidence: Array of objects with:
    - line: Line number from log
    - snippet: Exact text from log line
  * confidence: high/medium/low
  * next_action: Specific, actionable steps to fix
  * missing_data: (if confidence is low) What information is missing
- summary: Array of 3 bullet points suitable for PR/Slack

IMPORTANT:
- Only cite errors that appear in the log sections below
- Quote exact log lines in evidence
- If uncertain, mark confidence as low and explain what's missing
- Do not invent symbols, error messages, or line numbers not in the log

ERROR SECTIONS:
[filtered error sections with context]
"""
```

### Re-run Hybrid with Hardened Prompt

```bash
# Update the prompt in 04_hybrid_approach.py, then:
python3 04_hybrid_approach.py --outdir .hybrid_out | tee out_llm_hardened.txt

# View improved results
cat .hybrid_out/hybrid_result.json
```

### Compare Results

- Did the hardened prompt reduce hallucinations?
- Are evidence citations more accurate?
- Are confidence levels more realistic?

## Deliverables

1. **`out_grep.txt`** - Grep/awk output
2. **`out_python.txt`** - Python script output
3. **`.hybrid_out/hybrid_result.json`** - Hybrid approach results
4. **`prompt_hardened.txt`** - Your improved prompt
5. **Comparison table** (filled in)
6. **Production decision** (1-2 sentences)

## Debrief Questions

Be ready to discuss:

1. **Precision/Recall:** Did the LLM find real issues? Did it hallucinate?
2. **Actionability:** Were the suggested fixes actually useful?
3. **Token Discipline:** How much did this cost? How could you reduce token usage?
4. **For your pain point #1 (log file analysis):**
   - How much time does this save vs. manual analysis?
   - Which approach (grep/Python/LLM/Hybrid) would you use in production?
   - What's the cost per analysis? Is it worth it?
5. **Hybrid approach benefits:**
   - 70-90% cost savings vs. full log
   - Deterministic filtering (auditable)
   - LLM analysis (intelligent)
   - **Recommended for production use**

## RDK Context

**You're analyzing build logs from github.com/rdkcentral** - the RDK Software Stack codebase you manage. This directly addresses your pain point: understanding build failures quickly.

**For your RDK context:** How would you integrate this into your Jenkins setup for github.com/rdkcentral builds?

