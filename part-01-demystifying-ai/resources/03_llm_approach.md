# LLM Approach: Build Log Analysis

## Prompt Template

This prompt is designed for analyzing RDK build logs. It requests structured output with evidence, confidence levels, and actionable next steps.

```
You are assisting the RDK CMF team. Analyse the following CI build log.

Return:
1) A JSON array of the top 3 failure causes with fields:
   - cause: Brief description of the root cause
   - evidence: Line numbers or code snippets that support this finding
   - confidence: high/medium/low
   - next_action: Specific, actionable steps to fix this issue

2) A 3-bullet human summary suitable for a PR comment or Slack message.

Prefer evidence over speculation. If uncertain, mark confidence low.
Cite specific line numbers or code snippets when possible.

LOG:
{{ PLACEHOLDER - paste build.log content here }}
```

## Expected Output Format

```json
{
  "root_causes": [
    {
      "cause": "Missing type definition: telemetry_config_t",
      "evidence": "Line 46: error: unknown type name 'telemetry_config_t'",
      "confidence": "high",
      "next_action": "Define telemetry_config_t in collector.h or include the header that defines it"
    },
    {
      "cause": "Missing library: json-c",
      "evidence": "Line 73: /usr/bin/ld: cannot find -ljson-c",
      "confidence": "high",
      "next_action": "Install libjson-c-dev: apt-get install libjson-c-dev"
    },
    {
      "cause": "Undefined references to telemetry_config_load, telemetry_malloc, telemetry_free",
      "evidence": "Lines 88-92: undefined reference to 'telemetry_config_load'",
      "confidence": "high",
      "next_action": "Link telemetry_common library to telemetry_collector in CMakeLists.txt"
    }
  ],
  "summary": [
    "Build failed due to missing type definitions and undefined references in collector module",
    "Missing json-c library required for API module",
    "Three compilation errors and two linker errors need to be resolved"
  ]
}
```

## When to Use LLM vs. Automation

**Use LLM when:**
- ✅ You need explanations for complex errors
- ✅ You want actionable fix suggestions
- ✅ You need to communicate findings to humans (PR comments, Slack)
- ✅ Errors are unstructured or context-dependent
- ✅ You want confidence levels and reasoning

**Use automation (grep/Python) when:**
- ✅ You need fast, deterministic parsing
- ✅ Error patterns are well-structured
- ✅ You need auditability and reproducibility
- ✅ Cost is a concern (high volume)
- ✅ You need real-time analysis in CI/CD

## Acceptance Checklist

When reviewing LLM output, verify:

- [ ] Does the output cite **evidence** (line numbers/snippets)?
- [ ] Can a reviewer reproduce the finding locally?
- [ ] Is there a clear **next action** that's safe to attempt?
- [ ] Is the confidence level appropriate (not overconfident)?
- [ ] Does the summary communicate clearly to non-experts?

## Cost Considerations

**Token usage:**
- Input: ~200-400 lines of build log = ~2000-4000 tokens
- Output: ~500-800 tokens
- **Total per analysis: ~2500-4800 tokens**

**Cost estimate (GPT-4):**
- ~$0.075 - $0.144 per analysis
- For 10 builds/day: ~$0.75 - $1.44/day
- For 100 builds/day: ~$7.50 - $14.40/day

**Cost optimization:**
- Use cheaper models (GPT-3.5, Claude Haiku) for routine analysis
- Reserve GPT-4 for complex, high-impact failures
- Batch multiple logs in one request when possible
- Cache results for identical error patterns

## Example Usage

See `03_llm_api_call.py` for a working implementation that:
- Reads the build log
- Calls an LLM API (OpenAI, Anthropic, or Ollama)
- Parses the JSON response
- Formats output for humans

